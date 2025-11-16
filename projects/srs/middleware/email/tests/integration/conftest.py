"""
Configuração e fixtures específicas para testes BDD do Email Service.
"""

import pytest
import os
from pathlib import Path

# Configurar caminho base para features
@pytest.fixture(scope="session", autouse=True)
def configure_bdd_paths():
    """Configura os caminhos para os arquivos .feature"""
    # Garantir que o pytest-bdd encontre as features
    os.environ['PYTEST_BDD_STRICT_GHERKIN'] = '0'


@pytest.fixture(scope="session")
def srs_api_base_url():
    """
    URL base da API do SRS Middleware.

    Returns:
        str: URL configurada no .env.srs ou padrão local
    """
    from dotenv import load_dotenv

    # Tentar carregar .env.srs
    env_file = Path(__file__).parent.parent.parent.parent / '.env.srs'
    if env_file.exists():
        load_dotenv(env_file)

    return os.getenv('EMAIL_SERVICE_URL', 'http://localhost:3000')


@pytest.fixture(scope="session")
def srs_api_key():
    """
    API Key para autenticação no SRS Middleware.

    Returns:
        str: API Key configurada ou None
    """
    from dotenv import load_dotenv

    env_file = Path(__file__).parent.parent.parent.parent / '.env.srs'
    if env_file.exists():
        load_dotenv(env_file)

    return os.getenv('EMAIL_SERVICE_API_KEY')


@pytest.fixture
def email_service_client(srs_api_base_url, srs_api_key):
    """
    Cliente do Email Service configurado.

    Returns:
        EmailServiceClient: Cliente HTTP configurado
    """
    # Importação relativa do cliente
    import sys
    from pathlib import Path

    # Adicionar o diretório raiz do projeto ao path
    project_root = Path(__file__).parent.parent.parent.parent.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # Importar usando caminho absoluto a partir da raiz
    from projects.srs.middleware.email.clients.email_client import EmailServiceClient

    return EmailServiceClient(
        base_url=srs_api_base_url,
        api_key=srs_api_key
    )


@pytest.fixture
def sample_api_key_data():
    """Dados de exemplo para criação de API Key."""
    return {
        "name": "Test API Key",
        "expirationAt": "2025-12-31T23:59:59Z",
        "tier": "premium",
        "isInternal": False
    }


@pytest.fixture
def sample_template_data():
    """Dados de exemplo para criação de Template."""
    return {
        "type": "email",
        "name": "Test Welcome Email",
        "subject": "Welcome to {{company}}!",
        "body": "Hello {{name}}, welcome!",
        "html": "<h1>Hello {{name}}</h1><p>Welcome to {{company}}!</p>",
        "description": "Test template"
    }


@pytest.fixture
def sample_email_data():
    """Dados de exemplo para envio de email simples."""
    return {
        "to": ["test@example.com"],
        "subject": "Test Email",
        "body": "This is a test email"
    }


@pytest.fixture
def bdd_context():
    """
    Contexto BDD para compartilhar dados entre steps.

    Este fixture cria um objeto de contexto que pode armazenar dados
    temporários durante a execução de um cenário BDD, permitindo que
    diferentes steps compartilhem informações.

    Returns:
        BDDContext: Objeto de contexto para armazenar dados do cenário

    Example:
        @given("eu tenho os dados do email")
        def prepare_email_data(bdd_context):
            bdd_context.email_data = {"to": ["test@example.com"]}

        @when("eu envio o email")
        def send_email(bdd_context, email_service_client):
            response = email_service_client.send_email(**bdd_context.email_data)
            bdd_context.response = response
    """
    class BDDContext:
        """Contexto para armazenar dados temporários durante testes BDD."""
        pass

    return BDDContext()


@pytest.fixture(scope="function")
def cleanup_created_resources(request):
    """
    Fixture para cleanup automático de recursos criados durante os testes.

    Uso:
        def test_example(cleanup_created_resources):
            cleanup_created_resources.add('api_key', api_key_id)
            cleanup_created_resources.add('template', template_id)
    """
    class ResourceCleaner:
        def __init__(self):
            self.resources = []

        def add(self, resource_type, resource_id):
            """Adiciona um recurso para cleanup"""
            self.resources.append((resource_type, resource_id))

        def cleanup(self, client):
            """Executa o cleanup de todos os recursos"""
            for resource_type, resource_id in reversed(self.resources):
                try:
                    if resource_type == 'api_key':
                        client.delete(f'/api-keys/{resource_id}')
                    elif resource_type == 'template':
                        client.delete(f'/templates/{resource_id}')
                except Exception as e:
                    # Ignorar erros no cleanup
                    pass

    cleaner = ResourceCleaner()
    yield cleaner

    # Cleanup após o teste
    if hasattr(request, 'node') and hasattr(request.node, 'funcargs'):
        if 'email_service_client' in request.node.funcargs:
            client = request.node.funcargs['email_service_client']
            cleaner.cleanup(client)
