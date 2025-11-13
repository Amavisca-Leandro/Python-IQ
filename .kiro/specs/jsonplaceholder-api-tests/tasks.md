# Implementation Plan

- [x] 1. Criar estrutura base do projeto





  - Criar diretório `tests/jsonplaceholder/`
  - Criar diretório `core/clients/` para o JSONPlaceholderClient
  - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1_

- [x] 2. Implementar JSONPlaceholderClient




- [x] 2.1 Criar classe base JSONPlaceholderClient


  - Implementar `__init__` com APIClient
  - Implementar método `close()` para cleanup
  - Adicionar docstrings e type hints
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 2.2 Implementar métodos para Posts


  - Implementar `get_posts(user_id: Optional[int])` 
  - Implementar `get_post(post_id: int)`
  - Implementar `create_post(data: Dict)`
  - Implementar `update_post(post_id: int, data: Dict)`
  - Implementar `patch_post(post_id: int, data: Dict)`
  - Implementar `delete_post(post_id: int)`
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 4.1, 4.2_

- [x] 2.3 Implementar métodos para Users


  - Implementar `get_users()`
  - Implementar `get_user(user_id: int)`
  - Implementar `create_user(data: Dict)`
  - Implementar `update_user(user_id: int, data: Dict)`
  - Implementar `delete_user(user_id: int)`
  - _Requirements: 1.3, 1.4, 2.4, 3.4, 4.3_

- [x] 2.4 Implementar métodos para Comments


  - Implementar `get_comments(post_id: Optional[int])`
  - Implementar `get_comment(comment_id: int)`
  - Implementar `create_comment(data: Dict)`
  - _Requirements: 6.2_

- [x] 2.5 Implementar métodos para Todos


  - Implementar `get_todos(user_id: Optional[int])`
  - Implementar `get_todo(todo_id: int)`
  - Implementar `create_todo(data: Dict)`
  - Implementar `update_todo(todo_id: int, data: Dict)`
  - _Requirements: 6.1_

- [x] 2.6 Implementar métodos para Albums


  - Implementar `get_albums(user_id: Optional[int])`
  - Implementar `get_album(album_id: int)`
  - _Requirements: 6.1_

- [x] 3. Criar schemas de validação JSON




- [x] 3.1 Criar arquivo de schemas


  - Criar `core/clients/jsonplaceholder_schemas.py`
  - Definir POST_SCHEMA com campos obrigatórios
  - Definir USER_SCHEMA com campos obrigatórios
  - Definir COMMENT_SCHEMA com campos obrigatórios
  - Definir TODO_SCHEMA com campos obrigatórios
  - Definir ALBUM_SCHEMA com campos obrigatórios
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
-

- [x] 4. Criar fixtures pytest



- [x] 4.1 Criar conftest.py para JSONPlaceholder


  - Criar `tests/jsonplaceholder/conftest.py`
  - Implementar fixture `jsonplaceholder_client` (session scope)
  - Implementar fixture `sample_post_data`
  - Implementar fixture `sample_user_data`
  - Implementar fixture `sample_comment_data`
  - Implementar fixture `sample_todo_data`
  - Implementar função helper `validate_email_format` com regex
  - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.3_

- [x] 5. Implementar testes de Posts




- [x] 5.1 Criar test_posts.py com testes GET


  - Testar `GET /posts` retorna status 200 e lista de posts
  - Testar `GET /posts/{id}` retorna post específico com campos corretos
  - Testar `GET /posts/{id}` com ID inexistente retorna 404
  - Validar Content-Type é application/json
  - Validar schema JSON dos posts
  - Validar tipos de dados (userId e id são integers)
  - _Requirements: 1.1, 1.2, 1.5, 5.1, 5.2_

