# Projeto SRS - Test Automation

Testes automatizados para o projeto SRS, organizados por camadas e serviços.

## 📁 Estrutura do Projeto

```
srs/
├── middleware/              # Camada de Middleware
│   ├── email/              # Serviço de Email
│   ├── sms/                # Serviço de SMS
│   └── notification/       # Serviço de Notificações
├── backend/                # Camada de Backend (API)
├── frontend/               # Camada de Frontend (UI)
└── integration/            # Testes End-to-End
```

## 🚀 Quick Start

### 1. Configuração

```bash
# Copiar arquivo de configuração
cd projects/srs
cp .env.srs.example .env.srs

# Editar com suas credenciais
# vim .env.srs
```

### 2. Executar Testes

```bash
# Executar todos os testes do SRS
pytest projects/srs/

# Executar testes de uma camada específica
pytest projects/srs/middleware/
pytest projects/srs/backend/
pytest projects/srs/frontend/

# Executar testes de um serviço específico
pytest projects/srs/middleware/email/ -m email

# Executar apenas smoke tests
pytest projects/srs/ -m smoke

# Executar com relatório Allure
pytest projects/srs/ --alluredir=reports/allure-results/srs
allure serve reports/allure-results/srs
```

## 🏷️ Markers (Tags)

### Por Camada
- `@middleware` - Testes da camada middleware
- `@backend` - Testes da camada backend
- `@frontend` - Testes da camada frontend
- `@integration` - Testes end-to-end

### Por Serviço Middleware
- `@email` - Testes do serviço de email
- `@sms` - Testes do serviço de SMS
- `@notification` - Testes do serviço de notificações

### Por Tipo
- `@smoke` - Testes críticos (caminho feliz)
- `@regression` - Suite completa de regressão
- `@api` - Testes de API
- `@ui` - Testes de interface
- `@bdd` - Testes BDD com Gherkin

### Por Prioridade
- `@critical` - Prioridade crítica (P0)
- `@high` - Alta prioridade (P1)
- `@medium` - Média prioridade (P2)
- `@low` - Baixa prioridade (P3)

## 📊 Exemplos de Comandos

```bash
# Testes críticos de email
pytest projects/srs/middleware/email/ -m "email and critical"

# Testes de backend excluindo lentos
pytest projects/srs/backend/ -m "backend and not slow"

# Testes BDD de middleware
pytest projects/srs/middleware/ -m bdd

# Executar em paralelo (4 workers)
pytest projects/srs/ -n 4

# Testes de integração E2E
pytest projects/srs/integration/ -m integration
```

## 🔧 Estrutura de Cada Camada

### Middleware (Exemplo: Email)

```
middleware/email/
├── tests/
│   ├── bdd/
│   │   ├── features/           # Arquivos .feature
│   │   └── steps/              # Step definitions
│   └── functional/             # Testes pytest tradicionais
├── clients/
│   └── email_client.py         # Cliente do serviço
├── models/
│   └── email_schemas.py        # Schemas Pydantic
└── conftest.py                 # Fixtures específicas
```

### Backend

```
backend/
├── tests/
│   ├── bdd/
│   └── functional/
├── clients/
│   └── api_client.py           # Cliente da API backend
└── conftest.py
```

### Frontend

```
frontend/
├── tests/
│   ├── bdd/
│   └── functional/
├── pages/                      # Page Objects
│   ├── login_page.py
│   └── dashboard_page.py
└── conftest.py
```

## 📖 Documentação

- **Framework Core**: Ver `/docs/` na raiz do python-iq
- **BDD Guide**: `/tests/bdd/README.md`
- **Allure Reports**: `/docs/ALLURE_GUIDE.md`

## 🔗 Dependências do Core

Este projeto utiliza o framework `python-iq` localizado na raiz:
- `core/api/` - Cliente API genérico
- `core/ui/` - Page Object Model base
- `core/database/` - Database manager
- `core/helpers/` - Utilitários e validators

## 🧪 Criando Novos Testes

### BDD (Recomendado)

1. Criar feature em `<camada>/<servico>/tests/bdd/features/`
2. Criar/reutilizar steps em `<camada>/<servico>/tests/bdd/steps/`
3. Executar: `pytest <camada>/<servico>/tests/bdd/`

### Pytest Tradicional

1. Criar arquivo `test_*.py` em `<camada>/<servico>/tests/functional/`
2. Usar fixtures do `conftest.py`
3. Executar: `pytest <camada>/<servico>/tests/functional/`

## 📊 Relatórios

```bash
# Gerar relatório Allure específico do SRS
pytest projects/srs/ --alluredir=reports/allure-results/srs
allure serve reports/allure-results/srs

# Relatório HTML simples
pytest projects/srs/ --html=reports/srs_report.html
```

## 🤝 Contribuindo

1. Siga a estrutura de camadas/serviços
2. Use markers apropriados
3. Escreva testes BDD quando possível
4. Documente novos clients e schemas
5. Mantenha fixtures reutilizáveis no conftest.py

## 📞 Suporte

- Ver `/docs/troubleshooting/SOLUCAO_ERROS.md`
- Ver documentação do framework na raiz
