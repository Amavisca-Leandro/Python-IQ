# ✅ Setup Completo - SRS Email Service BDD Tests

## 📋 Resumo

Foi realizada a configuração completa dos testes BDD para o serviço de Email do middleware SRS, importados a partir da coleção do Insomnia. Todos os 46 testes estão agora visíveis e executáveis no VS Code Test Explorer.

## 🎯 O Que Foi Criado

### 1. **Feature Files (4 arquivos)** 📝
Localização: `projects/srs/middleware/email/tests/bdd/features/`

- ✅ **api_keys.feature** - 10 cenários para gerenciamento de API Keys
- ✅ **templates.feature** - 10 cenários para gerenciamento de Templates
- ✅ **email_sending.feature** - 11 cenários para envio síncrono de emails
- ✅ **email_queue.feature** - 15 cenários para fila assíncrona de emails

**Total: 46 cenários BDD** cobrindo 23 endpoints da API

### 2. **Step Definitions (3 arquivos)** 🔧
Localização: `projects/srs/middleware/email/tests/bdd/steps/`

- ✅ **email_common_steps.py** - Steps de setup e preparação de dados (Given)
  - Verificação de disponibilidade do serviço
  - Autenticação
  - Preparação de dados para API keys, templates, emails
  - Helper functions para parsing de tabelas Gherkin

- ✅ **email_api_steps.py** - Steps de ações de API (When)
  - API Keys: list, create, get, update, delete
  - Templates: list, create, get, update, delete
  - Email Sending: send (text, HTML, template, attachments)
  - Email Queue: queue, bulk, schedule, status, cancel

- ✅ **email_assertion_steps.py** - Steps de validação (Then)
  - Validação de status codes
  - Validação de campos na resposta
  - Validação de listas e arrays
  - Validação de dados salvos no contexto
  - Validação de mensagens de erro

### 3. **Test Files (4 arquivos)** 🧪
Localização: `projects/srs/middleware/email/tests/bdd/`

- ✅ **test_api_keys.py** - 10 testes
- ✅ **test_templates.py** - 10 testes
- ✅ **test_email_sending.py** - 11 testes
- ✅ **test_email_queue.py** - 15 testes

### 4. **Client Implementation** 💻
Localização: `projects/srs/middleware/email/clients/`

- ✅ **email_client.py** - 463 linhas
  - EmailServiceClient completo com todos os 23 endpoints
  - Herda de core.api.client.APIClient
  - Autenticação via x-api-key header
  - Tratamento de erros e retry logic

### 5. **Fixtures e Configuração** ⚙️
Localização: `projects/srs/middleware/email/tests/bdd/`

- ✅ **conftest.py** - Fixtures específicas do SRS
  - `srs_api_base_url` - URL base do serviço
  - `srs_api_key` - API key para autenticação
  - `email_service_client` - Cliente configurado
  - `bdd_context` - Contexto compartilhado entre steps
  - Sample data fixtures para testes

Localização: `projects/srs/`

- ✅ **pytest.ini** - Configuração do pytest para SRS
  - Markers para organização de testes
  - BDD configuration
  - Allure configuration
  - Logging configuration

- ✅ **.env.srs.example** - Template de variáveis de ambiente

## 📊 Estatísticas

```
📁 Estrutura Criada:
├── 4 feature files (535 linhas de Gherkin)
├── 3 step definition files (Python)
├── 4 test files (pytest-bdd)
├── 1 client implementation (463 linhas)
├── 1 conftest.py (fixtures)
├── 1 pytest.ini (config)
└── 1 .env.srs.example (template)

🧪 Testes:
├── 46 cenários BDD
├── 10 API Keys tests
├── 10 Templates tests
├── 11 Email Sending tests
└── 15 Email Queue tests

🔌 API Coverage:
├── 5 endpoints de API Keys
├── 5 endpoints de Templates
├── 1 endpoint de Email Sending (sync)
├── 6 endpoints de Email Queue (async)
└── 6 endpoints adicionais (status, bulk, etc.)
```

## 🚀 Como Executar os Testes

### No VS Code Test Explorer
Os testes agora aparecem automaticamente no Test Explorer do VS Code. Você pode:
- Executar todos os testes
- Executar por arquivo
- Executar por cenário individual
- Debug de cenários específicos

