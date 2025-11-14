# 📁 Estrutura de Testes do Projeto Python-IQ

## 🎯 Visão Geral

O projeto foi **totalmente convertido para BDD** e reorganizado em uma estrutura clara que separa **testes de sistema** e **testes funcionais**.

**Estatísticas:**
- ✅ **203 testes** coletados
- ✅ **100% dos testes funcionais** em BDD (Gherkin + pytest-bdd)
- ✅ **Frontend usa BDD + Page Object Model** (combinação recomendada)
- ✅ **API usa steps reutilizáveis** para todos os endpoints

---

## 📂 Estrutura de Diretórios

```
tests/
│
├── system/                                    # 🔧 TESTES DE SISTEMA (Infraestrutura)
│   ├── test_database_integration.py          # Testa DatabaseManager, ORM, Connection Pool
│   ├── test_ui_backend_db_integration.py     # Testa integração completa UI→API→DB
│   ├── test_explorer_verification.py         # Verificação do Test Explorer
│   └── test_simple_verification.py           # Testes simples de verificação
│
├── functional/                                # ✅ TESTES FUNCIONAIS (Cenários de Negócio)
│   │
│   ├── backend/                               # 📡 TESTES BACKEND (API)
│   │   ├── test_users_api.py                 # Users API (CRUD completo)
│   │   ├── test_posts_api.py                 # Posts API (CRUD + validações)
│   │   ├── test_comments_api.py              # Comments API
│   │   ├── test_todos_api.py                 # Todos API (boolean validation)
│   │   ├── test_albums_api.py                # Albums API
│   │   ├── test_filters_api.py               # Filtros e query parameters
│   │   ├── test_data_management.py           # Gerenciamento de dados de teste
│   │   ├── test_database_steps.py            # Steps de banco de dados
│   │   ├── test_end_to_end_integration.py    # Integração E2E
│   │   └── test_api_steps_validation.py      # Validação de steps de API
│   │
│   └── frontend/                              # 🖥️ TESTES FRONTEND (UI)
│       ├── test_login_ui.py                   # Login e autenticação
│       └── test_user_journey_ui.py            # Jornadas do usuário
│
├── bdd/                                       # 📝 ARQUIVOS BDD (Features, Steps, Config)
│   ├── features/                              # Arquivos .feature (Gherkin)
│   │   ├── api/                               # Features de API
│   │   │   ├── users.feature
│   │   │   ├── posts.feature
│   │   │   ├── comments.feature
│   │   │   ├── todos.feature
│   │   │   ├── albums.feature
│   │   │   └── filters.feature
│   │   │
│   │   ├── ui/                                # Features de UI
│   │   │   ├── login.feature
│   │   │   └── user_journey.feature
│   │   │
│   │   ├── database/                          # Features de Database
│   │   │   ├── user_management.feature
│   │   │   └── data_management.feature
│   │   │
│   │   └── integration/                       # Features de Integração E2E
│   │       └── end_to_end.feature
│   │
│   ├── steps/                                 # Step definitions (Python)
│   │   ├── api_steps.py                       # Steps de API (GET, POST, PUT, DELETE)
│   │   ├── ui_steps.py                        # Steps de UI (Playwright + POM)
│   │   ├── database_steps.py                  # Steps de Database
│   │   ├── assertions_steps.py                # Steps de assertions
│   │   └── common_steps.py                    # Steps comuns
│   │
│   └── conftest.py                            # Configurações e fixtures BDD
│
└── jsonplaceholder/                           # 📊 TESTES PERFORMANCE (não-BDD)
    ├── test_performance.py                    # Testes de performance e tempo de resposta
    ├── conftest.py                            # Fixtures do JSONPlaceholder
    └── conftest_metrics.py                    # Plugin de métricas
```

---

## 🔍 Classificação dos Testes

