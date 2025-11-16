# 🧪 Email Service - Test Suite

## 📂 Estrutura de Testes

```
tests/
├── integration/           # Testes de integração com API real
│   ├── features/          # ├─ Gherkin/BDD scenarios (.feature)
│   │   ├── api_keys.feature
│   │   ├── templates.feature
│   │   ├── email_sending.feature
│   │   └── email_queue.feature
│   ├── steps/             # ├─ BDD step definitions
│   │   ├── email_common_steps.py      (Given)
│   │   ├── email_api_steps.py         (When)
│   │   └── email_assertion_steps.py   (Then)
│   ├── test_api_keys.py
│   ├── test_templates.py
│   ├── test_email_sending.py
│   ├── test_email_queue.py
│   └── conftest.py
│
├── unit/                  # Testes unitários (sem deps externas)
│   ├── test_email_client_methods.py
│   └── test_helpers.py
│
├── contract/              # Validação de schemas/contratos de API
│   └── test_api_schema.py
│
└── functional/            # (legacy - pode ser removido futuramente)
```

## 🎯 Tipos de Teste

### 1️⃣ Integration Tests (`integration/`)

**O que é**: Testa integração com a **API real** do Email Service

**Quando usar**:
- Validar comportamento end-to-end de endpoints
- Testar fluxos completos (criar → listar → atualizar → deletar)
- Verificar integração entre componentes

**Requisitos**:
- ✅ Email Service rodando
- ✅ API key válida
- ✅ Conectividade de rede

**Formatos suportados**:
- **Gherkin** (`.feature`): Cenários em linguagem natural
- **Pytest** (`.py`): Testes tradicionais Python

**Exemplo**:
```bash
# Executar todos os testes de integração
pytest tests/integration/ -v

# Executar apenas BDD (Gherkin)
pytest tests/integration/test_api_keys.py -v

# Executar apenas pytest tradicional
pytest tests/integration/test_error_handling.py -v
```

### 2️⃣ Unit Tests (`unit/`)

**O que é**: Testa **lógica interna** sem dependências externas

**Quando usar**:
- Validar métodos privados do client
- Testar parsers, builders, validators
- Verificar error handling interno
- Testar helpers e utilities

**Requisitos**:
- ❌ Não precisa de Email Service rodando
- ❌ Não faz chamadas HTTP reais
- ✅ Usa mocks/stubs

**Exemplo**:
```python
# tests/unit/test_email_client_methods.py
@patch('requests.Session.get')
def test_build_query_params(mock_get):
    client = EmailServiceClient(...)
    params = client._build_query_params(page=1, limit=10)
    assert "page=1" in params
```

### 3️⃣ Contract Tests (`contract/`)

**O que é**: Valida **schemas** de request/response da API

**Quando usar**:
- Detectar breaking changes
- Garantir backward compatibility
- Validar versioning de API
- CI/CD pre-deployment checks

**Requisitos**:
- ✅ Email Service rodando (para alguns testes)
- ✅ JSON Schema definitions

**Exemplo**:
```python
# tests/contract/test_api_schema.py
def test_list_api_keys_response_schema():
    expected_schema = {...}
    response = requests.get(...)
    validate(instance=response.json(), schema=expected_schema)
```

## 🚀 Como Executar

### Por Tipo de Teste

```bash
# Testes de integração (requer serviço)
pytest tests/integration/ -v

# Testes unitários (rápidos)
pytest tests/unit/ -v

# Testes de contrato (validação de schemas)
pytest tests/contract/ -v

# Todos os testes
pytest tests/ -v
```

### Por Markers

```bash
# Smoke tests (críticos)
pytest -m smoke -v

# Por prioridade
pytest -m critical -v
pytest -m high -v

# Por feature
pytest -m api_keys -v
pytest -m templates -v
pytest -m sending -v
pytest -m queue -v

# Testes negativos
pytest -m negative -v

# Testes de segurança
pytest -m security -v
```

### Por Arquivo/Feature

```bash
# Testes de API Keys
pytest tests/integration/test_api_keys.py -v

# Testes de Templates
pytest tests/integration/test_templates.py -v

# Feature específica
pytest tests/integration/features/email_sending.feature -v
```

## 📊 Pirâmide de Testes

