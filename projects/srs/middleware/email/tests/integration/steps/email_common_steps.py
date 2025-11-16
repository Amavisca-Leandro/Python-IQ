"""
Step definitions comuns para testes BDD do Email Service.

Este módulo fornece steps reutilizáveis para configuração e preparação
de dados nos testes do serviço de email do SRS.
"""

import allure
import logging
from pytest_bdd import given, parsers

logger = logging.getLogger(__name__)

# Allure feature and story decorators
allure.feature("Email Service - Setup")
allure.story("Common Test Preconditions")


@given("que o serviço de comunicação está disponível")
@allure.story("Service Health Check")
def servico_comunicacao_disponivel(email_service_client):
    """
    Verifica que o serviço de comunicação está disponível.

    Args:
        email_service_client: Cliente do Email Service

    Example in feature file:
        Dado que o serviço de comunicação está disponível
    """
    with allure.step("Verificar disponibilidade do serviço de comunicação"):
        assert email_service_client is not None, "Email service client não está inicializado"
        assert email_service_client.base_url is not None, "Base URL não configurada"

        allure.attach(
            email_service_client.base_url,
            name="Service Base URL",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info(f"Email service client configurado: {email_service_client.base_url}")


@given("tenho credenciais de administrador válidas")
@allure.story("Authentication Setup")
def credenciais_admin_validas(email_service_client):
    """
    Verifica que as credenciais de administrador estão configuradas.

    Args:
        email_service_client: Cliente do Email Service

    Example in feature file:
        E tenho credenciais de administrador válidas
    """
    with allure.step("Verificar credenciais de administrador"):
        assert email_service_client.api_key is not None, "API Key não configurada"

        # Mascarar API key para segurança
        masked_key = f"{email_service_client.api_key[:8]}...{email_service_client.api_key[-4:]}" \
            if len(email_service_client.api_key) > 12 else "***"

        allure.attach(
            masked_key,
            name="API Key (masked)",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info("Credenciais de administrador validadas")


@given("não estou autenticado")
@allure.story("Unauthenticated Access")
def nao_autenticado(srs_api_base_url):
    """
    Cria um cliente sem autenticação para testes negativos.

    Args:
        srs_api_base_url: URL base do serviço

    Example in feature file:
        Dado que não estou autenticado
    """
    with allure.step("Remover autenticação"):
        import sys
        from pathlib import Path

        # Adicionar o diretório raiz do projeto ao path
        project_root = Path(__file__).parent.parent.parent.parent.parent.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        from projects.srs.middleware.email.clients.email_client import EmailServiceClient

        # Cliente sem API key
        client = EmailServiceClient(base_url=srs_api_base_url, api_key=None)

        allure.attach(
            "Unauthenticated",
            name="Authentication Status",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info("Cliente não autenticado criado")
        return client


@given(parsers.parse('eu tenho os dados da API key:\n{data_table}'))
@allure.story("Data Preparation - API Key")
def dados_api_key(bdd_context, data_table):
    """
    Prepara dados para criação de API key a partir de uma tabela.

    Args:
        bdd_context: Contexto BDD para armazenar dados
        data_table: Tabela Gherkin com dados

    Example in feature file:
        Dado eu tenho os dados da API key:
            | campo        | valor                    |
            | name         | My API Key               |
            | expirationAt | 2025-12-31T23:59:59Z     |
    """
    with allure.step("Preparar dados da API key"):
        data = _parse_data_table(data_table)
        bdd_context.api_key_data = data

        allure.attach(
            str(data),
            name="API Key Data",
            attachment_type=allure.attachment_type.JSON
        )

        logger.info(f"Dados da API key preparados: {list(data.keys())}")


@given(parsers.parse('eu tenho os dados do template:\n{data_table}'))
@allure.story("Data Preparation - Template")
def dados_template(bdd_context, data_table):
    """
    Prepara dados para criação de template a partir de uma tabela.

    Args:
        bdd_context: Contexto BDD para armazenar dados
        data_table: Tabela Gherkin com dados

    Example in feature file:
        Dado eu tenho os dados do template:
            | campo   | valor              |
            | type    | email              |
            | name    | Welcome Email      |
            | subject | Bem-vindo {{name}} |
    """
    with allure.step("Preparar dados do template"):
        data = _parse_data_table(data_table)
        bdd_context.template_data = data

        allure.attach(
            str(data),
            name="Template Data",
            attachment_type=allure.attachment_type.JSON
        )

        logger.info(f"Dados do template preparados: {list(data.keys())}")


@given(parsers.parse('eu tenho os dados do email:\n{data_table}'))
@allure.story("Data Preparation - Email")
def dados_email(bdd_context, data_table):
    """
    Prepara dados para envio de email a partir de uma tabela.

    Args:
        bdd_context: Contexto BDD para armazenar dados
        data_table: Tabela Gherkin com dados

    Example in feature file:
        Dado eu tenho os dados do email:
            | campo   | valor                |
            | to      | test@example.com     |
            | subject | Test Email           |
            | body    | Test body            |
    """
    with allure.step("Preparar dados do email"):
        data = _parse_data_table(data_table)

        # Converter campo 'to' em lista se for string
        if 'to' in data and isinstance(data['to'], str):
            data['to'] = [email.strip() for email in data['to'].split(',')]

        bdd_context.email_data = data

        allure.attach(
            str(data),
            name="Email Data",
            attachment_type=allure.attachment_type.JSON
        )

        logger.info(f"Dados do email preparados: {list(data.keys())}")


@given(parsers.parse('eu tenho os dados atualizados:\n{data_table}'))
@allure.story("Data Preparation - Update")
def dados_atualizados(bdd_context, data_table):
    """
    Prepara dados para atualização de recursos.

    Args:
        bdd_context: Contexto BDD para armazenar dados
        data_table: Tabela Gherkin com dados

    Example in feature file:
        E eu tenho os dados atualizados:
            | campo    | valor              |
            | name     | Updated Name       |
            | isActive | true               |
    """
    with allure.step("Preparar dados para atualização"):
        data = _parse_data_table(data_table)
        bdd_context.update_data = data

        allure.attach(
            str(data),
            name="Update Data",
            attachment_type=allure.attachment_type.JSON
        )

        logger.info(f"Dados de atualização preparados: {list(data.keys())}")


@given("eu tenho os dados da API key sem o campo \"name\"")
@allure.story("Data Preparation - Invalid")
def dados_api_key_sem_nome(bdd_context):
    """
    Prepara dados inválidos de API key sem o campo name.

    Args:
        bdd_context: Contexto BDD

    Example in feature file:
        Dado eu tenho os dados da API key sem o campo "name"
    """
    with allure.step("Preparar dados inválidos (sem name)"):
        data = {
            "expirationAt": "2025-12-31T23:59:59Z",
            "tier": "premium"
        }
        bdd_context.api_key_data = data

        allure.attach(
            str(data),
            name="Invalid API Key Data",
            attachment_type=allure.attachment_type.JSON
        )

        logger.info("Dados inválidos de API key preparados (sem name)")


def _parse_data_table(data_table: str) -> dict:
    """
    Converte uma tabela Gherkin em dicionário Python.

    Args:
        data_table: String da tabela Gherkin

    Returns:
        Dicionário com os dados parseados
    """
    data = {}
    lines = data_table.strip().split('\n')

    # Pular linha de cabeçalho
    for line in lines[1:]:
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            parts = [p for p in parts if p]

            if len(parts) >= 2:
                field = parts[0]
                value = parts[1]

                # Converter valor para tipo apropriado
                converted_value = _convert_value(value)
                data[field] = converted_value

    return data


def _convert_value(value: str):
    """
    Converte valor string para tipo Python apropriado.

    Args:
        value: Valor como string

    Returns:
        Valor convertido
    """
    import json

    # Null/None
    if value.lower() in ('null', 'none', ''):
        return None

    # Booleans
    if value.lower() == 'true':
        return True
    if value.lower() == 'false':
        return False

    # JSON objects/arrays
    if value.startswith(('{', '[')):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass

    # Integer
    try:
        return int(value)
    except ValueError:
        pass

    # Float
    try:
        return float(value)
    except ValueError:
        pass

    # String
    return value