### 🔧 **TESTES DE SISTEMA (4 arquivos)**
Testam a **infraestrutura técnica** e **componentes do framework**:
- DatabaseManager (connection pooling, transactions, cleanup)
- SQLAlchemy ORM models e relationships
- TestDataFactory (criação e limpeza de dados)
- Integração completa UI→API→Database (validação do framework)

**Quando executar:**
```bash
pytest tests/system/
```

---

### ✅ **TESTES FUNCIONAIS (12 arquivos)**

#### 📡 **BACKEND - API (10 arquivos)**
Testam **funcionalidades de negócio** através da API REST:
- ✅ CRUD completo para todos os endpoints (Users, Posts, Comments, Todos, Albums)
- ✅ Validação de schemas JSON
- ✅ Filtros e query parameters
- ✅ Integração com banco de dados
- ✅ Fluxos E2E (criar → ler → atualizar → deletar → validar)

**Endpoints cobertos:**
- `/users` - Gerenciamento de usuários
- `/posts` - Posts e publicações
- `/comments` - Comentários
- `/todos` - Lista de tarefas
- `/albums` - Álbuns
- Todos com suporte a filtros (`?userId=1`, `?postId=1`)

**Quando executar:**
```bash
# Todos os testes de API
pytest tests/functional/backend/

# Apenas testes smoke
pytest tests/functional/backend/ -m smoke

# Apenas CRUD
pytest tests/functional/backend/ -m crud

# Apenas validações
pytest tests/functional/backend/ -m validation
```

#### 🖥️ **FRONTEND - UI (2 arquivos)**
Testam **interface do usuário** usando **BDD + Page Object Model**:
- ✅ Login e autenticação
- ✅ Logout
- ✅ Navegação entre páginas
- ✅ Edição de perfil
- ✅ Jornadas completas do usuário

**Tecnologias:**
- pytest-bdd (cenários em Gherkin)
- Playwright (automação de browser)
- Page Object Model (organização do código)

**Quando executar:**
```bash
# Todos os testes de UI
pytest tests/functional/frontend/

# Apenas login
pytest tests/functional/frontend/test_login_ui.py

# Multi-browser
pytest tests/functional/frontend/ --browser chromium --browser firefox
```

---

## 🎯 Comandos de Execução

### Por Tipo de Teste

```bash
# Testes de Sistema (infraestrutura)
pytest tests/system/

# Testes Funcionais Backend (API)
pytest tests/functional/backend/

# Testes Funcionais Frontend (UI)
pytest tests/functional/frontend/

# Todos os testes
pytest
```

### Por Marker (Tags)

```bash
# Testes críticos (smoke)
pytest -m smoke

# Testes de regressão completa
pytest -m regression

# Apenas testes de API
pytest -m api

# Apenas testes de UI
pytest -m frontend

# CRUD operations
pytest -m crud

# Validações
pytest -m validation

# Testes rápidos (exclui slow)
pytest -m "not slow"
```

### Por Funcionalidade

```bash
# Apenas testes de usuários
pytest -k "user"

# Apenas testes de login
pytest tests/functional/frontend/test_login_ui.py

# Apenas testes de posts com filtro
pytest tests/functional/backend/test_posts_api.py -m filter
```

### Execução Paralela

```bash
# Backend (paralelizável)
pytest tests/functional/backend/ -n 4

# Frontend (cuidado com browsers)
pytest tests/functional/frontend/ -n 2
```

---

## 📊 Relatórios

### Allure Report

```bash
# Gerar relatório
pytest --alluredir=reports/allure-results
allure serve reports/allure-results

# Ou usar os scripts
scripts/gerar_allure.bat        # Windows
scripts/allure_server.bat       # Windows (com live reload)
```

### HTML Report

```bash
pytest tests/functional/ --html=reports/functional_report.html --self-contained-html
```

---

## 🏗️ Arquitetura BDD

### Feature Files (Gherkin)
Localização: `tests/bdd/features/`

