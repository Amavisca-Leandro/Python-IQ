@middleware @email @templates @crud
Feature: Gerenciamento de Templates
  Como um desenvolvedor
  Eu quero gerenciar templates de email e SMS
  Para reutilizar layouts e conteúdos personalizados

  Background:
    Given que o serviço de comunicação está disponível
    And tenho uma API key válida

  @smoke @critical
  Scenario: Listar templates com paginação
    When eu listo os templates com os parâmetros:
      | parametro | valor |
      | page      | 1     |
      | limit     | 10    |
    Then o status code deve ser 200
    And a resposta deve conter uma lista de templates
    And a lista deve ter no máximo 10 itens

  @smoke @critical
  Scenario: Criar um novo template de email
    Given eu tenho os dados do template:
      | campo       | valor                                                           |
      | type        | email                                                           |
      | name        | Welcome Email Template                                          |
      | subject     | Welcome to {{company}}!                                         |
      | body        | Hello {{name}}, welcome to our service!                         |
      | html        | <h1>Hello {{name}}</h1><p>Welcome to <strong>{{company}}</strong>!</p> |
      | description | Template de boas-vindas para novos usuários                     |
    When eu crio um novo template
    Then o status code deve ser 201
    And a resposta deve conter o campo "id"
    And o campo "name" deve ser "Welcome Email Template"
    And o campo "type" deve ser "email"
    And devo salvar o "id" retornado como "template_id"

  @regression
  Scenario: Buscar template por ID
    Given que existe um template com ID salvo
    When eu busco o template pelo ID
    Then o status code deve ser 200
    And a resposta deve conter o campo "id"
    And o campo "type" deve ser "email"

  @regression
  Scenario: Atualizar um template existente
    Given que existe um template com ID salvo
    And eu tenho os dados atualizados do template:
      | campo       | valor                                                                        |
      | name        | Updated Welcome Email Template                                               |
      | subject     | Welcome to {{company}}!                                                      |
      | html        | <h1>Hello {{name}}</h1><p>Welcome to <strong>{{company}}</strong>! We have new features!</p> |
      | description | Template de boas-vindas atualizado                                           |
      | isActive    | true                                                                         |
    When eu atualizo o template
    Then o status code deve ser 200
    And o campo "name" deve ser "Updated Welcome Email Template"

  @regression
  Scenario: Deletar (soft delete) um template
    Given que existe um template com ID salvo
    When eu deleto o template
    Then o status code deve ser 204 ou 200

  @regression @filter
  Scenario Outline: Filtrar templates por tipo
    When eu listo os templates filtrando por:
      | filtro        | valor  |
      | filter[type]  | <tipo> |
    Then o status code deve ser 200
    And todos os templates retornados devem ter type igual a "<tipo>"

    Examples:
      | tipo  |
      | email |
      | sms   |

  @regression @variables
  Scenario: Template deve suportar variáveis dinâmicas
    Given eu tenho um template com variáveis "{{name}}" e "{{company}}"
    When eu crio o template
    Then o template deve aceitar as variáveis
    And o campo "subject" deve conter "{{company}}"
    And o campo "html" deve conter "{{name}}"

  @negative
  Scenario: Tentar criar template sem tipo
    Given eu tenho os dados do template sem o campo "type"
    When eu tento criar o template
    Then o status code deve ser 400
    And a mensagem de erro deve conter "type is required"

  @negative
  Scenario: Tentar criar template sem nome
    Given eu tenho os dados do template sem o campo "name"
    When eu tento criar o template
    Then o status code deve ser 400
    And a mensagem de erro deve conter "name is required"
