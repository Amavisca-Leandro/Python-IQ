# JSONPlaceholder API Tests

Testes automatizados para a API pública JSONPlaceholder (https://jsonplaceholder.typicode.com/).

## 📋 Visão Geral

Este conjunto de testes valida todos os endpoints principais da API JSONPlaceholder, incluindo operações CRUD completas para os seguintes recursos:

- **Posts** - Artigos/publicações
- **Users** - Usuários
- **Comments** - Comentários
- **Todos** - Tarefas
- **Albums** - Álbuns

## 🎯 Objetivos dos Testes

- ✅ Validar operações GET, POST, PUT, PATCH e DELETE
- ✅ Verificar estrutura e schemas JSON das respostas
- ✅ Validar tipos de dados e campos obrigatórios
- ✅ Testar filtros e query parameters
- ✅ Medir performance e tempos de resposta
- ✅ Garantir consistência dos contratos da API

## 🏗️ Estrutura dos Testes

```
tests/jsonplaceholder/
├── conftest.py                 # Fixtures compartilhadas
├── conftest_metrics.py         # Plugin de métricas
├── test_posts.py              # Testes de posts (GET, POST, PUT, PATCH, DELETE)
├── test_users.py              # Testes de users (GET, POST, PUT, DELETE)
├── test_comments.py           # Testes de comments (GET, POST)
├── test_todos.py              # Testes de todos (GET, POST, PUT)
├── test_albums.py             # Testes de albums (GET)
├── test_filters.py            # Testes de query parameters
├── test_performance.py        # Testes de performance
└── README.md                  # Esta documentação
```

## 🚀 Como Executar os Testes

### Executar Todos os Testes

```bash
pytest tests/jsonplaceholder/ -v
```

### Executar por Categoria (Markers)

#### Smoke Tests (Testes Críticos)
```bash
pytest tests/jsonplaceholder/ -m smoke -v
```

#### CRUD Tests (Operações Create, Read, Update, Delete)
```bash
pytest tests/jsonplaceholder/ -m crud -v
```

#### Validation Tests (Validação de Schemas e Dados)
```bash
pytest tests/jsonplaceholder/ -m validation -v
```

#### Filter Tests (Testes de Query Parameters)
```bash
pytest tests/jsonplaceholder/ -m filters -v
```

#### Performance Tests (Validação de Tempos de Resposta)
```bash
pytest tests/jsonplaceholder/ -m performance -v
```

### Executar Testes de um Recurso Específico

```bash
# Testes de Posts
pytest tests/jsonplaceholder/test_posts.py -v

# Testes de Users
pytest tests/jsonplaceholder/test_users.py -v

# Testes de Comments
pytest tests/jsonplaceholder/test_comments.py -v

# Testes de Todos
pytest tests/jsonplaceholder/test_todos.py -v

# Testes de Albums
pytest tests/jsonplaceholder/test_albums.py -v

# Testes de Filtros
pytest tests/jsonplaceholder/test_filters.py -v

# Testes de Performance
pytest tests/jsonplaceholder/test_performance.py -v
```

### Executar com Relatório HTML

```bash
pytest tests/jsonplaceholder/ -v --html=reports/jsonplaceholder_report.html --self-contained-html
```

### Executar em Paralelo (Mais Rápido)

```bash
pytest tests/jsonplaceholder/ -v -n auto
```

## 📊 Markers Disponíveis

| Marker | Descrição | Exemplo |
|--------|-----------|---------|
| `smoke` | Testes críticos que devem sempre passar | `@pytest.mark.smoke` |
| `crud` | Testes de operações CRUD | `@pytest.mark.crud` |
| `validation` | Testes de validação de schemas e dados | `@pytest.mark.validation` |
| `filters` | Testes de query parameters e filtros | `@pytest.mark.filters` |
| `performance` | Testes de performance e tempos de resposta | `@pytest.mark.performance` |

## 📈 Relatórios e Métricas

### Relatório HTML Padrão

Após executar os testes, um relatório HTML é gerado automaticamente:

```
reports/jsonplaceholder_report.html
```

### Relatório de Métricas

Um relatório de métricas detalhado é gerado em:

```
reports/jsonplaceholder_metrics.txt
```

Este relatório inclui:
- Taxa de sucesso por recurso
- Cobertura de endpoints
- Métricas de performance
- Violações de threshold

### Relatório HTML Aprimorado

Para gerar um relatório HTML customizado com visualizações aprimoradas:

```bash
python scripts/generate_jsonplaceholder_report.py
```

O relatório será gerado em:
```
reports/jsonplaceholder_enhanced_report.html
```

## 🔧 Fixtures Disponíveis

### `jsonplaceholder_client`
Cliente configurado para a API JSONPlaceholder (session scope).

```python
def test_example(jsonplaceholder_client):
    response = jsonplaceholder_client.get_posts()
    assert response.status_code == 200
```

### `sample_post_data`
Dados de exemplo para criar um post.

```python
def test_create_post(jsonplaceholder_client, sample_post_data):
    response = jsonplaceholder_client.create_post(sample_post_data)
    assert response.status_code == 201
```

### `sample_user_data`
Dados de exemplo para criar um usuário.

```python
def test_create_user(jsonplaceholder_client, sample_user_data):
    response = jsonplaceholder_client.create_user(sample_user_data)
    assert response.status_code == 201
```

### `sample_comment_data`
Dados de exemplo para criar um comentário.

```python
def test_create_comment(jsonplaceholder_client, sample_comment_data):
    response = jsonplaceholder_client.create_comment(sample_comment_data)
    assert response.status_code == 201
```

### `sample_todo_data`
Dados de exemplo para criar uma tarefa.

```python
def test_create_todo(jsonplaceholder_client, sample_todo_data):
    response = jsonplaceholder_client.create_todo(sample_todo_data)
    assert response.status_code == 201
```

## 📝 Exemplos de Uso

### Exemplo 1: Teste GET Básico

```python
import pytest
from core.helpers.validators import validate_response_status

@pytest.mark.smoke
def test_get_posts(jsonplaceholder_client):
    """Testa que GET /posts retorna lista de posts."""
    response = jsonplaceholder_client.get_posts()
    validate_response_status(response, 200)
    
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0
```

### Exemplo 2: Teste POST com Validação

```python
import pytest
from core.helpers.validators import validate_response_status, validate_json_schema
from core.clients.jsonplaceholder_schemas import POST_SCHEMA

@pytest.mark.crud
def test_create_post(jsonplaceholder_client, sample_post_data):
    """Testa criação de post."""
    response = jsonplaceholder_client.create_post(sample_post_data)
    validate_response_status(response, 201)
    
    data = response.json()
    assert "id" in data
    validate_json_schema(data, POST_SCHEMA)
```

### Exemplo 3: Teste de Filtro

```python
import pytest
from core.helpers.validators import validate_response_status

@pytest.mark.filters
def test_filter_posts_by_user(jsonplaceholder_client):
    """Testa filtragem de posts por userId."""
    user_id = 1
    response = jsonplaceholder_client.get_posts(user_id=user_id)
    validate_response_status(response, 200)
    
    posts = response.json()
    assert all(post["userId"] == user_id for post in posts)
```

### Exemplo 4: Teste de Performance

```python
import pytest
from core.helpers.validators import validate_response_status, validate_response_time

@pytest.mark.performance
def test_get_posts_performance(jsonplaceholder_client):
    """Testa que GET /posts responde em menos de 1000ms."""
    response = jsonplaceholder_client.get_posts()
    validate_response_status(response, 200)
    validate_response_time(response, 1000)
```

## 🎨 Cobertura de Endpoints

### Posts
- ✅ GET /posts - Listar todos os posts
- ✅ GET /posts/{id} - Obter post específico
- ✅ GET /posts?userId={id} - Filtrar posts por usuário
- ✅ POST /posts - Criar novo post
- ✅ PUT /posts/{id} - Atualizar post completo
- ✅ PATCH /posts/{id} - Atualizar post parcialmente
- ✅ DELETE /posts/{id} - Deletar post

### Users
- ✅ GET /users - Listar todos os usuários
- ✅ GET /users/{id} - Obter usuário específico
- ✅ POST /users - Criar novo usuário
- ✅ PUT /users/{id} - Atualizar usuário
- ✅ DELETE /users/{id} - Deletar usuário

### Comments
- ✅ GET /comments - Listar todos os comentários
- ✅ GET /comments/{id} - Obter comentário específico
- ✅ GET /comments?postId={id} - Filtrar comentários por post
- ✅ POST /comments - Criar novo comentário

### Todos
- ✅ GET /todos - Listar todas as tarefas
- ✅ GET /todos/{id} - Obter tarefa específica
- ✅ GET /todos?userId={id} - Filtrar tarefas por usuário
- ✅ POST /todos - Criar nova tarefa
- ✅ PUT /todos/{id} - Atualizar tarefa

### Albums
- ✅ GET /albums - Listar todos os álbuns
- ✅ GET /albums/{id} - Obter álbum específico
- ✅ GET /albums?userId={id} - Filtrar álbuns por usuário

## ⚡ Thresholds de Performance

Os testes de performance validam os seguintes limites:

| Tipo de Requisição | Threshold |
|-------------------|-----------|
| GET (item único) | < 500ms |
| GET (lista) | < 1000ms |
| POST | < 1000ms |
| PUT | < 1000ms |
| PATCH | < 1000ms |
| DELETE | < 500ms |

## 🔍 Validações Implementadas

### Validação de Status Code
```python
validate_response_status(response, 200)
```

### Validação de Schema JSON
```python
validate_json_schema(data, POST_SCHEMA)
```

### Validação de Campos Obrigatórios
```python
validate_required_fields(data, ["userId", "id", "title", "body"])
```

### Validação de Tipos de Dados
```python
validate_field_types(data, {
    "userId": int,
    "id": int,
    "title": str,
    "body": str
})
```

### Validação de Tempo de Resposta
```python
validate_response_time(response, 1000)  # 1000ms
```

### Validação de Formato de Email
```python
from tests.jsonplaceholder.conftest import validate_email_format
assert validate_email_format("user@example.com")
```

## 🛠️ Componentes Utilizados

### JSONPlaceholderClient
Cliente especializado para interagir com a API JSONPlaceholder.

```python
from core.clients.jsonplaceholder_client import JSONPlaceholderClient

client = JSONPlaceholderClient()
response = client.get_posts()
client.close()
```

### Schemas de Validação
Schemas JSON para validar estrutura das respostas.

```python
from core.clients.jsonplaceholder_schemas import (
    POST_SCHEMA,
    USER_SCHEMA,
    COMMENT_SCHEMA,
    TODO_SCHEMA,
    ALBUM_SCHEMA
)
```

### Validators
Funções de validação reutilizáveis.

```python
from core.helpers.validators import (
    validate_response_status,
    validate_response_time,
    validate_json_schema,
    validate_required_fields,
    validate_field_types
)
```

## 📚 Recursos Adicionais

### API Documentation
- **JSONPlaceholder**: https://jsonplaceholder.typicode.com/
- **Guide**: https://jsonplaceholder.typicode.com/guide/

### Pytest Documentation
- **Pytest**: https://docs.pytest.org/
- **Markers**: https://docs.pytest.org/en/stable/how-to/mark.html
- **Fixtures**: https://docs.pytest.org/en/stable/how-to/fixtures.html

## 🤝 Contribuindo

Para adicionar novos testes:

1. Identifique o recurso ou endpoint a ser testado
2. Adicione o teste no arquivo apropriado (test_posts.py, test_users.py, etc.)
3. Use os markers apropriados (@pytest.mark.smoke, @pytest.mark.crud, etc.)
4. Utilize as fixtures e validators existentes
5. Documente o teste com docstring clara
6. Execute os testes para validar

## 📞 Suporte

Para questões ou problemas:
- Verifique a documentação da API JSONPlaceholder
- Revise os exemplos neste README
- Consulte os testes existentes como referência
- Execute os testes com `-v` para output detalhado

## 📄 Licença

Este projeto faz parte do Python Test Automation Framework.
