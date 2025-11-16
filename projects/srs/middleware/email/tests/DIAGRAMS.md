# 📊 Diagramas Visuais - Estrutura de Testes

## 🔄 Evolução da Estrutura

### Diagrama 1: ANTES vs DEPOIS

```
┌─────────────────────────────────────────────────────────────────┐
│                    ❌ ESTRUTURA ANTERIOR                         │
└─────────────────────────────────────────────────────────────────┘

                        tests/
                          │
                    ┌─────┴─────┐
                    │           │
                  bdd/      functional/
               (Metodologia) (Escopo)
                    │
        ┌───────────┼───────────┐
        │           │           │
    features/    steps/    test_*.py
   (Gherkin)  (Python)   (pytest-bdd)


    ⚠️  PROBLEMA: Mistura HOW (BDD) com WHAT (funcional)
    ⚠️  BDD é metodologia, não tipo de teste!


┌─────────────────────────────────────────────────────────────────┐
│                    ✅ ESTRUTURA CORRIGIDA                        │
└─────────────────────────────────────────────────────────────────┘

                        tests/
                          │
            ┌─────────────┼─────────────┐
            │             │             │
      integration/     unit/       contract/
      (Escopo)       (Escopo)     (Escopo)
            │
    ┌───────┼───────┐
    │       │       │
features/ steps/ test_*.py
(Gherkin) (BDD)  (pytest)
    │
    └─ BDD format DENTRO de integration
       (metodologia aplicada ao escopo)


    ✅ SOLUÇÃO: Organização por escopo técnico
    ✅ BDD pode existir em qualquer escopo!
```

## 🎯 Diagrama 2: BDD como Formato, não Tipo

```
┌──────────────────────────────────────────────────────────────────┐
│         BDD (Behavior-Driven Development)                        │
│         É uma METODOLOGIA/FORMATO, não um TIPO                   │
└──────────────────────────────────────────────────────────────────┘

        Formato/Metodologia (HOW - Como escrever)
                        │
        ┌───────────────┼───────────────┐
        │               │               │
     Gherkin         pytest         unittest
   (.feature)         (.py)           (.py)
        │
        └─ Pode ser aplicado a qualquer escopo ↓

        ┌───────────────────────────────────────┐
        │   Escopo Técnico (WHAT - O que testar)│
        └───────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
      Unit         Integration       E2E
   (isolado)      (API real)    (fluxo completo)


    Exemplo de BDD em diferentes escopos:
    ┌─────────────────────────────────────────────────┐
    │ Unit + BDD:                                     │
    │   Scenario: Validate email format               │
    │     Given an email validator                    │
    │     When I validate "user@example.com"          │
    │     Then it should be valid                     │
    └─────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────┐
    │ Integration + BDD:                              │
    │   Scenario: Create API key via API              │
    │     Given the Email Service is available        │
    │     When I create an API key                    │
    │     Then the status code should be 201          │
    └─────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────┐
    │ E2E + BDD:                                      │
    │   Scenario: User receives welcome email         │
    │     Given a new user registers                  │
    │     When the registration completes             │
    │     Then the user should receive welcome email  │
    └─────────────────────────────────────────────────┘
```

## 📊 Diagrama 3: Pirâmide de Testes

```
┌──────────────────────────────────────────────────────────────────┐
│                    PIRÂMIDE DE TESTES                            │
└──────────────────────────────────────────────────────────────────┘

                          /\
                         /  \
                        / E2E \          ← 10% dos testes
                       /────────\          • Lentos (minutos)
                      /          \         • Fluxo completo
                     / Integration\        • UI + API + DB
                    /──────────────\
                   /                \    ← 20% dos testes
                  /   Integration    \     • Médios (segundos)
                 /                    \    • API real
                /──────────────────────\   • Múltiplos componentes
               /                        \
              /    Unit + Contract       \ ← 70% dos testes
             /                            \  • Rápidos (ms)
            /______________________________\ • Isolados
                                             • Sem dependências


    Mapeamento para nossa estrutura:

    ┌─────────────────────────────────────────────────┐
    │  tests/unit/              ← Base da pirâmide    │
    │  tests/contract/          ← Base da pirâmide    │
    │                                                  │
    │  • Rápidos (< 100ms)                            │
    │  • Não requerem deps externas                   │
    │  • 70% dos testes                               │
    │  • Executar a cada commit                       │
    └─────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────┐
    │  tests/integration/       ← Meio da pirâmide    │
    │                                                  │
    │  • Médios (1-5s)                                │
    │  • Requerem Email Service rodando               │
    │  • 20% dos testes                               │
    │  • Executar antes de push                       │
    └─────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────┐
    │  projects/srs/integration/ ← Topo da pirâmide   │
    │  (E2E cross-service)                            │
    │                                                  │
    │  • Lentos (10-60s)                              │
    │  • Requerem todos serviços (email, sms, db, ui) │
    │  • 10% dos testes                               │
    │  • Executar em pipeline CI/CD                   │
    └─────────────────────────────────────────────────┘
```

