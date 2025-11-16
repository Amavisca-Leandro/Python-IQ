# 🔄 Nova Estrutura de Testes - Email Service

## 📊 Mudança de Estrutura

### ❌ Estrutura Anterior (Problemática)

```
tests/
├── bdd/                    # ❌ Metodologia como tipo de teste
│   ├── features/
│   ├── steps/
│   └── test_*.py
└── functional/             # ❌ Tipo de teste real
```

**Problema**: Mistura conceitos diferentes (metodologia vs escopo técnico)

### ✅ Estrutura Nova (Corrigida)

```
tests/
├── integration/            # ✅ Escopo: testes de integração com API real
│   ├── features/          # Gherkin (BDD format)
│   │   ├── api_keys.feature
│   │   ├── templates.feature
│   │   ├── email_sending.feature
│   │   └── email_queue.feature
│   ├── steps/             # Step definitions (BDD implementation)
│   │   ├── email_common_steps.py
│   │   ├── email_api_steps.py
│   │   └── email_assertion_steps.py
│   ├── test_api_keys.py
│   ├── test_templates.py
│   ├── test_email_sending.py
│   ├── test_email_queue.py
│   └── conftest.py
│
├── unit/                   # ✅ Escopo: testes unitários sem dependências externas
│   ├── test_email_client_methods.py
│   └── test_helpers.py
│
└── contract/               # ✅ Escopo: validação de contratos de API
    └── test_api_schema.py
```

## 🎯 Justificativa da Mudança

### Problema com "BDD como Tipo"

**BDD não é um tipo de teste** - é uma **metodologia/abordagem** de desenvolvimento que pode ser aplicada a qualquer escopo de teste:

- ✅ Testes **unitários** escritos em BDD (Gherkin)
- ✅ Testes **de integração** escritos em BDD (Gherkin)
- ✅ Testes **E2E** escritos em BDD (Gherkin)

**BDD é HOW (como escrever)**, não **WHAT (o que testar)**

### Solução: Organização por Escopo Técnico

Agora os testes são organizados por **escopo técnico** (categorias mutuamente exclusivas):

#### 1. **`integration/`** - Testes de Integração
- Testa integração com **API real do Email Service**
- Requer **serviço rodando**
- Valida **comportamento end-to-end** de cada endpoint
- **Formato**: Pode ser Gherkin (`.feature`) OU pytest tradicional (`.py`)

**Exemplos**:
```bash
# BDD/Gherkin format
tests/integration/features/api_keys.feature

# Pytest tradicional format
tests/integration/test_error_handling.py
```

#### 2. **`unit/`** - Testes Unitários
- Testa **lógica interna** sem dependências externas
- **Não faz chamadas HTTP reais** (usa mocks)
- Rápido, isolado, sem side effects
- Valida: parsing, validação, transformação de dados

**Exemplos**:
```python
# tests/unit/test_email_client_methods.py
def test_build_headers_includes_api_key():
    client = EmailServiceClient(base_url="...", api_key="test")
    headers = client._build_headers()
    assert "x-api-key" in headers
```

#### 3. **`contract/`** - Testes de Contrato
- Valida **schemas de request/response**
- Detecta **breaking changes** na API
- Garante **backward compatibility**
- Usa JSON Schema validation

**Exemplos**:
```python
# tests/contract/test_api_schema.py
def test_list_api_keys_response_schema():
    expected_schema = {...}
    validate(instance=response.json(), schema=expected_schema)
```

## 📋 Comparação de Conceitos

| Conceito | O que é? | Onde fica? |
|----------|----------|------------|
| **BDD** | Metodologia/formato (Gherkin) | Dentro de qualquer escopo (`integration/features/`) |
| **Unit** | Escopo técnico (sem deps externas) | `tests/unit/` |
| **Integration** | Escopo técnico (com API real) | `tests/integration/` |
| **Contract** | Escopo técnico (schema validation) | `tests/contract/` |
| **E2E** | Escopo técnico (fluxo completo) | `tests/e2e/` ou `projects/srs/integration/` |

