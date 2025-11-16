@middleware @email @sending @sync
Feature: Envio Direto de Emails (Síncrono)
  Como um desenvolvedor
  Eu quero enviar emails de forma síncrona
  Para comunicações imediatas e simples

  Background:
    Given que o serviço de email está disponível
    And tenho uma API key válida

  @smoke @critical
  Scenario: Enviar email simples (texto)
    Given eu tenho os dados do email:
      | campo   | valor                         |
      | to      | ["usuario@example.com"]       |
      | subject | Bem-vindo ao nosso serviço    |
      | body    | Obrigado por se juntar a nós! |
    When eu envio o email de forma síncrona
    Then o status code deve ser 200 ou 202
    And a resposta deve conter o campo "messageId" ou "trackingId"
    And o campo "status" deve ser "sent" ou "queued"

  @smoke @critical @html
  Scenario: Enviar email HTML com CC
    Given eu tenho os dados do email HTML:
      | campo   | valor                                                      |
      | to      | ["usuario@example.com"]                                    |
      | cc      | ["gerente@example.com"]                                    |
      | subject | Relatório Mensal                                           |
      | html    | <h1>Relatório Mensal</h1><p>Aqui está o seu relatório mensal.</p> |
    When eu envio o email de forma síncrona
    Then o status code deve ser 200 ou 202
    And a resposta deve confirmar o envio

  @regression @template
  Scenario: Enviar email usando template
    Given que existe um template salvo
    And eu tenho os dados do email com template:
      | campo       | valor                         |
      | to          | ["usuario@example.com"]       |
      | templateId  | <template_id>                 |
      | variables   | {"name": "João Silva", "company": "Acme Corp"} |
    When eu envio o email usando o template
    Then o status code deve ser 200 ou 202
    And o email deve ser processado com as variáveis substituídas

  @regression @attachment
  Scenario: Enviar email com anexo
    Given eu tenho um email com anexo:
      | campo       | valor                                  |
      | to          | ["usuario@example.com"]                |
      | subject     | Documento anexado                      |
      | body        | Por favor, encontre o documento anexado. |
      | attachments | [{"filename": "documento.pdf", "content": "base64...", "contentType": "application/pdf"}] |
    When eu envio o email com anexo
    Then o status code deve ser 200 ou 202
    And o email deve incluir o anexo "documento.pdf"

  @regression
  Scenario Outline: Enviar emails para múltiplos destinatários
    Given eu tenho um email para "<destinatario>"
    When eu envio o email
    Then o status code deve ser 200 ou 202
    And o email deve ser enviado para "<destinatario>"

    Examples:
      | destinatario         |
      | user1@example.com    |
      | user2@example.com    |
      | admin@example.com    |

  @negative @validation
  Scenario: Tentar enviar email sem destinatário
    Given eu tenho um email sem o campo "to"
    When eu tento enviar o email
    Then o status code deve ser 400
    And a mensagem de erro deve conter "to is required"

  @negative @validation
  Scenario: Tentar enviar email com formato inválido
    Given eu tenho um email com destinatário "email-invalido"
    When eu tento enviar o email
    Then o status code deve ser 400
    And a mensagem de erro deve conter "invalid email format"

  @negative @validation
  Scenario: Tentar enviar email sem assunto
    Given eu tenho um email sem o campo "subject"
    When eu tento enviar o email
    Then o status code deve ser 400
    And a mensagem de erro deve conter "subject is required"

  @negative @template
  Scenario: Tentar enviar email com template inexistente
    Given eu tenho um email com templateId "invalid-template-id"
    When eu tento enviar o email usando template
    Then o status code deve ser 404
    And a mensagem de erro deve conter "template not found"
