# Design Document - JSONPlaceholder API Tests

## Overview

Este documento descreve o design técnico para implementar testes automatizados da API pública JSONPlaceholder (https://jsonplaceholder.typicode.com/). A solução reutilizará componentes existentes do framework de automação Python já implementado, incluindo o APIClient, validators e sistema de configuração.

A JSONPlaceholder é uma API REST gratuita que fornece endpoints para recursos como posts, comments, users, todos e albums, suportando operações CRUD completas. É ideal para demonstrar capacidades de teste de API real.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Test Layer (pytest)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ test_posts.py│  │test_users.py │  │test_comments │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              JSONPlaceholder Client Layer                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  jsonplaceholder_client.py                            │  │
│  │  - Métodos específicos para cada recurso             │  │
│  │  - Validações de schema                               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Core Framework Components                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  APIClient   │  │  Validators  │  │   Settings   │      │
│  │  (existing)  │  │  (existing)  │  │  (existing)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           JSONPlaceholder API (External)                     │
│         https://jsonplaceholder.typicode.com                 │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

1. **Test Files** → Invocam métodos do JSONPlaceholderClient
2. **JSONPlaceholderClient** → Usa APIClient para fazer requisições HTTP
3. **APIClient** → Executa requisições com retry, logging e timeout
4. **Validators** → Validam respostas, schemas e dados
5. **Settings** → Fornecem configuração centralizada

## Components and Interfaces

### 1. JSONPlaceholderClient

Cliente especializado que encapsula a lógica de interação com a API JSONPlaceholder.

```python
class JSONPlaceholderClient:
    """Cliente para interagir com a API JSONPlaceholder."""
    
    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com"):
        self.client = APIClient(base_url=base_url, timeout=10, retries=2)
    
    # Posts endpoints
    def get_posts(self, user_id: Optional[int] = None) -> requests.Response
    def get_post(self, post_id: int) -> requests.Response
    def create_post(self, data: Dict) -> requests.Response
    def update_post(self, post_id: int, data: Dict) -> requests.Response
    def patch_post(self, post_id: int, data: Dict) -> requests.Response
    def delete_post(self, post_id: int) -> requests.Response
    
    # Users endpoints
    def get_users(self) -> requests.Response
    def get_user(self, user_id: int) -> requests.Response
    def create_user(self, data: Dict) -> requests.Response
    def update_user(self, user_id: int, data: Dict) -> requests.Response
    def delete_user(self, user_id: int) -> requests.Response
    
    # Comments endpoints
    def get_comments(self, post_id: Optional[int] = None) -> requests.Response
    def get_comment(self, comment_id: int) -> requests.Response
    def create_comment(self, data: Dict) -> requests.Response
    
    # Todos endpoints
    def get_todos(self, user_id: Optional[int] = None) -> requests.Response
    def get_todo(self, todo_id: int) -> requests.Response
    def create_todo(self, data: Dict) -> requests.Response
    def update_todo(self, todo_id: int, data: Dict) -> requests.Response
    
    # Albums endpoints
    def get_albums(self, user_id: Optional[int] = None) -> requests.Response
    def get_album(self, album_id: int) -> requests.Response
    
    def close(self):
        """Fecha a sessão HTTP."""
        self.client.close()
```

### 2. Schema Validators

Validadores de schema JSON para cada tipo de recurso.

```python
# Schemas para validação
POST_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title", "body"],
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"}
    }
}

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "username", "email"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "address": {"type": "object"},
        "phone": {"type": "string"},
        "website": {"type": "string"},
        "company": {"type": "object"}
    }
}

COMMENT_SCHEMA = {
    "type": "object",
    "required": ["postId", "id", "name", "email", "body"],
    "properties": {
        "postId": {"type": "integer"},
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"},
        "body": {"type": "string"}
    }
}

TODO_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title", "completed"],
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "completed": {"type": "boolean"}
    }
}

ALBUM_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title"],
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"}
    }
}
```

### 3. Test Fixtures (conftest.py)

Fixtures pytest para setup e teardown dos testes.

```python
import re

@pytest.fixture(scope="session")
def jsonplaceholder_client():
    """Fixture que fornece cliente JSONPlaceholder."""
    client = JSONPlaceholderClient()
    yield client
    client.close()

@pytest.fixture
def sample_post_data():
    """Fixture com dados de exemplo para criar post."""
    return {
        "userId": 1,
        "title": "Test Post Title",
        "body": "Test post body content"
    }

@pytest.fixture
def sample_user_data():
    """Fixture com dados de exemplo para criar usuário."""
    return {
        "name": "Test User",
        "username": "testuser",
        "email": "test@example.com",
        "address": {
            "street": "Test Street",
            "city": "Test City"
        }
    }

@pytest.fixture
def sample_comment_data():
    """Fixture com dados de exemplo para criar comment."""
    return {
        "postId": 1,
        "name": "Test Comment",
        "email": "test@example.com",
        "body": "Test comment body"
    }

@pytest.fixture
def sample_todo_data():
    """Fixture com dados de exemplo para criar todo."""
    return {
        "userId": 1,
        "title": "Test Todo",
        "completed": False
    }

def validate_email_format(email: str) -> bool:
    """Valida formato de email usando regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

## Data Models

### Post Model
```python
{
    "userId": int,      # ID do usuário que criou o post
    "id": int,          # ID único do post
    "title": str,       # Título do post
    "body": str         # Conteúdo do post
}
```

### User Model
```python
{
    "id": int,
    "name": str,
    "username": str,
    "email": str,
    "address": {
        "street": str,
        "suite": str,
        "city": str,
        "zipcode": str,
        "geo": {
            "lat": str,
            "lng": str
        }
    },
    "phone": str,
    "website": str,
    "company": {
        "name": str,
        "catchPhrase": str,
        "bs": str
    }
}
```

### Comment Model
```python
{
    "postId": int,      # ID do post relacionado
    "id": int,          # ID único do comentário
    "name": str,        # Nome/título do comentário
    "email": str,       # Email do autor
    "body": str         # Conteúdo do comentário
}
```

### Todo Model
```python
{
    "userId": int,      # ID do usuário
    "id": int,          # ID único do todo
    "title": str,       # Título da tarefa
    "completed": bool   # Status de conclusão
}
```

### Album Model
```python
{
    "userId": int,      # ID do usuário
    "id": int,          # ID único do álbum
    "title": str        # Título do álbum
}
```

## Error Handling

### Strategy

1. **Network Errors**: APIClient já possui retry automático para falhas de rede
2. **HTTP Errors**: Validar status codes esperados usando `validate_response_status`
3. **Validation Errors**: Usar `ValidationError` customizado para falhas de validação
4. **Timeout Errors**: Configurar timeout apropriado (10s) para API pública

### Error Scenarios

| Scenario | Expected Behavior | Handling |
|----------|------------------|----------|
| 404 Not Found | Recurso não existe | Validar status 404 explicitamente |
| 500 Server Error | Erro no servidor | Retry automático via APIClient |
| Timeout | Requisição demorou muito | Falhar após timeout configurado |
| Invalid JSON | Resposta não é JSON válido | Capturar exceção e falhar teste |
| Schema Mismatch | Dados não correspondem ao schema | ValidationError com detalhes |

## Testing Strategy

### Test Organization

```
tests/jsonplaceholder/
├── conftest.py                 # Fixtures compartilhadas
├── test_posts.py              # Testes de posts
├── test_users.py              # Testes de users
├── test_comments.py           # Testes de comments
├── test_todos.py              # Testes de todos
├── test_albums.py             # Testes de albums
└── test_filters.py            # Testes de query parameters
```

### Test Categories

1. **Smoke Tests** (`@pytest.mark.smoke`)
   - Verificar que endpoints principais estão acessíveis
   - Validar estrutura básica de resposta

2. **CRUD Tests** (`@pytest.mark.crud`)
   - Testar operações GET, POST, PUT, PATCH, DELETE
   - Validar dados retornados

3. **Validation Tests** (`@pytest.mark.validation`)
   - Validar schemas JSON
   - Validar tipos de dados
   - Validar campos obrigatórios

4. **Filter Tests** (`@pytest.mark.filters`)
   - Testar query parameters
   - Validar filtragem de resultados

5. **Performance Tests** (`@pytest.mark.performance`)
   - Validar tempos de resposta
   - Verificar thresholds de performance

### Test Patterns

#### Pattern 1: Basic GET Test
```python
def test_get_posts_returns_list(jsonplaceholder_client):
    """Testa que GET /posts retorna uma lista de posts."""
    response = jsonplaceholder_client.get_posts()
    
    validate_response_status(response, 200)
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"
    
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0
    validate_json_schema(posts[0], POST_SCHEMA)
```

#### Pattern 2: POST with Validation
```python
def test_create_post_returns_201(jsonplaceholder_client, sample_post_data):
    """Testa que POST /posts cria um novo post."""
    response = jsonplaceholder_client.create_post(sample_post_data)
    
    validate_response_status(response, 201)
    data = response.json()
    assert "id" in data
    assert data["title"] == sample_post_data["title"]
    assert data["body"] == sample_post_data["body"]
```

#### Pattern 3: Filter Test
```python
def test_filter_posts_by_user_id(jsonplaceholder_client):
    """Testa filtragem de posts por userId."""
    user_id = 1
    response = jsonplaceholder_client.get_posts(user_id=user_id)
    
    validate_response_status(response, 200)
    posts = response.json()
    assert all(post["userId"] == user_id for post in posts)
    assert len(posts) > 0
```

#### Pattern 4: Error Handling Test
```python
def test_get_nonexistent_post_returns_404(jsonplaceholder_client):
    """Testa que buscar post inexistente retorna 404."""
    response = jsonplaceholder_client.get_post(99999)
    assert response.status_code == 404
```

### Test Data Strategy

- **Usar dados existentes** para testes GET (posts 1-100, users 1-10)
- **Gerar dados dinâmicos** para testes POST/PUT/PATCH
- **Não depender de cleanup** (API é fake, não persiste dados realmente)
- **IDs conhecidos** para testes de relacionamento (ex: post 1 tem comments)

### Content-Type Validation

Todos os testes devem validar que a API retorna o Content-Type correto:
- **Expected**: `application/json; charset=utf-8`
- **Validation**: Verificar header `Content-Type` em todas as respostas

### Performance Thresholds

- **GET requests**: < 500ms
- **POST/PUT/PATCH requests**: < 1000ms
- **DELETE requests**: < 500ms
- **List endpoints**: < 1000ms

## Configuration

### Environment Variables

Adicionar ao `.env`:

```bash
# JSONPlaceholder API Configuration
JSONPLACEHOLDER_BASE_URL=https://jsonplaceholder.typicode.com
JSONPLACEHOLDER_TIMEOUT=10
JSONPLACEHOLDER_RETRIES=2
```

### Settings Extension

Não é necessário modificar `settings.py` pois o APIClient já aceita `base_url` customizada no construtor.

## Reporting

### Metrics to Track

1. **Coverage por Endpoint**
   - Quantos endpoints foram testados
   - Quais métodos HTTP foram cobertos

2. **Success Rate**
   - Taxa de sucesso por recurso
   - Taxa de sucesso por operação (GET, POST, etc.)

3. **Performance Metrics**
   - Tempo médio de resposta por endpoint
   - Endpoints mais lentos
   - Violações de threshold

4. **Validation Results**
   - Schemas validados com sucesso
   - Falhas de validação encontradas

### Report Structure

```
JSONPlaceholder API Test Report
================================

Summary:
- Total Tests: 45
- Passed: 43
- Failed: 2
- Duration: 12.5s

Endpoint Coverage:
- /posts: 10/10 tests ✓
- /users: 8/8 tests ✓
- /comments: 7/7 tests ✓
- /todos: 6/6 tests ✓
- /albums: 5/5 tests ✓

Performance:
- Average Response Time: 245ms
- Slowest Endpoint: GET /users (450ms)
- Threshold Violations: 0

Validation:
- Schema Validations: 43/43 passed
- Type Validations: 43/43 passed
```

## Implementation Notes

### Reuse of Existing Components

1. **APIClient**: Usar diretamente sem modificações
2. **Validators**: Usar `validate_response_status`, `validate_json_schema`, `validate_required_fields`
3. **Settings**: Não requer modificações, passar base_url no construtor

### New Components Required

1. **JSONPlaceholderClient**: Nova classe wrapper
2. **Schema Definitions**: Novos schemas JSON para cada recurso
3. **Test Files**: Novos arquivos de teste organizados por recurso
4. **Fixtures**: Novas fixtures específicas para JSONPlaceholder

### Dependencies

Todas as dependências já estão instaladas:
- `requests`: Para HTTP requests
- `pytest`: Para test framework
- `jsonschema`: Para validação de schemas
- `pydantic`: Para configuração

### Extensibility

O design permite fácil extensão para:
- Adicionar novos endpoints (photos, etc.)
- Adicionar novos tipos de validação
- Integrar com outras APIs públicas
- Adicionar testes de carga/stress

## Design Decisions

### Decision 1: Client Wrapper vs Direct APIClient

**Decision**: Criar JSONPlaceholderClient wrapper

**Rationale**:
- Encapsula lógica específica da API
- Facilita manutenção e reutilização
- Permite adicionar validações específicas
- Melhora legibilidade dos testes

### Decision 2: Schema Validation Approach

**Decision**: Usar jsonschema library

**Rationale**:
- Padrão da indústria para validação JSON
- Já está disponível no framework
- Permite validações complexas
- Mensagens de erro claras

### Decision 3: Test Organization

**Decision**: Organizar testes por recurso (posts, users, etc.)

**Rationale**:
- Facilita navegação e manutenção
- Permite execução seletiva por recurso
- Segue convenções pytest
- Escalável para novos recursos

### Decision 4: No Authentication Required

**Decision**: Não implementar autenticação

**Rationale**:
- JSONPlaceholder é API pública sem auth
- Simplifica implementação
- Foco em testes funcionais
- Auth já está implementado no APIClient para outras APIs

### Decision 5: Minimal Test Data Cleanup

**Decision**: Não implementar cleanup de dados

**Rationale**:
- API é fake, não persiste dados realmente
- Operações POST/PUT/DELETE retornam sucesso mas não modificam dados
- Reduz complexidade
- Foco em validação de contratos da API