## 🚀 Como Executar os Testes

### Por Escopo (Tipo Técnico)

```bash
# Testes de integração (requer serviço rodando)
pytest projects/srs/middleware/email/tests/integration/ -v

# Testes unitários (rápidos, sem deps)
pytest projects/srs/middleware/email/tests/unit/ -v

# Testes de contrato (validação de schemas)
pytest projects/srs/middleware/email/tests/contract/ -v
```

### Por Formato (BDD vs Pytest)

```bash
# Apenas testes BDD (Gherkin)
pytest projects/srs/middleware/email/tests/integration/ -k "test_" -v

# Apenas testes pytest tradicionais
pytest projects/srs/middleware/email/tests/integration/ --ignore=features/ -v
```

### Por Markers

```bash
# Todos os testes de integração (marker)
pytest -m integration -v

# Todos os testes unitários (marker)
pytest -m unit -v

# Todos os testes de contrato (marker)
pytest -m contract -v

# Testes críticos de qualquer escopo
pytest -m critical -v
```

## 📊 Pirâmide de Testes

A nova estrutura reflete a **pirâmide de testes**:

```
        /\
       /  \       E2E (projects/srs/integration/)
      /    \
     /------\     Integration (tests/integration/)
    /        \
   /          \   Unit (tests/unit/)
  /__________\   Contract (tests/contract/)
```

- **70%**: Testes unitários (`unit/`) - rápidos, isolados
- **20%**: Testes de integração (`integration/`) - médios, com deps
- **10%**: Testes E2E - lentos, fluxo completo

## 🎓 Exemplos Práticos

### Exemplo 1: Teste Unitário vs Integração

**Unitário** (`tests/unit/test_email_client_methods.py`):
```python
@patch('requests.Session.get')
def test_list_api_keys_builds_correct_url(mock_get):
    client = EmailServiceClient(base_url="http://localhost:3000")
    client.list_api_keys(page=2, limit=20)

    # Verifica que URL foi construída corretamente
    called_url = mock_get.call_args[0][0]
    assert "page=2" in called_url
    assert "limit=20" in called_url
```

**Integração** (`tests/integration/features/api_keys.feature`):
```gherkin
Scenario: Listar API keys com paginação
  Given o serviço de Email está disponível
  And eu tenho uma API key válida
  When eu listo as API keys com os parâmetros:
    | parametro | valor |
    | page      | 2     |
    | limit     | 20    |
  Then o status code deve ser 200
  And a resposta deve conter uma lista de API keys
```

### Exemplo 2: BDD em Diferentes Escopos

**BDD para Integration** (`tests/integration/features/`):
```gherkin
Feature: Email Service API Keys Management
  Scenario: Create new API key
    When eu crio uma nova API key
    Then o status code deve ser 201
```

**BDD para E2E** (futuro - `projects/srs/integration/`):
```gherkin
Feature: Complete Email Flow
  Scenario: User registration triggers welcome email
    Given a new user registers
    When the backend creates the user
    Then an email should be queued via Email Service
    And the email should be sent via SMTP
    And the user should receive the email
```

## ✅ Benefícios da Nova Estrutura

1. **Categorias Mutuamente Exclusivas**: Cada teste tem um lugar claro
2. **BDD Coexiste com Pytest**: Ambos formatos convivem no mesmo escopo
3. **Alinhamento com Pirâmide**: Reflete best practices de testing
4. **Execução Granular**: Pode rodar por escopo ou formato
5. **Clareza Conceitual**: Separação clara entre HOW e WHAT
6. **Escalabilidade**: Estrutura cresce de forma organizada

## 📚 Referências

- **Pirâmide de Testes**: [martinfowler.com/bliki/TestPyramid.html](https://martinfowler.com/bliki/TestPyramid.html)
- **BDD vs TDD**: BDD é metodologia, não tipo de teste
- **Contract Testing**: [pact.io](https://pact.io)

---

✅ **Estrutura refatorada com sucesso!**
🎯 **Conceitos alinhados com best practices de testing!**
