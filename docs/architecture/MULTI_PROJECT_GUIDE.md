# Guia de Organização Multi-Projeto

Este guia explica como usar o python-iq como framework reutilizável para múltiplos projetos e escopos.

## 🎯 Conceito

O **python-iq** é um framework de automação de testes que pode ser usado por **múltiplos projetos**. Cada projeto mantém seus próprios testes, clientes e configurações, mas **reutiliza o core** do framework.

### Estrutura Geral

```
python-iq/                      # Framework (reutilizável)
├── core/                       # ✅ Compartilhado por todos
│   ├── api/                    # Cliente API base
│   ├── ui/                     # Page Object Model base
│   ├── database/               # Database manager
│   ├── config/                 # Settings management
│   └── helpers/                # Utilitários
│
├── projects/                   # 🔥 Projetos específicos
│   ├── projeto-a/              # Projeto A
│   ├── projeto-b/              # Projeto B
│   └── srs/                    # Exemplo: Projeto SRS
│
└── docs/                       # Documentação do framework
```

---

## 📁 Anatomia de um Projeto

Cada projeto na pasta `projects/` segue esta estrutura:

```
projects/nome-projeto/
├── camada1/                    # Ex: middleware, backend, frontend
│   ├── servico1/               # Ex: email, sms, api-users
│   │   ├── tests/
│   │   │   ├── bdd/
│   │   │   │   ├── features/   # Arquivos .feature
│   │   │   │   └── steps/      # Step definitions
│   │   │   └── functional/     # Testes pytest
│   │   ├── clients/            # Clientes HTTP/API
│   │   ├── models/             # Schemas Pydantic
│   │   └── conftest.py         # Fixtures específicas
│   │
│   ├── servico2/
│   └── conftest.py             # Fixtures da camada
│
├── camada2/
├── .env.nome-projeto.example   # Template de configuração
├── pytest.ini                  # Configuração pytest
└── README.md                   # Documentação do projeto
```

---

## 🚀 Criando um Novo Projeto

### Passo 1: Estrutura de Diretórios

```bash
# Criar estrutura base
mkdir -p projects/meu-projeto/{camada1/{servico1,servico2},camada2}

# Exemplo real (projeto SRS):
mkdir -p projects/srs/{middleware/{email,sms},backend,frontend,integration}
```

### Passo 2: Configuração (.env)

Crie `.env.nome-projeto.example`:

```env
# .env.meu-projeto.example

# Environment
ENV=dev

# === CAMADA 1 - SERVIÇO 1 ===
SERVICO1_URL=https://api.example.com/servico1
SERVICO1_API_KEY=your_api_key

# === CAMADA 2 ===
CAMADA2_URL=https://api.example.com/camada2
CAMADA2_AUTH_USER=user
CAMADA2_AUTH_PASSWORD=pass
```

### Passo 3: Configuração pytest.ini

```ini
# projects/meu-projeto/pytest.ini

[pytest]
testpaths =
    camada1
    camada2

markers =
    camada1: Testes da camada 1
    servico1: Testes do serviço 1
    smoke: Smoke tests

alluredir = ../../reports/allure-results/meu-projeto

log_cli = true
log_cli_level = INFO
```

### Passo 4: Cliente Específico

```python
# projects/meu-projeto/camada1/servico1/clients/servico1_client.py

from core.api.client import APIClient
import os

class Servico1Client(APIClient):
    """Cliente para Serviço 1"""

    def __init__(self):
        super().__init__(
            base_url=os.getenv("SERVICO1_URL"),
            timeout=30,
            retries=3
        )

        # Adicionar autenticação
        api_key = os.getenv("SERVICO1_API_KEY")
        self.session.headers.update({"X-API-Key": api_key})

    def listar_items(self):
        """GET /items"""
        return self.get("/items")
```

### Passo 5: Feature BDD

```gherkin
# projects/meu-projeto/camada1/servico1/tests/bdd/features/servico1.feature

@camada1 @servico1 @smoke
Feature: Serviço 1

  Scenario: Listar items
    When eu listo os items do serviço 1
    Then deve retornar status 200
    And deve retornar uma lista não vazia
```

### Passo 6: README do Projeto

```markdown
# Projeto: Meu Projeto

## Quick Start

1. Configurar: `cp .env.meu-projeto.example .env.meu-projeto`
2. Executar: `pytest projects/meu-projeto/`

## Estrutura

- `camada1/servico1/` - Serviço 1
- `camada2/` - Camada 2

## Markers

- `@camada1` - Testes da camada 1
- `@servico1` - Testes do serviço 1
```

---

## 🔧 Executando Testes

### Por Projeto

```bash
# Todos os testes do projeto
pytest projects/meu-projeto/

# Com configuração específica
pytest projects/meu-projeto/ -c projects/meu-projeto/pytest.ini
```

### Por Camada

```bash
# Testes de uma camada específica
pytest projects/meu-projeto/camada1/
pytest projects/meu-projeto/backend/
```

### Por Serviço

```bash
# Testes de um serviço específico
pytest projects/meu-projeto/camada1/servico1/
pytest projects/srs/middleware/email/
```

### Por Marker

```bash
# Smoke tests do projeto
pytest projects/meu-projeto/ -m smoke

# Testes de email do SRS
pytest projects/srs/ -m email

# Middleware crítico
pytest projects/srs/middleware/ -m "middleware and critical"
```

### Relatórios Separados

```bash
# Relatório específico do projeto
pytest projects/srs/ --alluredir=reports/allure-results/srs
allure serve reports/allure-results/srs

# Relatório específico de uma camada
pytest projects/srs/middleware/ --alluredir=reports/allure-results/srs-middleware
```

