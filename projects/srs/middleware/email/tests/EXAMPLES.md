# 📚 Exemplos Práticos - Testes por Escopo

## 🎯 Objetivo

Este documento mostra **exemplos práticos** de como escrever testes em cada escopo (integration, unit, contract), demonstrando a diferença entre eles.

---

## 📋 Cenário de Teste: Criação de API Key

Vamos usar o **mesmo cenário** (criar API key) e mostrar como ele seria testado em cada escopo.

### Requisito de Negócio

> Como desenvolvedor, quero criar uma API key via endpoint POST /api/v1/api-keys para poder autenticar minhas requisições no Email Service.

---

## 1️⃣ Integration Test (API Real)

### Formato BDD (Gherkin)

**Localização**: `tests/integration/features/api_keys.feature`

```gherkin
Feature: API Keys Management
  Como desenvolvedor
  Quero gerenciar API keys
  Para autenticar minhas requisições

  Background:
    Given o serviço de Email está disponível
    And eu tenho uma API key válida

  Scenario: Criar API key com sucesso
    Given eu tenho os dados da API key:
      | campo        | valor                |
      | name         | My Test API Key      |
      | tier         | premium              |
      | expirationAt | 2025-12-31T23:59:59Z |
    When eu crio uma nova API key
    Then o status code deve ser 201
    And a resposta deve conter o campo "id"
    And a resposta deve conter o campo "key"
    And o campo "name" deve ser "My Test API Key"
    And o campo "tier" deve ser "premium"
    And o campo "isActive" deve ser "true"

  Scenario: Criar API key sem nome retorna erro 400
    Given eu tenho os dados da API key:
      | campo | valor   |
      | tier  | premium |
    When eu tento criar a API key
    Then o status code deve ser 400
    And a resposta deve conter uma mensagem de erro
    And a mensagem de erro deve conter "name is required"
```

**Step Implementation**: `tests/integration/steps/email_api_steps.py`

```python
@when('eu crio uma nova API key')
def criar_api_key(bdd_context, email_service_client):
    """Criar uma nova API key via API real."""
    data = bdd_context.api_key_data

    # Faz chamada HTTP real para o serviço
    response_data = email_service_client.create_api_key(
        name=data['name'],
        expiration_at=data.get('expirationAt'),
        tier=data.get('tier', 'premium'),
        is_internal=data.get('isInternal', False)
    )

    bdd_context.response_data = response_data
    bdd_context.status_code = 201
```

### Formato Pytest Tradicional

**Localização**: `tests/integration/test_api_keys_crud.py`

```python
import pytest

@pytest.mark.integration
@pytest.mark.api_keys
@pytest.mark.smoke
def test_create_api_key_returns_201(email_service_client):
    """Should create API key and return 201."""
    # Arrange
    api_key_data = {
        "name": "My Test API Key",
        "tier": "premium",
        "expirationAt": "2025-12-31T23:59:59Z"
    }

    # Act
    response = email_service_client.create_api_key(**api_key_data)

    # Assert
    assert response["id"] is not None
    assert response["key"] is not None
    assert response["name"] == "My Test API Key"
    assert response["tier"] == "premium"
    assert response["isActive"] is True


@pytest.mark.integration
@pytest.mark.api_keys
@pytest.mark.negative
def test_create_api_key_without_name_returns_400(email_service_client):
    """Should return 400 when name is missing."""
    # Arrange
    api_key_data = {
        "tier": "premium"
        # name is missing
    }

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        email_service_client.create_api_key(**api_key_data)

    assert "400" in str(exc_info.value)
    assert "name is required" in str(exc_info.value).lower()
```

**Características**:
- ✅ Faz chamadas HTTP **reais**
- ✅ Requer Email Service **rodando**
- ✅ Valida comportamento **end-to-end**
- ✅ Tempo: 1-5 segundos por teste
- ✅ Usado para: Validar integração real

---

## 2️⃣ Unit Test (Sem Deps Externas)

**Localização**: `tests/unit/test_api_key_creation.py`