## 🔀 Diagrama 4: Fluxo de Execução

```
┌──────────────────────────────────────────────────────────────────┐
│              FLUXO DE EXECUÇÃO DE TESTES                         │
└──────────────────────────────────────────────────────────────────┘

    Developer Workflow:
    ──────────────────

    ┌──────────┐
    │  Commit  │
    └────┬─────┘
         │
         ├─→ pytest tests/unit/           ← Rápido (5s)
         │   ✓ Testes unitários
         │   ✓ Sem deps externas
         │
         ├─→ pytest tests/contract/       ← Rápido (10s)
         │   ✓ Schema validation
         │   ✓ Smoke tests
         │
    ┌────┴─────┐
    │   Push   │
    └────┬─────┘
         │
         ├─→ pytest tests/integration/    ← Médio (2min)
         │   ✓ Testes com API real
         │   ✓ Cenários críticos
         │
    ┌────┴──────┐
    │    PR     │
    └────┬──────┘
         │
         └─→ Full regression suite        ← Lento (10min)
             ✓ Todos os testes
             ✓ Múltiplos ambientes
             ✓ E2E cross-service


    CI/CD Pipeline:
    ───────────────

    ┌────────────────────────────────────────────────┐
    │  Stage 1: Unit + Contract (parallel)           │
    │  ├─ pytest tests/unit/ -n 4                    │
    │  └─ pytest tests/contract/                     │
    │  Duration: 15 segundos                         │
    │  ✓ Fast feedback                               │
    └─────────────┬──────────────────────────────────┘
                  │
                  │ PASS ✓
                  ↓
    ┌────────────────────────────────────────────────┐
    │  Stage 2: Integration (parallel browsers)      │
    │  ├─ pytest tests/integration/ -n 2             │
    │  └─ Email Service container started            │
    │  Duration: 2 minutos                           │
    │  ✓ API validation                              │
    └─────────────┬──────────────────────────────────┘
                  │
                  │ PASS ✓
                  ↓
    ┌────────────────────────────────────────────────┐
    │  Stage 3: E2E (sequential)                     │
    │  └─ pytest projects/srs/integration/           │
    │  Duration: 10 minutos                          │
    │  ✓ Full system validation                      │
    └────────────────────────────────────────────────┘
```

## 🗂️ Diagrama 5: Organização de Arquivos

```
┌──────────────────────────────────────────────────────────────────┐
│           ORGANIZAÇÃO DETALHADA DE ARQUIVOS                      │
└──────────────────────────────────────────────────────────────────┘

projects/srs/middleware/email/
│
├── clients/
│   └── email_client.py         ← EmailServiceClient
│
├── models/
│   └── email_schemas.py        ← Pydantic models
│
└── tests/                      ← AQUI!
    │
    ├── integration/            ← Testes com API real
    │   │
    │   ├── features/           ← Gherkin scenarios
    │   │   ├── __init__.py
    │   │   ├── api_keys.feature       (10 scenarios)
    │   │   ├── templates.feature      (10 scenarios)
    │   │   ├── email_sending.feature  (11 scenarios)
    │   │   └── email_queue.feature    (15 scenarios)
    │   │
    │   ├── steps/              ← BDD step definitions
    │   │   ├── __init__.py
    │   │   ├── email_common_steps.py     (Given)
    │   │   ├── email_api_steps.py        (When)
    │   │   └── email_assertion_steps.py  (Then)
    │   │
    │   ├── test_api_keys.py          ← pytest-bdd runner
    │   ├── test_templates.py         ← pytest-bdd runner
    │   ├── test_email_sending.py     ← pytest-bdd runner
    │   ├── test_email_queue.py       ← pytest-bdd runner
    │   ├── conftest.py               ← Fixtures (bdd_context, client)
    │   └── __init__.py
    │
    ├── unit/                   ← Testes sem deps externas
    │   ├── __init__.py
    │   ├── test_email_client_methods.py  ← Client internals
    │   └── test_helpers.py               ← Utility functions
    │
    ├── contract/               ← Validação de schemas
    │   ├── __init__.py
    │   └── test_api_schema.py            ← JSON Schema validation
    │
    ├── __init__.py
    ├── README.md               ← Guia de uso
    ├── NOVA_ESTRUTURA.md       ← Explicação da refatoração
    └── DIAGRAMS.md             ← Este arquivo


    Métricas:
    ─────────
    • 46 cenários BDD (integration)
    • 2 arquivos unit tests
    • 1 arquivo contract tests
    • 23 endpoints cobertos
    • 4 features Gherkin
    • 3 step definition files
```