---

## 📊 Organizando por Camadas

### Padrão Recomendado

#### Camadas Comuns

1. **Middleware**: Serviços intermediários (email, sms, notifications)
2. **Backend**: API REST principal
3. **Frontend**: Interface do usuário (UI)
4. **Integration**: Testes end-to-end

#### Exemplo: Projeto SRS

```
srs/
├── middleware/
│   ├── email/          # Serviço de email
│   ├── sms/            # Serviço de SMS
│   └── notification/   # Serviço de notificações
├── backend/            # API principal
├── frontend/           # Testes UI
└── integration/        # E2E tests
```

### Fixtures por Camada

```python
# projects/srs/middleware/conftest.py

import pytest
from .email.clients.email_client import EmailServiceClient

@pytest.fixture
def email_client():
    """Cliente do serviço de email"""
    return EmailServiceClient()

@pytest.fixture
def sms_client():
    """Cliente do serviço de SMS"""
    from .sms.clients.sms_client import SMSServiceClient
    return SMSServiceClient()
```

```python
# projects/srs/middleware/email/conftest.py

import pytest

@pytest.fixture
def sample_email_data():
    """Dados de exemplo para email"""
    return {
        "to": "test@example.com",
        "subject": "Test Email",
        "body": "This is a test"
    }
```

---

## 🎯 Vantagens da Organização Multi-Projeto

### ✅ Isolamento

- Cada projeto tem suas próprias configurações
- Testes de um projeto não interferem em outro
- Relatórios separados por projeto

### ✅ Reutilização

- **Core compartilhado**: APIClient, BasePage, DatabaseManager
- **Fixtures globais**: Disponíveis em `conftest.py` raiz
- **Helpers**: Validators, data generators

### ✅ Escalabilidade

- Adicionar novos projetos sem modificar os existentes
- Adicionar camadas/serviços de forma modular
- Equipes diferentes podem trabalhar em projetos diferentes

### ✅ Manutenibilidade

- Estrutura clara e previsível
- Fácil encontrar testes de um projeto específico
- Documentação por projeto

---

## 🔗 Compartilhamento de Código

### O que PODE ser compartilhado

✅ **Core framework** (`core/`)
- `APIClient`, `BasePage`, `DatabaseManager`
- Settings management
- Helpers e validators

✅ **Fixtures globais** (`tests/conftest.py`)
- Fixtures comuns a todos os projetos

✅ **Step definitions genéricos** (`tests/bdd/steps/`)
- Steps reutilizáveis (common_steps, api_steps, etc.)

### O que NÃO deve ser compartilhado

❌ **Clientes específicos**
- Cada projeto tem seus próprios clients

❌ **Schemas/Models**
- Específicos por projeto/serviço

❌ **Features BDD**
- Específicas por projeto (mas podem reutilizar steps)

❌ **Configurações (.env, pytest.ini)**
- Cada projeto tem as suas

---

## 📚 Exemplos Práticos

### Exemplo 1: Projeto com Microserviços

```
projects/ecommerce/
├── cart-service/
├── payment-service/
├── shipping-service/
├── user-service/
└── frontend/
```

### Exemplo 2: Projeto Multi-Tenant

```
projects/saas-platform/
├── tenant-a/
├── tenant-b/
├── admin-panel/
└── shared-api/
```

### Exemplo 3: Projeto com Múltiplos Ambientes

```
projects/mobile-app/
├── android/
├── ios/
├── backend-api/
└── web-version/
```

---

## 🛠️ Scripts Utilitários

### Criar Novo Projeto

```bash
# scripts/create_project.sh
PROJECT_NAME=$1
mkdir -p projects/$PROJECT_NAME
cp templates/project-template/* projects/$PROJECT_NAME/
echo "✅ Projeto $PROJECT_NAME criado!"
```

### Executar Todos os Projetos

```bash
# Executar smoke tests de todos os projetos
for project in projects/*/; do
    echo "🧪 Testing $(basename $project)..."
    pytest "$project" -m smoke
done
```

---

## 📊 Boas Práticas

### 1. Nomenclatura Consistente

- Use nomes descritivos para camadas e serviços
- Mantenha padrão: `nome-projeto/camada/servico/`

### 2. Markers Claros

- Use `@camada` + `@servico` + `@tipo`
- Exemplo: `@middleware @email @smoke`

### 3. Documentação

- Cada projeto DEVE ter README.md
- Documente configurações específicas
- Liste markers disponíveis

### 4. Fixtures Organizadas

- Fixtures globais → `tests/conftest.py`
- Fixtures de camada → `projeto/camada/conftest.py`
- Fixtures de serviço → `projeto/camada/servico/conftest.py`

### 5. Relatórios Separados

- Use `alluredir` específico por projeto
- Facilita rastreabilidade

---

## 🎓 Migração de Testes Existentes

Se você já tem testes, pode migrá-los para a estrutura multi-projeto:

### Antes

```
tests/
├── api/
│   ├── test_email.py
│   └── test_sms.py
└── ui/
    └── test_login.py
```

### Depois

```
projects/meu-projeto/
├── middleware/
│   ├── email/tests/functional/test_email.py
│   └── sms/tests/functional/test_sms.py
└── frontend/
    └── tests/functional/test_login.py
```

---

## 📞 Suporte

- Ver [README do Projeto SRS](../../projects/srs/README.md) como exemplo completo
- Ver [docs/INDEX.md](../INDEX.md) para documentação do framework
- Ver [tests/bdd/README.md](../../tests/bdd/README.md) para guia de BDD

---

**Última atualização:** 2025-11-15
**Versão:** 1.0 - Guia inicial de multi-projetos