```python
import pytest
from unittest.mock import Mock, patch
from projects.srs.middleware.email.clients.email_client import EmailServiceClient


@pytest.mark.unit
@pytest.mark.api_keys
class TestAPIKeyCreation:
    """Unit tests for API key creation logic."""

    @pytest.fixture
    def client(self):
        """Create client instance for testing."""
        return EmailServiceClient(
            base_url="http://localhost:3000",
            api_key="test-key"
        )

    def test_build_create_api_key_payload(self, client):
        """Should build correct payload for create API key request."""
        # Arrange
        name = "My Test API Key"
        tier = "premium"
        expiration = "2025-12-31T23:59:59Z"

        # Act
        payload = client._build_api_key_payload(
            name=name,
            tier=tier,
            expiration_at=expiration,
            is_internal=False
        )

        # Assert
        assert payload["name"] == name
        assert payload["tier"] == tier
        assert payload["expirationAt"] == expiration
        assert payload["isInternal"] is False

    def test_build_create_api_key_payload_filters_none_values(self, client):
        """Should filter out None values from payload."""
        # Act
        payload = client._build_api_key_payload(
            name="Test Key",
            tier=None,  # Should be filtered out
            expiration_at=None,  # Should be filtered out
            is_internal=False
        )

        # Assert
        assert "name" in payload
        assert "tier" not in payload  # Filtered
        assert "expirationAt" not in payload  # Filtered
        assert "isInternal" in payload

    @patch('requests.Session.post')
    def test_create_api_key_makes_post_request(self, mock_post, client):
        """Should make POST request to correct endpoint."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "123",
            "key": "sk_test_abc",
            "name": "Test Key"
        }
        mock_post.return_value = mock_response

        # Act
        result = client.create_api_key(name="Test Key", tier="premium")

        # Assert
        mock_post.assert_called_once()
        called_url = mock_post.call_args[0][0]
        assert "/api/v1/api-keys" in called_url
        assert result["id"] == "123"

    def test_validate_api_key_name_min_length(self, client):
        """Should validate API key name minimum length."""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            client._validate_api_key_name("ab")  # Too short (min 3)

        assert "minimum length" in str(exc_info.value).lower()

    def test_validate_api_key_name_max_length(self, client):
        """Should validate API key name maximum length."""
        # Arrange
        long_name = "a" * 101  # Max is 100

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            client._validate_api_key_name(long_name)

        assert "maximum length" in str(exc_info.value).lower()

    def test_validate_api_key_tier_valid_values(self, client):
        """Should validate API key tier is one of allowed values."""
        # Valid tiers
        assert client._validate_tier("free") is True
        assert client._validate_tier("premium") is True
        assert client._validate_tier("enterprise") is True

        # Invalid tier
        with pytest.raises(ValueError) as exc_info:
            client._validate_tier("invalid")

        assert "tier must be one of" in str(exc_info.value).lower()
```

**Características**:
- ✅ **Não faz** chamadas HTTP reais (usa mocks)
- ✅ **Não requer** Email Service rodando
- ✅ Testa **lógica interna** do client
- ✅ Tempo: 10-50 ms por teste
- ✅ Usado para: Validar lógica de código

---

## 3️⃣ Contract Test (Validação de Schema)

**Localização**: `tests/contract/test_api_key_schema.py`