- [x] 5.2 Adicionar testes POST para posts


  - Testar `POST /posts` com dados válidos retorna 201
  - Testar `POST /posts` retorna ID gerado
  - Testar `POST /posts` reflete dados enviados na resposta
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 5.3 Adicionar testes PUT/PATCH para posts


  - Testar `PUT /posts/{id}` atualiza todos os campos
  - Testar `PATCH /posts/{id}` atualiza campos parcialmente
  - Validar status 200 para atualizações
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 5.4 Adicionar testes DELETE para posts






  - Testar `DELETE /posts/{id}` retorna 200
  - Testar `DELETE /posts/{id}` confirma exclusão
  - _Requirements: 4.1, 4.2_

- [x] 6. Implementar testes de Users




- [x] 6.1 Criar test_users.py com testes GET


  - Testar `GET /users` retorna status 200 e exatamente 10 usuários
  - Testar `GET /users/{id}` retorna usuário específico
  - Validar Content-Type é application/json
  - Validar campos obrigatórios (name, email, address)
  - Validar formato de email usando regex
  - Testar `GET /users/{id}` com ID inexistente retorna 404
  - _Requirements: 1.3, 1.4, 5.1, 5.3, 5.5_

- [x] 6.2 Adicionar testes CRUD para users






  - Testar `POST /users` com dados completos
  - Testar `PUT /users/{id}` atualiza usuário
  - Testar `DELETE /users/{id}` remove usuário
  - _Requirements: 2.4, 3.5, 4.3_
-

- [x] 7. Implementar testes de Comments






- [x] 7.1 Criar test_comments.py






  - Testar `GET /comments` retorna lista
  - Testar `GET /comments/{id}` retorna comment específico
  - Testar `POST /comments` cria novo comment
  - Validar schema JSON dos comments
  - _Requirements: 5.1, 5.5_

- [x] 8. Implementar testes de Todos




-

- [x] 8.1 Criar test_todos.py






  - Testar `GET /todos` retorna lista
  - Testar `GET /todos/{id}` retorna todo específico
  - Testar `POST /todos` cria novo todo
  - Testar `PUT /todos/{id}` atualiza todo
  - Validar campo completed é boolean
  - _Requirements: 5.2, 5.5_


- [x] 9. Implementar testes de Albums




- [x] 9.1 Criar test_albums.py







  - Testar `GET /albums` retorna lista
  - Testar `GET /albums/{id}` retorna album específico
  - Validar schema JSON dos albums
  - _Requirements: 5.1, 5.5_

- [x] 10. Implementar testes de filtros e query parameters






- [x] 10.1 Criar test_filters.py

  - Testar `GET /posts?userId=1` filtra por userId
  - Testar `GET /comments?postId=1` filtra por postId
  - Testar `GET /todos?userId=1` filtra por userId
  - Testar `GET /albums?userId=1` filtra por userId
  - Validar que filtros são aplicados corretamente
  - _Requirements: 6.1, 6.2, 6.3_

- [x] 11. Adicionar validações de performance




- [x]* 11.1 Adicionar testes de performance
  - Validar GET requests < 500ms
  - Validar POST/PUT/PATCH requests < 1000ms
  - Validar DELETE requests < 500ms
  - Usar `validate_response_time` do framework
  - _Requirements: 7.2_

-


- [x] 12. Adicionar markers pytest

- [x] 12.1 Configurar markers nos testes


  - Adicionar `@pytest.mark.smoke` para testes básicos
  - Adicionar `@pytest.mark.crud` para testes CRUD
  - Adicionar `@pytest.mark.validation` para testes de validação
  - Adicionar `@pytest.mark.filters` para testes de filtros
  - Adicionar `@pytest.mark.performance` para testes de performance
  - _Requirements: 7.1, 7.3_

- [x] 13. Configurar relatórios




- [x]* 13.1 Adicionar configuração de relatórios avançados
  - Configurar pytest-html para relatórios HTML
  - Adicionar métricas de cobertura de endpoints
  - Adicionar métricas de performance
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 14. Criar documentação





- [x]* 14.1 Criar README para testes JSONPlaceholder
  - Documentar como executar os testes
  - Documentar markers disponíveis
  - Documentar estrutura dos testes
  - Adicionar exemplos de uso
  - _Requirements: 7.1_
