# Python Test Automation Framework

Framework completo de automação de testes funcionais usando Python, suportando testes de backend (API) e frontend (UI) com integração CI/CD, reporting avançado e sincronização com Zephyr Scale.

## 📋 Índice

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [🚀 Início Rápido - Execute Testes SEM Linha de Comando](#-início-rápido---execute-testes-sem-linha-de-comando)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração](#configuração)
- [Execução de Testes](#execução-de-testes)
- [Reporting](#reporting)
- [CI/CD](#cicd)
- [Contribuindo](#contribuindo)

## ✨ Características

- **Testes de Backend (API)**: Cliente HTTP robusto com retry automático e autenticação
- **Testes de Frontend (UI)**: Automação com Playwright e Page Objects
- **Integração com Banco de Dados**: SQLAlchemy ORM para criação de massa de dados e validações
- **Validação de Dados**: Modelos Pydantic para type safety e validação
- **📊 Reporting Avançado**: Relatórios interativos com Allure (dashboard, steps, screenshots, histórico)
- **Gestão de Testes**: Sincronização automática com Zephyr Scale
- **CI/CD**: Pipelines prontos para GitHub Actions
- **Execução Paralela**: Suporte a pytest-xdist para performance
- **Múltiplos Ambientes**: Configuração flexível para dev, staging e prod

## 🔧 Requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git
- Acesso ao banco de dados PostgreSQL (para testes de integração)

## 🚀 Início Rápido - Execute Testes SEM Linha de Comando!

### ⚡ Método 1: Test Explorer do VS Code (RECOMENDADO)

1. Abra o VS Code
2. Clique no ícone 🧪 **"Testing"** na barra lateral
3. Clique em **"Refresh Tests"** (🔄)
4. Clique no ▶️ ao lado de qualquer teste

**Pronto!** O navegador abre e executa o teste automaticamente! ✅

### ⚡ Método 2: Duplo Clique

1. Vá na pasta `scripts`
2. Dê duplo clique em **`run_ui_mode.bat`**
3. Veja os testes executarem!

### 📚 Guias Completos

- **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Guia visual passo a passo
- **[COMO_EXECUTAR_TESTES.md](COMO_EXECUTAR_TESTES.md)** - Todas as formas de executar
- **[GERAR_RELATORIOS_RAPIDO.md](GERAR_RELATORIOS_RAPIDO.md)** 📊 - Como gerar relatórios
- **[docs/ALLURE_QUICK_START.md](docs/ALLURE_QUICK_START.md)** 🎯 - Allure Reports - Guia Rápido
- **[docs/ALLURE_GUIDE.md](docs/ALLURE_GUIDE.md)** 📈 - Allure Reports - Guia Completo
- **[docs/COMO_USAR_TEST_EXPLORER.md](docs/COMO_USAR_TEST_EXPLORER.md)** - Test Explorer detalhado
- **[docs/INTERFACES_GRAFICAS_TESTES.md](docs/INTERFACES_GRAFICAS_TESTES.md)** - Todas as interfaces disponíveis
- **[SOLUCAO_ERROS.md](SOLUCAO_ERROS.md)** 🔧 - Solução de erros comuns

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone <repository-url>
cd qa-automation
```

### 2. Crie e ative o ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Instale os browsers do Playwright

```bash
playwright install
```

### 5. Configure as variáveis de ambiente

Copie o arquivo de exemplo e configure suas credenciais:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edite o arquivo `.env` com suas configurações.

## 📁 Estrutura do Projeto

```
qa-automation/
├── .github/workflows/      # Pipelines de CI/CD
├── core/                   # Framework core
│   ├── api/                # Cliente de API e endpoints
│   ├── config/             # Gerenciamento de configuração
│   ├── database/           # Integração com banco de dados
│   │   ├── manager.py      # Database manager
│   │   ├── factory.py      # Test data factory
│   │   ├── models.py       # SQLAlchemy models
│   │   └── fixtures.py     # Database fixtures
│   ├── helpers/            # Funções utilitárias
│   ├── models/             # Modelos Pydantic
│   └── ui/                 # Componentes de UI
├── tests/                  # Suites de teste
│   ├── backend/            # Testes de API
│   ├── frontend/           # Testes de UI
│   ├── integration/        # Testes end-to-end
│   └── conftest.py         # Fixtures globais
├── fixtures/               # Dados de teste
│   ├── sql/                # Scripts SQL
│   └── json/               # Dados JSON
├── scripts/                # Scripts utilitários
├── reports/                # Relatórios gerados
├── docs/                   # Documentação
├── .env.example            # Exemplo de variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
├── pytest.ini              # Configuração do pytest
├── requirements.txt        # Dependências Python
└── README.md               # Este arquivo
```

## ⚙️ Configuração

### Variáveis de Ambiente

Configure as seguintes variáveis no arquivo `.env`:

```env
# Environment
ENV=dev

# API Configuration
API_BASE_URL=https://api.example.com
API_TIMEOUT=30
API_RETRIES=3

# Authentication
AUTH_USER=your_username
AUTH_PASSWORD=your_password

# Frontend Configuration
FRONTEND_BASE_URL=https://app.example.com
BROWSER=chromium
HEADLESS=true

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=test_db
DB_USER=postgres
DB_PASSWORD=your_db_password

# Integrations (opcional)
ZEPHYR_API_TOKEN=your_zephyr_token
JIRA_API_TOKEN=your_jira_token
```

### Configuração do pytest

O arquivo `pytest.ini` contém configurações padrão. Personalize conforme necessário.

## 🚀 Execução de Testes

### 🎯 Test Explorer (Interface Gráfica)

**Recomendado para desenvolvimento!** Execute testes com interface visual integrada ao Kiro/VS Code:

1. **Abrir Test Explorer:**
   - Clique no ícone 🧪 (Testing) na sidebar esquerda
   - Ou use: `Ctrl+Shift+P` → `Test: Focus on Test Explorer View`

2. **Executar testes:**
   - Clique no botão ▶ (play) ao lado de qualquer teste, arquivo ou pasta
   - Use o botão 🐛 (debug) para debugar com breakpoints

3. **Ver resultados:**
   - Status visual (✓ verde, ✗ vermelho) inline no código
   - Tempo de execução e mensagens de erro no painel
   - Navegação rápida para falhas

📖 **[Guia Completo do Test Explorer](docs/test-explorer-guide.md)** - Setup, troubleshooting e melhores práticas

### Executar todos os testes (CLI)

```bash
pytest
```

### Executar testes por categoria

```bash
# Testes smoke (críticos)
pytest -m smoke

# Testes de backend
pytest -m backend

# Testes de frontend
pytest -m frontend

# Testes de regressão
pytest -m regression
```

### Executar testes em paralelo

```bash
pytest -n auto  # Usa todos os cores disponíveis
pytest -n 4     # Usa 4 workers
```

### Executar testes específicos

```bash
# Por arquivo
pytest tests/backend/test_auth.py

# Por função
pytest tests/backend/test_auth.py::test_login_success

# Por padrão no nome
pytest -k "login"
```

### Gerar relatório Allure

```bash
# Executar testes e gerar dados
pytest --alluredir=allure-results

# Gerar e abrir relatório
allure serve allure-results
```

## 📊 Reporting

### 🎯 Allure Reports

[![Allure Report](https://img.shields.io/badge/Allure-Report-yellow.svg)](https://docs.qameta.io/allure/)

O framework gera relatórios interativos e detalhados com Allure Framework.

#### 🚀 Início Rápido

```bash
# 1. Executar testes
pytest tests/ --alluredir=reports/allure-results

# 2. Gerar relatório (Método Fácil)
scripts\gerar_allure.bat  # Windows
./scripts/gerar_allure.sh # Unix/Linux/macOS

# OU iniciar servidor com live reload
scripts\allure_server.bat  # Windows
./scripts/allure_server.sh # Unix/Linux/macOS
```

#### 📋 Recursos do Relatório

- **Dashboard Interativo**: Estatísticas, gráficos e tendências
- **Steps Detalhados**: Cada teste mostra passos de execução
- **Screenshots Automáticos**: Captura em falhas de testes UI
- **Anexos**: Request/Response de APIs, logs, dados de teste
- **Categorização**: Falhas classificadas automaticamente
- **Histórico**: Acompanhe evolução dos testes
- **Severidade**: Testes organizados por criticidade (BLOCKER, CRITICAL, NORMAL)
- **Features & Stories**: Agrupamento por funcionalidade

#### 📚 Documentação Completa

- **[Guia Rápido do Allure](docs/ALLURE_QUICK_START.md)** - Instalação e comandos essenciais
- **[Guia Completo do Allure](docs/ALLURE_GUIDE.md)** - Decoradores, recursos avançados, CI/CD
- **[Scripts README](scripts/ALLURE_SCRIPTS_README.md)** - Documentação dos scripts

#### 🛠️ Instalação do Allure CLI

**Windows:**
```bash
scoop install allure  # Recomendado
# OU
npm install -g allure-commandline
```

**macOS:**
```bash
brew install allure
```

**Linux:**
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update && sudo apt-get install allure
```

#### 🎨 Exemplo de Uso nos Testes

```python
import allure

@allure.feature("User Management")
@allure.story("Create User")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_user(api_client):
    with allure.step("Prepare user data"):
        user_data = {"name": "João", "email": "joao@example.com"}
    
    with allure.step("Send POST request"):
        response = api_client.post("/users", json=user_data)
        allure.attach(response.text, "Response", allure.attachment_type.JSON)
    
    with allure.step("Validate response"):
        assert response.status_code == 201
```

### Zephyr Scale Integration

Os resultados são sincronizados automaticamente com Zephyr Scale após a execução no CI/CD.

## 🔄 CI/CD

### GitHub Actions

O projeto inclui workflows para:

1. **Backend Tests** (`.github/workflows/backend-tests.yml`)
   - Executa em PRs e pushes para main
   - Testes de API e integração

2. **Frontend Tests** (`.github/workflows/frontend-tests.yml`)
   - Testes de UI em múltiplos browsers
   - Captura de screenshots e vídeos

3. **Nightly Regression** (`.github/workflows/nightly-regression.yml`)
   - Suite completa executada diariamente
   - Notificações em caso de falha

## 🧪 Escrevendo Testes

### Exemplo de Teste de API

```python
import pytest
from core.models.user import UserCreate

@pytest.mark.backend
@pytest.mark.smoke
def test_create_user(api_client):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="SecurePass123!"
    )
    
    response = api_client.post("/users", json=user_data.dict())
    
    assert response.status_code == 201
    assert response.json()["username"] == user_data.username
```

### Exemplo de Teste de UI

```python
import pytest

@pytest.mark.frontend
@pytest.mark.smoke
def test_login_success(login_page, dashboard_page):
    login_page.navigate()
    login_page.login("testuser", "password123")
    
    assert dashboard_page.is_displayed()
    assert dashboard_page.get_welcome_message() == "Welcome, testuser!"
```

### Exemplo de Teste com Banco de Dados

```python
import pytest

@pytest.mark.integration
def test_user_workflow_with_database(api_client, db_manager, test_data_factory, test_data_context):
    # Criar massa de dados
    user_data = test_data_factory.create_user_with_profile(
        test_id=test_data_context.test_id,
        email="integration@test.com"
    )
    
    # Executar ação via API
    response = api_client.get(f"/users/{user_data.user.id}")
    assert response.status_code == 200
    
    # Validar no banco
    with db_manager.get_session() as session:
        user = session.query(User).filter(User.id == user_data.user.id).first()
        assert user.email == "integration@test.com"
    
    # Cleanup automático via fixture
```

## 🤝 Contribuindo

1. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
2. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
3. Push para a branch (`git push origin feature/nova-feature`)
4. Abra um Pull Request

## 📝 Convenções

- Use type hints em todo o código Python
- Siga PEP 8 para estilo de código
- Escreva docstrings para funções e classes
- Mantenha testes focados e independentes
- Use fixtures para setup/teardown
- Adicione markers apropriados aos testes

## 🐛 Troubleshooting

### Erro de conexão com banco de dados

Verifique se o PostgreSQL está rodando e as credenciais no `.env` estão corretas.

### Browsers do Playwright não instalados

Execute: `playwright install`

### Testes falhando por timeout

Aumente o valor de `API_TIMEOUT` no `.env` ou ajuste timeouts específicos nos testes.

## 📚 Documentação Adicional

- [Pytest Documentation](https://docs.pytest.org/)
- [Playwright Python](https://playwright.dev/python/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Allure Framework](https://docs.qameta.io/allure/)

## 📄 Licença

[Adicione informações de licença aqui]

## 👥 Autores

[Adicione informações dos autores aqui]