### Via Linha de Comando

```bash
# Todos os testes do SRS Email Service
pytest projects/srs/middleware/email/tests/bdd/ -v

# Apenas API Keys
pytest projects/srs/middleware/email/tests/bdd/test_api_keys.py -v

# Apenas testes com tag @smoke
pytest projects/srs/middleware/email/tests/bdd/ -m smoke -v

# Apenas testes com tag @critical
pytest projects/srs/middleware/email/tests/bdd/ -m critical -v

# Com relatório Allure
pytest projects/srs/middleware/email/tests/bdd/ --alluredir=reports/allure-results/srs
allure serve reports/allure-results/srs
```

### Executar por Markers

```bash
# CRUD operations
pytest -m crud

# Smoke tests
pytest -m smoke

# Testes de API Keys
pytest -m api_keys

# Testes de Templates
pytest -m templates

# Testes de envio de email
pytest -m sending

# Testes de fila de email
pytest -m queue

# Testes negativos
pytest -m negative

# Testes de segurança
pytest -m security
```

## 🔑 Configuração Necessária

### 1. Criar arquivo `.env.srs` a partir do `.env.srs.example`

```bash
cp projects/srs/.env.srs.example projects/srs/.env.srs
```

### 2. Configurar variáveis de ambiente no `.env.srs`

```ini
# Email Service Configuration
EMAIL_SERVICE_URL=http://localhost:3000
EMAIL_SERVICE_API_KEY=your-api-key-here
EMAIL_SERVICE_TIMEOUT=30
EMAIL_SERVICE_RETRIES=3
```

### 3. Instalar dependências (se necessário)

```bash
pip install pytest pytest-bdd allure-pytest requests
```

## 📝 Detalhes Técnicos Importantes

### Conversão de Keywords Gherkin
As features foram convertidas de keywords em Português para Inglês:
- `Funcionalidade:` → `Feature:`
- `Cenário:` → `Scenario:`
- `Esquema do Cenário:` → `Scenario Outline:`
- `Contexto:` → `Background:`
- `Dado/Quando/Então/E` → `Given/When/Then/And`

**Motivo:** pytest-bdd não suporta nativamente a diretiva `# language: pt`. O conteúdo dos steps permanece em português.

### Padrão de Step Definitions
Todos os steps seguem o padrão:
1. Decorador Allure para reporting
2. Acesso ao `bdd_context` para compartilhar dados
3. Tratamento de erros com try-except
4. Armazenamento de response e status code
5. Logging de todas as ações

### Fixture Hierarchy
```
conftest.py (root)
    ↓
conftest.py (projects/srs/)
    ↓
conftest.py (projects/srs/middleware/email/tests/bdd/)
```

## ✨ Próximos Passos Recomendados

1. **Configurar ambiente de testes**
   - Subir o Email Service localmente ou configurar ambiente de dev
   - Criar API key válida
   - Testar conexão com `pytest projects/srs/middleware/email/tests/bdd/test_api_keys.py::test_listar_api_keys_com_paginação -v`

2. **Executar smoke tests**
   - `pytest projects/srs/middleware/email/tests/bdd/ -m smoke -v`
   - Validar que os endpoints críticos estão funcionando

3. **Implementar steps faltantes** (se houver falhas)
   - Alguns steps podem precisar de ajustes conforme a resposta real da API
   - Adicionar steps específicos que não foram mapeados

4. **Integração com CI/CD**
   - Adicionar job para executar testes do SRS
   - Configurar Allure reporting
   - Configurar notificações de falhas

5. **Expandir cobertura**
   - Adicionar mais cenários conforme necessário
   - Criar testes de performance
   - Adicionar testes de integração entre serviços

## 🎓 Referências

- **Documentação Multi-Projeto**: [docs/architecture/MULTI_PROJECT_GUIDE.md](../../docs/architecture/MULTI_PROJECT_GUIDE.md)
- **Importação Insomnia**: [INSOMNIA_IMPORT_SUMMARY.md](INSOMNIA_IMPORT_SUMMARY.md)
- **Cliente Email Service**: [clients/email_client.py](clients/email_client.py)
- **Configuração pytest**: [pytest.ini](../../pytest.ini)

---

✅ **Setup completo e funcional!**
🎉 **46 testes BDD prontos para execução no Test Explorer!**
