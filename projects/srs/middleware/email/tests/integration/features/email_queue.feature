@middleware @email @queue @async
Feature: Fila de Emails (Assíncrono)
  Como um desenvolvedor
  Eu quero adicionar emails em fila
  Para envios em massa, agendados e com alta disponibilidade

  Background:
    Given que o serviço de fila de emails está disponível
    And tenho uma API key válida

  @smoke @critical
  Scenario: Adicionar email único na fila
    Given eu tenho os dados do email para fila:
      | campo        | valor                                         |
      | to           | [{"email": "usuario@example.com", "name": "João Silva"}] |
      | subject      | Bem-vindo ao nosso serviço                    |
      | textContent  | Obrigado por se juntar a nós!                 |
      | priority     | medium                                        |
    When eu adiciono o email na fila
    Then o status code deve ser 201 ou 202
    And a resposta deve conter o campo "trackingId" ou "queueId"
    And o campo "status" deve ser "queued" ou "pending"

  @regression @template
  Scenario: Adicionar email com template na fila
    Given que existe um template salvo
    And eu tenho os dados do email com template para fila:
      | campo             | valor                                                |
      | to                | [{"email": "usuario@example.com", "name": "João Silva"}] |
      | templateId        | <template_id>                                        |
      | templateVariables | {"name": "João Silva", "company": "Acme Corp"}       |
      | priority          | high                                                 |
      | trackOpens        | true                                                 |
      | trackClicks       | true                                                 |
    When eu adiciono o email na fila
    Then o status code deve ser 201 ou 202
    And o email deve ser enfileirado com prioridade "high"
    And o tracking deve estar habilitado

  @regression @status
  Scenario: Consultar status de email na fila
    Given que adicionei um email na fila
    And salvei o trackingId retornado
    When eu consulto o status do email pelo trackingId
    Then o status code deve ser 200
    And a resposta deve conter o campo "status"
    And o status deve ser um dos valores válidos:
      | status      |
      | queued      |
      | processing  |
      | sent        |
      | delivered   |
      | failed      |
      | bounced     |

  @smoke @critical @bulk
  Scenario: Adicionar emails em massa na fila
    Given eu tenho os dados para envio em massa:
      | campo      | valor                                                            |
      | templateId | <template_id>                                                    |
      | recipients | [{"email": "user1@example.com", "name": "João", "templateVariables": {"name": "João"}}, {"email": "user2@example.com", "name": "Maria", "templateVariables": {"name": "Maria"}}] |
      | batchSize  | 100                                                              |
      | batchDelay | 5                                                                |
      | priority   | medium                                                           |
    When eu adiciono os emails em massa na fila
    Then o status code deve ser 201 ou 202
    And a resposta deve conter o campo "batchId" ou "bulkTrackingId"
    And o número de emails enfileirados deve ser 2

  @regression @bulk @status
  Scenario: Consultar status de envio em massa
    Given que adicionei emails em massa na fila
    And salvei o batchId retornado
    When eu consulto o status do envio em massa
    Then o status code deve ser 200
    And a resposta deve conter estatísticas do lote:
      | campo       |
      | total       |
      | queued      |
      | sent        |
      | failed      |
      | delivered   |

  @regression @scheduled
  Scenario: Agendar email para envio futuro
    Given eu tenho os dados do email agendado:
      | campo             | valor                                                |
      | to                | [{"email": "usuario@example.com", "name": "João Silva"}] |
      | subject           | Newsletter Agendada                                  |
      | templateId        | <template_id>                                        |
      | scheduledFor      | 2025-12-25T09:00:00Z                                 |
      | timezone          | America/Sao_Paulo                                    |
      | priority          | medium                                               |
    When eu agendar o email
    Then o status code deve ser 201 ou 202
    And a resposta deve conter o campo "scheduleId"
    And o email deve estar agendado para "2025-12-25T09:00:00Z"

  @regression @scheduled @cancel
  Scenario: Cancelar email agendado
    Given que agendei um email
    And salvei o scheduleId retornado
    When eu cancelo o email agendado
    Then o status code deve ser 200 ou 204
    And o email agendado deve ser cancelado

  @regression @priority
  Scenario Outline: Enfileirar emails com diferentes prioridades
    Given eu tenho um email com prioridade "<prioridade>"
    When eu adiciono o email na fila
    Then o email deve ser processado com prioridade "<prioridade>"

    Examples:
      | prioridade |
      | low        |
      | medium     |
      | high       |
      | urgent     |

  @regression @tracking
  Scenario: Email com tracking habilitado
    Given eu tenho um email com tracking:
      | campo       | valor |
      | trackOpens  | true  |
      | trackClicks | true  |
    When eu adiciono o email na fila
    Then o email deve ter tracking de aberturas habilitado
    And o email deve ter tracking de cliques habilitado

  @negative
  Scenario: Tentar adicionar email sem destinatário na fila
    Given eu tenho dados de email sem o campo "to"
    When eu tento adicionar na fila
    Then o status code deve ser 400
    And a mensagem de erro deve conter "to is required"

  @negative @bulk
  Scenario: Tentar envio em massa sem recipients
    Given eu tenho dados de envio em massa sem "recipients"
    When eu tento adicionar na fila
    Then o status code deve ser 400
    And a mensagem de erro deve conter "recipients is required"

  @negative @scheduled
  Scenario: Tentar agendar email com data passada
    Given eu tenho um email com scheduledFor no passado
    When eu tento agendar o email
    Then o status code deve ser 400
    And a mensagem de erro deve conter "scheduledFor must be in the future"