```python
import pytest
import requests
from jsonschema import validate, ValidationError


@pytest.mark.contract
@pytest.mark.api_keys
class TestAPIKeySchemas:
    """Contract tests for API Key schemas."""

    @pytest.fixture
    def base_url(self):
        """Get base URL from environment."""
        return "http://localhost:3000"

    @pytest.fixture
    def api_key(self):
        """Get API key from environment."""
        return "test-api-key"

    def test_create_api_key_request_schema(self):
        """Should validate create API key request schema."""
        # Define expected schema
        request_schema = {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {
                    "type": "string",
                    "minLength": 3,
                    "maxLength": 100
                },
                "tier": {
                    "type": "string",
                    "enum": ["free", "premium", "enterprise"]
                },
                "expirationAt": {
                    "type": ["string", "null"],
                    "format": "date-time"
                },
                "isInternal": {
                    "type": "boolean"
                }
            },
            "additionalProperties": False
        }

        # Valid payload examples
        valid_payloads = [
            {"name": "Test Key"},
            {"name": "Test Key", "tier": "premium"},
            {"name": "Test Key", "tier": "premium", "expirationAt": "2025-12-31T23:59:59Z"},
            {"name": "Test Key", "isInternal": True}
        ]

        # Validate each payload
        for payload in valid_payloads:
            try:
                validate(instance=payload, schema=request_schema)
            except ValidationError as e:
                pytest.fail(f"Valid payload failed validation: {e.message}")

    def test_create_api_key_response_schema(self, base_url, api_key):
        """Should validate create API key response schema."""
        # Define expected response schema
        response_schema = {
            "type": "object",
            "required": ["id", "key", "name", "tier", "isActive", "createdAt"],
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uuid"
                },
                "key": {
                    "type": "string",
                    "pattern": "^sk_(test|live)_[a-zA-Z0-9]+$"
                },
                "name": {
                    "type": "string"
                },
                "tier": {
                    "type": "string",
                    "enum": ["free", "premium", "enterprise"]
                },
                "isActive": {
                    "type": "boolean"
                },
                "isInternal": {
                    "type": "boolean"
                },
                "expirationAt": {
                    "type": ["string", "null"],
                    "format": "date-time"
                },
                "createdAt": {
                    "type": "string",
                    "format": "date-time"
                },
                "updatedAt": {
                    "type": "string",
                    "format": "date-time"
                }
            }
        }

        # Make actual API call
        response = requests.post(
            f"{base_url}/api/v1/api-keys",
            headers={"x-api-key": api_key},
            json={"name": "Schema Test Key", "tier": "premium"},
            timeout=10
        )

        # Validate response schema
        try:
            validate(instance=response.json(), schema=response_schema)
        except ValidationError as e:
            pytest.fail(f"Response schema validation failed: {e.message}")

    def test_api_key_backward_compatibility(self):
        """Should ensure backward compatibility of API key schema."""
        # Required fields that must ALWAYS be present
        # (never remove these without major version bump)
        required_fields = ["id", "key", "name", "isActive", "createdAt"]

        # Enum values that must remain stable
        tier_values = ["free", "premium", "enterprise"]

        # These fields should never be removed or renamed
        stable_fields = {
            "id": "string",
            "key": "string",
            "name": "string",
            "tier": "string",
            "isActive": "boolean",
            "isInternal": "boolean",
            "expirationAt": "string or null",
            "createdAt": "string",
            "updatedAt": "string"
        }

        # Assertions to prevent breaking changes
        assert len(required_fields) == 5
        assert len(tier_values) == 3
        assert len(stable_fields) == 9

    def test_error_response_schema(self):
        """Should validate error response schema."""
        error_schema = {
            "type": "object",
            "required": ["error", "message", "statusCode"],
            "properties": {
                "error": {"type": "string"},
                "message": {"type": "string"},
                "statusCode": {"type": "integer"},
                "details": {
                    "type": "object",
                    "properties": {
                        "field": {"type": "string"},
                        "reason": {"type": "string"}
                    }
                }
            }
        }

        # Example error responses
        error_examples = [
            {
                "error": "Bad Request",
                "message": "name is required",
                "statusCode": 400
            },
            {
                "error": "Validation Error",
                "message": "Invalid tier",
                "statusCode": 400,
                "details": {
                    "field": "tier",
                    "reason": "Must be one of: free, premium, enterprise"
                }
            }
        ]

        # Validate each error example
        for error in error_examples:
            try:
                validate(instance=error, schema=error_schema)
            except ValidationError as e:
                pytest.fail(f"Error response schema validation failed: {e.message}")
```

**Características**:
- ✅ Valida **estrutura** de request/response
- ✅ Detecta **breaking changes**
- ✅ Garante **backward compatibility**
- ✅ Tempo: 100-500 ms por teste
- ✅ Usado para: Prevenir mudanças incompatíveis

