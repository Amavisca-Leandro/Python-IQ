# Requirements Document

## Introduction

Este documento define os requisitos para implementar a geração automatizada de relatórios Allure profissionais e visualmente atraentes para o framework de testes Python + Playwright existente. O sistema já possui integração com Allure (allure-pytest), mas necessita de scripts e documentação para facilitar a geração e visualização dos relatórios HTML.

## Glossary

- **Allure Framework**: Framework de relatórios de testes open-source que gera relatórios HTML interativos e visualmente atraentes
- **Allure Results**: Arquivos JSON e anexos gerados durante a execução dos testes (localizados em `reports/allure-results/`)
- **Allure Report**: Relatório HTML final gerado a partir dos resultados Allure
- **Test Automation System**: O framework de testes Python + Playwright + Pytest existente no projeto
- **Report Generation Script**: Script batch/shell que automatiza o processo de geração do relatório Allure
- **Allure CLI**: Ferramenta de linha de comando do Allure para gerar e servir relatórios

## Requirements

### Requirement 1

**User Story:** Como QA Engineer, eu quero gerar relatórios Allure HTML profissionais com um único comando, para que eu possa visualizar os resultados dos testes de forma rápida e eficiente

#### Acceptance Criteria

1. WHEN THE QA Engineer executa o script de geração de relatório, THE Test Automation System SHALL gerar um relatório Allure HTML completo em menos de 10 segundos
2. WHEN THE relatório é gerado, THE Test Automation System SHALL armazenar o relatório HTML no diretório `reports/allure-report/`
3. WHEN THE relatório é gerado com sucesso, THE Test Automation System SHALL abrir automaticamente o relatório no navegador padrão
4. WHERE THE Allure CLI não está instalado, THE Test Automation System SHALL exibir instruções claras de instalação
5. WHEN THE diretório de resultados está vazio, THE Test Automation System SHALL exibir uma mensagem informativa orientando o usuário a executar testes primeiro

### Requirement 2

**User Story:** Como QA Engineer, eu quero visualizar relatórios Allure com gráficos, histórico e categorização de falhas, para que eu possa analisar a qualidade dos testes de forma profissional

#### Acceptance Criteria

1. THE Allure Report SHALL exibir um dashboard com estatísticas gerais (total de testes, taxa de sucesso, duração)
2. THE Allure Report SHALL incluir gráficos visuais de distribuição de status dos testes (passed, failed, broken, skipped)
3. THE Allure Report SHALL categorizar testes por suites, features e severidade
4. THE Allure Report SHALL exibir histórico de execuções quando disponível
5. WHEN UM teste falha, THE Allure Report SHALL exibir stack traces, screenshots e logs anexados

### Requirement 3

**User Story:** Como QA Engineer, eu quero scripts separados para diferentes cenários de geração de relatório, para que eu possa escolher entre gerar relatório simples ou com servidor local

#### Acceptance Criteria

1. THE Test Automation System SHALL fornecer um script para gerar relatório e abrir no navegador
2. THE Test Automation System SHALL fornecer um script para iniciar servidor Allure local na porta 4040
3. THE Test Automation System SHALL fornecer um script para limpar resultados antigos antes de nova execução
4. WHERE O usuário executa o script de servidor, THE Test Automation System SHALL manter o servidor ativo até interrupção manual
5. THE Test Automation System SHALL fornecer scripts compatíveis com Windows (batch) e Unix (shell)

### Requirement 4

**User Story:** Como QA Engineer, eu quero documentação clara sobre como gerar e visualizar relatórios Allure, para que eu possa usar o sistema sem conhecimento prévio do Allure

#### Acceptance Criteria

1. THE Test Automation System SHALL fornecer um guia rápido em português com comandos essenciais
2. THE Test Automation System SHALL documentar o processo de instalação do Allure CLI
3. THE Test Automation System SHALL incluir exemplos de uso dos scripts de geração de relatório
4. THE Test Automation System SHALL documentar como interpretar os principais elementos do relatório Allure
5. THE Test Automation System SHALL incluir troubleshooting para problemas comuns

### Requirement 5

**User Story:** Como QA Engineer, eu quero que os testes existentes já incluam metadados Allure (severidade, features, stories), para que os relatórios sejam mais organizados e informativos

#### Acceptance Criteria

1. WHERE POSSÍVEL, THE Test Automation System SHALL adicionar decorators `@allure.feature()` aos testes existentes
2. WHERE POSSÍVEL, THE Test Automation System SHALL adicionar decorators `@allure.story()` aos testes existentes
3. WHERE POSSÍVEL, THE Test Automation System SHALL adicionar decorators `@allure.severity()` aos testes críticos
4. THE Test Automation System SHALL adicionar steps descritivos usando `allure.step()` em testes complexos
5. THE Test Automation System SHALL anexar screenshots automaticamente em falhas de testes UI
