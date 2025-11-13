# Requirements Document

## Introduction

Este documento define os requisitos para implementar testes automatizados da API pública JSONPlaceholder (https://jsonplaceholder.typicode.com/). A API fornece endpoints REST para recursos como posts, comments, users, todos e albums, permitindo operações CRUD completas para fins de teste e aprendizado.

## Glossary

- **Test Framework**: O sistema de automação de testes Python baseado em pytest
- **JSONPlaceholder API**: API REST pública gratuita disponível em https://jsonplaceholder.typicode.com/
- **API Client**: Componente responsável por fazer requisições HTTP à API
- **Test Suite**: Conjunto de testes automatizados para validar endpoints da API
- **Resource Endpoint**: URL da API que representa um recurso específico (ex: /posts, /users)
- **HTTP Method**: Verbo HTTP usado para operações (GET, POST, PUT, PATCH, DELETE)
- **Response Validator**: Componente que valida estrutura e conteúdo das respostas da API
- **Test Report**: Documento gerado após execução dos testes com resultados e métricas

## Requirements

### Requirement 1

**User Story:** Como um QA Engineer, eu quero testar operações GET em recursos da API, para que eu possa validar que a API retorna dados corretos e completos

#### Acceptance Criteria

1. WHEN uma requisição GET é enviada para /posts, THE Test Framework SHALL validar que o status code é 200
2. WHEN uma requisição GET é enviada para /posts/{id}, THE Test Framework SHALL validar que o post retornado contém os campos userId, id, title e body
3. WHEN uma requisição GET é enviada para /users, THE Test Framework SHALL validar que a lista de usuários contém exatamente 10 registros
4. WHEN uma requisição GET é enviada para /users/{id}, THE Test Framework SHALL validar que o usuário retornado contém campos obrigatórios como name, email e address
5. WHEN uma requisição GET é enviada com um ID inexistente, THE Test Framework SHALL validar que o status code é 404

### Requirement 2

**User Story:** Como um QA Engineer, eu quero testar operações POST para criar novos recursos, para que eu possa validar que a API aceita e processa corretamente novos dados

#### Acceptance Criteria

1. WHEN uma requisição POST é enviada para /posts com dados válidos, THE Test Framework SHALL validar que o status code é 201
2. WHEN uma requisição POST é enviada para /posts com dados válidos, THE Test Framework SHALL validar que a resposta contém um ID gerado
3. WHEN uma requisição POST é enviada para /posts, THE Test Framework SHALL validar que os dados enviados são refletidos na resposta
4. WHEN uma requisição POST é enviada para /users com dados completos, THE Test Framework SHALL validar que o status code é 201
5. WHEN uma requisição POST é enviada sem campos obrigatórios, THE Test Framework SHALL validar o comportamento da API

### Requirement 3

**User Story:** Como um QA Engineer, eu quero testar operações PUT e PATCH para atualizar recursos, para que eu possa validar que a API processa corretamente atualizações de dados

#### Acceptance Criteria

1. WHEN uma requisição PUT é enviada para /posts/{id} com dados completos, THE Test Framework SHALL validar que o status code é 200
2. WHEN uma requisição PUT é enviada para /posts/{id}, THE Test Framework SHALL validar que todos os campos são atualizados na resposta
3. WHEN uma requisição PATCH é enviada para /posts/{id} com atualização parcial, THE Test Framework SHALL validar que o status code é 200
4. WHEN uma requisição PATCH é enviada para /posts/{id}, THE Test Framework SHALL validar que apenas os campos enviados são atualizados
5. WHEN uma requisição PUT ou PATCH é enviada para um ID inexistente, THE Test Framework SHALL validar o comportamento da API

### Requirement 4

**User Story:** Como um QA Engineer, eu quero testar operações DELETE para remover recursos, para que eu possa validar que a API processa corretamente exclusões

#### Acceptance Criteria

1. WHEN uma requisição DELETE é enviada para /posts/{id}, THE Test Framework SHALL validar que o status code é 200
2. WHEN uma requisição DELETE é enviada para um recurso válido, THE Test Framework SHALL validar que a resposta confirma a exclusão
3. WHEN uma requisição DELETE é enviada para /users/{id}, THE Test Framework SHALL validar que o status code é 200
4. WHEN uma requisição DELETE é enviada para um ID inexistente, THE Test Framework SHALL validar o comportamento da API

### Requirement 5

**User Story:** Como um QA Engineer, eu quero validar a estrutura e tipos de dados das respostas da API, para que eu possa garantir a consistência dos contratos da API

#### Acceptance Criteria

1. WHEN qualquer endpoint retorna dados, THE Test Framework SHALL validar que o Content-Type é application/json
2. WHEN um endpoint de posts retorna dados, THE Test Framework SHALL validar que userId e id são números inteiros
3. WHEN um endpoint de users retorna dados, THE Test Framework SHALL validar que email possui formato válido
4. WHEN um endpoint retorna uma lista, THE Test Framework SHALL validar que a resposta é um array JSON
5. WHEN um endpoint retorna um objeto, THE Test Framework SHALL validar que todos os campos obrigatórios estão presentes

### Requirement 6

**User Story:** Como um QA Engineer, eu quero testar filtros e query parameters, para que eu possa validar que a API suporta corretamente operações de busca e filtragem

#### Acceptance Criteria

1. WHEN uma requisição GET é enviada para /posts?userId=1, THE Test Framework SHALL validar que apenas posts do userId 1 são retornados
2. WHEN uma requisição GET é enviada para /comments?postId=1, THE Test Framework SHALL validar que apenas comments do postId 1 são retornados
3. WHEN uma requisição GET é enviada com múltiplos query parameters, THE Test Framework SHALL validar que todos os filtros são aplicados
4. WHEN uma requisição GET é enviada com query parameter inválido, THE Test Framework SHALL validar o comportamento da API

### Requirement 7

**User Story:** Como um QA Engineer, eu quero gerar relatórios detalhados dos testes executados, para que eu possa documentar e comunicar os resultados dos testes

#### Acceptance Criteria

1. WHEN os testes são executados, THE Test Framework SHALL gerar um relatório HTML com resultados detalhados
2. WHEN os testes são executados, THE Test Framework SHALL registrar tempo de resposta de cada requisição
3. WHEN os testes são executados, THE Test Framework SHALL capturar e registrar falhas com detalhes completos
4. WHEN os testes são executados, THE Test Framework SHALL calcular taxa de sucesso por endpoint
5. WHEN os testes são executados, THE Test Framework SHALL gerar métricas de cobertura dos endpoints testados