```
        /\
       /  \       E2E (projects/srs/integration/)
      /    \      Poucos, lentos, fluxo completo
     /------\
    /        \    Integration (tests/integration/)
   /          \   Médios, API real, cenários completos
  /__________\
  Unit + Contract  Unit (tests/unit/) + Contract (tests/contract/)
  Muitos, rápidos  Testes rápidos, isolados, sem deps
```

**Distribuição recomendada**:
- **70%**: Unit + Contract tests
- **20%**: Integration tests
- **10%**: E2E tests

## 🎓 BDD vs Pytest Tradicional

### Quando usar BDD (Gherkin)?

✅ **Use quando**:
- Colaboração com PO/BA/stakeholders não-técnicos
- Documentação viva de requisitos
- Cenários de aceite de usuário
- Necessidade de exemplos executáveis

**Exemplo**:
```gherkin
Scenario: Criar API key com sucesso
  Given o serviço de Email está disponível
  And eu tenho os dados da API key:
    | campo | valor      |
    | name  | Test Key   |
    | tier  | premium    |
  When eu crio uma nova API key
  Then o status code deve ser 201
  And a API key deve ser retornada
```

### Quando usar Pytest Tradicional?

✅ **Use quando**:
- Testes puramente técnicos
- Edge cases complexos
- Necessidade de loops/condicionais
- Testes parametrizados

**Exemplo**:
```python
@pytest.mark.parametrize("tier", ["free", "premium", "enterprise"])
def test_create_api_key_with_different_tiers(tier):
    response = client.create_api_key(name="Test", tier=tier)
    assert response["tier"] == tier
```

## 🔧 Configuração

### Variáveis de Ambiente

Criar arquivo `.env.srs` na raiz de `projects/srs/`:

```bash
# Email Service Configuration
EMAIL_SERVICE_URL=http://localhost:3000
EMAIL_SERVICE_API_KEY=your-api-key-here
EMAIL_SERVICE_TIMEOUT=30
EMAIL_SERVICE_RETRIES=3
```

### Fixtures Disponíveis

```python
# tests/integration/conftest.py
def email_service_client():
    """Cliente configurado do Email Service."""

def bdd_context():
    """Contexto compartilhado entre steps BDD."""

def sample_api_key_data():
    """Dados de exemplo para criar API key."""
```

## 📈 Cobertura de Testes

### Integration Tests
- ✅ 10 cenários de API Keys
- ✅ 10 cenários de Templates
- ✅ 11 cenários de Email Sending
- ✅ 15 cenários de Email Queue
- **Total: 46 cenários BDD**

### Unit Tests
- ✅ Client initialization
- ✅ Request building
- ✅ Response parsing
- ✅ Error handling
- ✅ Retry logic
- ✅ Data validation

### Contract Tests
- ✅ API Keys schema
- ✅ Templates schema
- ✅ Email Sending schema
- ✅ Email Queue schema
- ✅ Backward compatibility

## 📚 Documentação Adicional

- **Nova Estrutura**: [NOVA_ESTRUTURA.md](./NOVA_ESTRUTURA.md)
- **Setup Completo**: [../SETUP_COMPLETO.md](../SETUP_COMPLETO.md)
- **Importação Insomnia**: [../INSOMNIA_IMPORT_SUMMARY.md](../INSOMNIA_IMPORT_SUMMARY.md)
- **Cliente Email**: [../clients/email_client.py](../clients/email_client.py)

## 🐛 Troubleshooting

### Testes de integração falhando?

1. ✅ Email Service está rodando?
2. ✅ API key está configurada no `.env.srs`?
3. ✅ URL do serviço está correta?
4. ✅ Conectividade de rede OK?

```bash
# Testar conectividade
curl http://localhost:3000/health
```

### Testes unitários falhando?

1. ✅ Dependências instaladas? (`pip install -r requirements.txt`)
2. ✅ Imports corretos?
3. ✅ PYTHONPATH configurado?

```bash
# Executar com verbose
pytest tests/unit/ -vv
```

## 🎯 Próximos Passos

1. [ ] Implementar helper methods faltantes no `email_client.py`
2. [ ] Adicionar testes de performance (`tests/performance/`)
3. [ ] Integrar com CI/CD pipeline
4. [ ] Configurar Allure reporting
5. [ ] Adicionar testes E2E cross-service

---

✅ **Suite completa de testes organizada por escopo técnico!**
🎯 **BDD e Pytest tradicional coexistindo harmoniosamente!**
