@middleware @email @api_keys @crud
Feature: Gerenciamento de API Keys
  Como um administrador do sistema
  Eu quero gerenciar API Keys
  Para controlar o acesso ao serviço de comunicação

  Background:
    Given que o serviço de comunicação está disponível
    And tenho credenciais de administrador válidas

  @smoke @critical
  Scenario: Listar API Keys com paginação
    When eu listo as API keys com os parâmetros:
      | parametro | valor |
      | page      | 1     |
      | limit     | 10    |
    Then o status code deve ser 200
    And a resposta deve conter uma lista de API keys
    And a lista deve ter no máximo 10 itens
    And cada API key deve conter os campos obrigatórios:
      | campo        |
      | id           |
      | name         |
      | value        |
      | expirationAt |
      | tier         |
      | isActive     |

  @smoke @critical
  Scenario: Criar uma nova API Key
    Given eu tenho os dados da API key:
      | campo        | valor                    |
      | name         | My API Key               |
      | expirationAt | 2025-12-31T23:59:59Z     |
      | tier         | premium                  |
      | isInternal   | false                    |
    When eu crio uma nova API key
    Then o status code deve ser 201
    And a resposta deve conter o campo "id"
    And a resposta deve conter o campo "value"
    And o campo "name" deve ser "My API Key"
    And o campo "tier" deve ser "premium"
    And o campo "isActive" deve ser verdadeiro
    And devo salvar o "id" retornado como "api_key_id"
    And devo salvar o "value" retornado como "api_key_value"

  @regression
  Scenario: Buscar API Key por ID
    Given que existe uma API key com ID salvo
    When eu busco a API key pelo ID
    Then o status code deve ser 200
    And a resposta deve conter o campo "id"
    And o campo "id" deve corresponder ao ID salvo

  @regression
  Scenario: Atualizar uma API Key existente
    Given que existe uma API key com ID salvo
    And eu tenho os dados atualizados:
      | campo        | valor                      |
      | name         | My Updated API Key         |
      | isActive     | true                       |
      | expirationAt | 2025-12-31T23:59:59Z       |
      | tier         | premium                    |
    When eu atualizo a API key
    Then o status code deve ser 200
    And o campo "name" deve ser "My Updated API Key"

  @regression
  Scenario: Deletar (soft delete) uma API Key
    Given que existe uma API key com ID salvo
    When eu deleto a API key
    Then o status code deve ser 204 ou 200
    And a API key deve ser marcada como inativa

  @regression @filter
  Scenario Outline: Filtrar API Keys por status
    When eu listo as API keys filtrando por:
      | filtro        | valor           |
      | filter[isActive] | <status_ativo> |
    Then o status code deve ser 200
    And todas as API keys retornadas devem ter isActive igual a <status_ativo>

    Examples:
      | status_ativo |
      | true         |
      | false        |

  @negative
  Scenario: Tentar criar API Key sem nome
    Given eu tenho os dados da API key sem o campo "name"
    When eu tento criar a API key
    Then o status code deve ser 400
    And a mensagem de erro deve conter "name is required"

  @negative
  Scenario: Tentar buscar API Key com ID inválido
    When eu tento buscar a API key com ID "invalid-id-123"
    Then o status code deve ser 404
    And a mensagem de erro deve conter "not found"

  @negative @security
  Scenario: Tentar acessar API Keys sem autenticação
    Given que não estou autenticado
    When eu tento listar as API keys
    Then o status code deve ser 401 ou 403
