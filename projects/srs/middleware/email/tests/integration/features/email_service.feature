@middleware @email @api @smoke
Feature: Email Service do SRS
  Como um desenvolvedor do SRS
  Eu quero enviar emails através do middleware
  Para que os usuários recebam notificações

  Background:
    Given o serviço de email está disponível
    And tenho uma API key válida

  @critical
  Scenario: Enviar email simples com sucesso
    Given eu tenho os dados do email:
      | field   | value                    |
      | to      | user@example.com         |
      | subject | Teste de Email           |
      | body    | Este é um email de teste |
    When eu envio o email através do serviço
    Then o email deve ser aceito com status code 200
    And a resposta deve conter o ID do email
    And a resposta deve conter o status "queued"

  @critical
  Scenario: Consultar status de email enviado
    Given eu enviei um email com ID "12345"
    When eu consulto o status do email
    Then o status code deve ser 200
    And o status do email deve ser "delivered"

  @regression
  Scenario Outline: Enviar emails para múltiplos destinatários
    Given eu tenho um email para "<destinatario>"
    When eu envio o email
    Then o email deve ser aceito
    And o destinatário "<destinatario>" deve estar correto

    Examples:
      | destinatario         |
      | user1@example.com    |
      | user2@example.com    |
      | admin@example.com    |

  @negative
  Scenario: Enviar email sem destinatário
    Given eu tenho um email sem destinatário
    When eu tento enviar o email
    Then deve retornar erro 400
    And a mensagem de erro deve conter "to is required"

  @negative
  Scenario: Enviar email com formato inválido
    Given eu tenho um email com destinatário "email-invalido"
    When eu tento enviar o email
    Then deve retornar erro 400
    And a mensagem de erro deve conter "invalid email format"

  @email @validation
  Scenario: Validar endereço de email
    When eu valido o email "user@example.com"
    Then o email deve ser considerado válido
    And não deve haver sugestões de correção

  @email @validation @negative
  Scenario: Validar email com typo
    When eu valido o email "user@gmial.com"
    Then o email deve ser considerado inválido
    And deve sugerir "gmail.com" como correção

  @email @history
  Scenario: Listar histórico de emails
    Given existem 10 emails enviados
    When eu consulto o histórico de emails
    Then deve retornar 10 emails
    And cada email deve ter ID, status e timestamp

  @email @history @filter
  Scenario: Filtrar histórico por status
    Given existem emails com diferentes status
    When eu consulto o histórico filtrando por status "failed"
    Then deve retornar apenas emails com status "failed"