---

## 📊 Comparação Lado a Lado

| Aspecto | Integration | Unit | Contract |
|---------|-------------|------|----------|
| **Faz chamada HTTP real** | ✅ Sim | ❌ Não (mock) | ✅ Sim |
| **Requer serviço rodando** | ✅ Sim | ❌ Não | ✅ Sim |
| **Velocidade** | 1-5s | 10-50ms | 100-500ms |
| **O que testa** | Comportamento completo | Lógica interna | Estrutura de dados |
| **Quando falha** | API quebrada, bug de integração | Lógica errada, validação incorreta | Schema mudou, breaking change |
| **Formato** | BDD ou pytest | Pytest apenas | Pytest apenas |
| **Usa mocks** | ❌ Não | ✅ Sim (muito) | ❌ Não |
| **Side effects** | ✅ Sim (cria dados) | ❌ Não | ✅ Sim (pode criar) |
| **Exemplo de falha** | "404 Not Found" | "Expected True, got False" | "Missing required field 'id'" |

---

## 🎯 Quando Usar Cada Tipo

### Use Integration Test quando:

✅ Validar **fluxo completo** de uma funcionalidade
✅ Testar **integração real** entre componentes
✅ Verificar **comportamento end-to-end**
✅ Validar **cenários de negócio**
✅ Documentar **requisitos** com Gherkin

**Exemplo**: "Quando eu crio uma API key, ela deve ser retornada com ID único e ficar ativa"

### Use Unit Test quando:

✅ Testar **lógica interna** de métodos
✅ Validar **transformações de dados**
✅ Testar **edge cases** complexos
✅ Verificar **error handling**
✅ Garantir **cobertura de código**

**Exemplo**: "O método _build_payload deve filtrar valores None do dicionário"

### Use Contract Test quando:

✅ Validar **schemas** de API
✅ Detectar **breaking changes**
✅ Garantir **backward compatibility**
✅ Documentar **contratos** de API
✅ Validar **versionamento**

**Exemplo**: "O campo 'id' deve sempre estar presente no response de criação de API key"

---

## 🚀 Exemplo Completo: Feature Completa

Vamos implementar uma feature completa usando os 3 tipos de teste:

### Requisito

> Implementar criação de API key com validação de nome (3-100 caracteres) e tier (free, premium, enterprise)

### 1. Unit Tests (TDD - escrever primeiro)

```python
# tests/unit/test_api_key_validation.py

def test_validate_name_min_length():
    assert validate_name("ab") == False  # Too short
    assert validate_name("abc") == True  # OK

def test_validate_name_max_length():
    assert validate_name("a" * 100) == True  # OK
    assert validate_name("a" * 101) == False  # Too long

def test_validate_tier():
    assert validate_tier("free") == True
    assert validate_tier("premium") == True
    assert validate_tier("enterprise") == True
    assert validate_tier("invalid") == False
```

### 2. Contract Tests (schema primeiro)

```python
# tests/contract/test_api_key_contract.py

def test_create_request_schema():
    schema = {
        "required": ["name"],
        "properties": {
            "name": {"minLength": 3, "maxLength": 100},
            "tier": {"enum": ["free", "premium", "enterprise"]}
        }
    }
    # Validar payloads contra schema
```

### 3. Integration Tests (BDD - por último)

```gherkin
# tests/integration/features/api_keys.feature

Scenario: Criar API key com nome válido
  When eu crio uma API key com nome "Valid Name"
  Then deve retornar status 201

Scenario: Criar API key com nome curto
  When eu crio uma API key com nome "ab"
  Then deve retornar status 400
  And a mensagem deve ser "name must be at least 3 characters"
```

---

## 📚 Recursos Adicionais

- **Estrutura Completa**: [README.md](./README.md)
- **Diagramas Visuais**: [DIAGRAMS.md](./DIAGRAMS.md)
- **Guia de Migração**: [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md)

---

✅ **Exemplos práticos demonstram claramente a diferença entre tipos!**
🎯 **Cada tipo de teste tem seu propósito e momento certo de uso!**