Exemplo:
```gherkin
@smoke @backend @api
Feature: JSONPlaceholder Users API
  As a QA engineer
  I want to test the Users API
  So that I can ensure it works correctly

  @crud @get
  Scenario: Get all users
    When I send a GET request to "/users"
    Then the response status code should be 200
    And the response should be a non-empty list
```

### Step Definitions (Python)
Localização: `tests/bdd/steps/`

Exemplo:
```python
@when(parsers.parse('I send a GET request to "{endpoint}"'))
def send_get_request(bdd_context, jsonplaceholder_client, endpoint):
    response = jsonplaceholder_client.client.get(endpoint)
    bdd_context.response = response
```

### Test Runners (pytest)
Localização: `tests/functional/backend/`, `tests/functional/frontend/`

Exemplo:
```python
from pytest_bdd import scenarios
from tests.bdd.steps.api_steps import *

scenarios('api/users.feature')
```

---

## 🎨 Page Object Model (Frontend)

Os testes de UI seguem o padrão **BDD + Page Object Model**:

**Page Objects:**
- `core/ui/pages/login_page.py` - LoginPage
- `core/ui/pages/dashboard_page.py` - DashboardPage
- `core/ui/pages/user_profile_page.py` - UserProfilePage

**Steps de UI:**
- `tests/bdd/steps/ui_steps.py` - Steps que utilizam os Page Objects

**Combinação:**
```gherkin
Given I am on the login page          # ui_steps.py → LoginPage
When I fill the login form            # ui_steps.py → LoginPage.login()
Then I should see the dashboard       # ui_steps.py → DashboardPage.is_loaded()
```

---

## 📈 Cobertura de Testes

### API (JSONPlaceholder)
- ✅ GET `/users` (listar e por ID)
- ✅ POST `/users` (criar)
- ✅ PUT `/users/{id}` (atualizar)
- ✅ DELETE `/users/{id}` (deletar)
- ✅ GET `/posts` + filtros
- ✅ GET `/comments` + filtros
- ✅ GET `/todos` + validação boolean
- ✅ GET `/albums`
- ✅ Validação de schemas JSON
- ✅ Validação de tipos de dados
- ✅ Testes de filtros cross-resource

### UI (Frontend)
- ✅ Login com credenciais válidas
- ✅ Login com credenciais inválidas
- ✅ Logout
- ✅ Navegação entre páginas
- ✅ Edição de perfil
- ✅ Cancelamento de edições
- ✅ Validação de formulários

### Database
- ✅ Criação de dados de teste
- ✅ Queries e validações
- ✅ Cleanup automático
- ✅ Relacionamentos (User → Profile)
- ✅ Transações e rollback

---

## 🔧 Configuração

### pytest.ini
```ini
[pytest]
testpaths =
    tests/system
    tests/functional/backend
    tests/functional/frontend

markers =
    smoke: Critical path tests
    regression: Full test suite
    backend: API tests
    frontend: UI tests
    api: API endpoint tests
    crud: CRUD operations
    validation: Data validation
    # ... e mais

bdd_features_base_dir = tests/bdd/features/
```

### Fixtures BDD
Localização: `tests/bdd/conftest.py`

Principais fixtures:
- `bdd_context` - Contexto BDD para compartilhar dados entre steps
- `jsonplaceholder_client` - Cliente API configurado
- `authenticated_page` - Página Playwright autenticada

---

## 📚 Documentação Adicional

- [README.md](README.md) - Documentação principal do framework
- [CLAUDE.md](CLAUDE.md) - Instruções para Claude Code
- [tests/bdd/README.md](tests/bdd/README.md) - Documentação detalhada do BDD

---

## ✨ Próximos Passos

1. ✅ Estrutura organizada (Sistema vs Funcional)
2. ✅ Todos os testes em BDD
3. ✅ Frontend com BDD + POM
4. ⏳ CI/CD pipelines (GitHub Actions)
5. ⏳ Integração com Zephyr Scale
6. ⏳ Testes de performance detalhados

---

**Última atualização:** 2025-11-14
**Total de testes:** 203
**Status:** ✅ Produção Ready