## 🎭 Diagrama 6: Responsabilidades de Cada Tipo

```
┌──────────────────────────────────────────────────────────────────┐
│          RESPONSABILIDADES POR TIPO DE TESTE                     │
└──────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  UNIT TESTS (tests/unit/)                                   │
├─────────────────────────────────────────────────────────────┤
│  Responsabilidades:                                         │
│  ✓ Validar lógica interna de métodos                        │
│  ✓ Testar parsers e builders                               │
│  ✓ Validar error handling                                   │
│  ✓ Testar retry logic                                       │
│  ✓ Validar transformações de dados                          │
│                                                             │
│  Não testa:                                                 │
│  ✗ Integração com API externa                              │
│  ✗ Comportamento end-to-end                                │
│  ✗ Schemas de request/response                             │
│                                                             │
│  Exemplo:                                                   │
│  def test_build_query_params():                            │
│      params = client._build_query_params(                  │
│          page=1, limit=10, sort=None                       │
│      )                                                      │
│      assert "page=1" in params                             │
│      assert "sort" not in params  # None foi filtrado      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  INTEGRATION TESTS (tests/integration/)                     │
├─────────────────────────────────────────────────────────────┤
│  Responsabilidades:                                         │
│  ✓ Validar comunicação com API real                        │
│  ✓ Testar fluxos completos (CRUD)                          │
│  ✓ Validar status codes e responses                        │
│  ✓ Testar autenticação/autorização                         │
│  ✓ Validar comportamento em cenários reais                 │
│                                                             │
│  Requer:                                                    │
│  • Email Service rodando                                   │
│  • API key válida                                          │
│  • Conectividade de rede                                   │
│                                                             │
│  Exemplo (BDD):                                            │
│  Scenario: Create API key                                  │
│    Given the Email Service is available                    │
│    When I create a new API key                             │
│    Then the status code should be 201                      │
│    And the API key should be returned                      │
│                                                             │
│  Exemplo (pytest):                                         │
│  def test_create_api_key_returns_201():                    │
│      response = client.create_api_key(...)                 │
│      assert response.status_code == 201                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  CONTRACT TESTS (tests/contract/)                          │
├─────────────────────────────────────────────────────────────┤
│  Responsabilidades:                                         │
│  ✓ Validar schemas de request/response                     │
│  ✓ Detectar breaking changes                               │
│  ✓ Garantir backward compatibility                         │
│  ✓ Validar tipos de dados                                  │
│  ✓ Verificar campos obrigatórios                           │
│                                                             │
│  Não testa:                                                 │
│  ✗ Lógica de negócio                                       │
│  ✗ Fluxos completos                                        │
│  ✗ Performance                                             │
│                                                             │
│  Exemplo:                                                   │
│  def test_api_key_schema():                                │
│      schema = {                                            │
│          "type": "object",                                 │
│          "required": ["id", "key", "name"]                 │
│      }                                                      │
│      response = client.get_api_key(id)                     │
│      validate(response.json(), schema)                     │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Diagrama 7: Decisão de Onde Colocar Testes

```
┌──────────────────────────────────────────────────────────────────┐
│              ÁRVORE DE DECISÃO: ONDE COLOCAR TESTE?              │
└──────────────────────────────────────────────────────────────────┘

                     Novo Teste
                         │
                         │
            ┌────────────┴────────────┐
            │                         │
      Precisa de API real?         Não
            │                         │
           Sim                        │
            │                         │
            ↓                         ↓
    ┌───────────────┐         ┌──────────────┐
    │ Integration   │         │ Testa schema?│
    │ tests/        │         └──────┬───────┘
    │ integration/  │                │
    └───────────────┘          ┌─────┴─────┐
            │                  │           │
            │                 Sim         Não
            │                  │           │
    ┌───────┴────────┐         ↓           ↓
    │                │   ┌──────────┐  ┌────────┐
    │  Formato?      │   │ Contract │  │  Unit  │
    │                │   │ tests/   │  │ tests/ │
    └───┬────────┬───┘   │contract/ │  │ unit/  │
        │        │       └──────────┘  └────────┘
       BDD     Pytest
        │        │
        ↓        ↓
    features/ test_*.py
    (Gherkin)


    Exemplos práticos:
    ──────────────────

    ❓ "Testar criação de API key via endpoint POST"
       → Integration (precisa de API real)
       → Formato: BDD ou pytest (sua escolha)
       → tests/integration/features/api_keys.feature

    ❓ "Testar parser de data ISO 8601"
       → Unit (não precisa de API)
       → tests/unit/test_helpers.py

    ❓ "Validar schema de response de lista de templates"
       → Contract (validação de schema)
       → tests/contract/test_api_schema.py

    ❓ "Testar retry logic quando API retorna 503"
       → Unit (pode mockar response)
       → tests/unit/test_email_client_methods.py

    ❓ "Testar fluxo: criar template → enviar email → verificar status"
       → Integration (fluxo completo)
       → tests/integration/features/email_sending.feature
```

## 📈 Diagrama 8: Crescimento da Suite

```
┌──────────────────────────────────────────────────────────────────┐
│              COMO A SUITE CRESCE AO LONGO DO TEMPO               │
└──────────────────────────────────────────────────────────────────┘

    Sprint 1: Setup inicial
    ───────────────────────
    tests/
    ├── integration/
    │   └── test_api_keys.py     (10 scenarios)
    └── unit/
        └── test_client.py       (5 tests)

    Total: 15 testes


    Sprint 2: Adicionar Templates
    ──────────────────────────────
    tests/
    ├── integration/
    │   ├── test_api_keys.py     (10 scenarios)
    │   └── test_templates.py    (10 scenarios) ← NOVO
    ├── unit/
    │   └── test_client.py       (8 tests)      ← +3
    └── contract/
        └── test_schema.py       (5 tests)      ← NOVO

    Total: 33 testes (+18)


    Sprint 3: Email Sending + Queue
    ────────────────────────────────
    tests/
    ├── integration/
    │   ├── test_api_keys.py        (10 scenarios)
    │   ├── test_templates.py       (10 scenarios)
    │   ├── test_email_sending.py   (11 scenarios) ← NOVO
    │   └── test_email_queue.py     (15 scenarios) ← NOVO
    ├── unit/
    │   ├── test_client.py          (12 tests)     ← +4
    │   └── test_helpers.py         (8 tests)      ← NOVO
    └── contract/
        └── test_schema.py          (12 tests)     ← +7

    Total: 78 testes (+45)


    Sprint 4+: Expansão contínua
    ────────────────────────────
    tests/
    ├── integration/
    │   ├── features/               (46 scenarios)
    │   ├── test_error_handling.py  (15 tests)     ← pytest tradicional
    │   └── test_rate_limiting.py   (8 tests)      ← pytest tradicional
    ├── unit/
    │   ├── test_client.py          (20 tests)
    │   ├── test_helpers.py         (15 tests)
    │   ├── test_validators.py      (12 tests)     ← NOVO
    │   └── test_parsers.py         (10 tests)     ← NOVO
    ├── contract/
    │   └── test_schema.py          (20 tests)
    └── performance/                               ← NOVO
        └── test_load.py            (5 tests)

    Total: 151 testes (+73)


    Distribuição final (Pirâmide):
    ───────────────────────────────
    Unit:        57 tests  (38%)  ← Base da pirâmide
    Contract:    20 tests  (13%)  ← Base da pirâmide
    Integration: 69 tests  (46%)  ← Meio da pirâmide
    Performance:  5 tests  (3%)   ← Topo da pirâmide

    ✓ Estrutura mantém organização
    ✓ Fácil localizar e adicionar testes
    ✓ Escala de forma sustentável
```

---

## 🎯 Resumo dos Diagramas

1. **Evolução** - ANTES vs DEPOIS
2. **BDD como Formato** - HOW vs WHAT
3. **Pirâmide** - Distribuição de testes
4. **Fluxo de Execução** - Developer workflow + CI/CD
5. **Organização de Arquivos** - Estrutura detalhada
6. **Responsabilidades** - O que cada tipo testa
7. **Árvore de Decisão** - Onde colocar novos testes
8. **Crescimento** - Como a suite escala

---

✅ **Estrutura visual completa para facilitar entendimento!**
📊 **Diagramas cobrem todos os aspectos da organização!**
