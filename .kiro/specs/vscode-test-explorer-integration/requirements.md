# Requirements Document

## Introduction

Este documento define os requisitos para integrar o VS Code Test Explorer ao framework de automação de testes Python existente, permitindo que os usuários executem testes pytest através de uma interface gráfica integrada ao Kiro/VS Code, com botões de execução, visualização em árvore e resultados inline.

## Glossary

- **Test Explorer**: Painel lateral do VS Code que exibe testes em estrutura de árvore com controles de execução
- **Workspace Settings**: Arquivo `.vscode/settings.json` que contém configurações específicas do projeto
- **Python Extension**: Extensão oficial da Microsoft para suporte a Python no VS Code
- **Test Discovery**: Processo automático de identificação de testes no projeto
- **Inline Results**: Exibição de resultados de testes diretamente no editor de código

## Requirements

### Requirement 1

**User Story:** Como um testador, eu quero visualizar todos os testes do projeto em uma árvore hierárquica no painel lateral, para que eu possa navegar facilmente pela estrutura de testes.

#### Acceptance Criteria

1. WHEN the Test Explorer is opened, THE Test Explorer SHALL display all pytest test files in a hierarchical tree structure
2. THE Test Explorer SHALL organize tests by directory structure matching the tests/ folder hierarchy
3. THE Test Explorer SHALL show individual test functions within each test file
4. THE Test Explorer SHALL automatically refresh the test tree when new test files are created or modified
5. THE Test Explorer SHALL display test status icons (not run, passed, failed, skipped) next to each test item

### Requirement 2

**User Story:** Como um testador, eu quero executar testes individuais ou em grupo clicando em botões, para que eu não precise usar a linha de comando.

#### Acceptance Criteria

1. WHEN a user clicks the play button next to a test, THE Test Explorer SHALL execute only that specific test
2. WHEN a user clicks the play button next to a test file, THE Test Explorer SHALL execute all tests within that file
3. WHEN a user clicks the play button next to a directory, THE Test Explorer SHALL execute all tests within that directory and subdirectories
4. THE Test Explorer SHALL provide a "Run All Tests" button that executes the entire test suite
5. THE Test Explorer SHALL display a loading indicator while tests are running

### Requirement 3

**User Story:** Como um testador, eu quero ver os resultados dos testes diretamente no editor, para que eu possa identificar rapidamente falhas sem abrir relatórios externos.

#### Acceptance Criteria

1. WHEN a test passes, THE Test Explorer SHALL display a green checkmark icon next to the test
2. WHEN a test fails, THE Test Explorer SHALL display a red X icon and show the failure message
3. THE Test Explorer SHALL display inline decorations in the code editor showing pass/fail status
4. WHEN a test fails, THE Test Explorer SHALL provide a clickable link to navigate to the failure location in code
5. THE Test Explorer SHALL show execution time for each test in the tree view

### Requirement 4

**User Story:** Como um desenvolvedor, eu quero depurar testes individuais com breakpoints, para que eu possa investigar problemas complexos passo a passo.

#### Acceptance Criteria

1. WHEN a user clicks the debug button next to a test, THE Test Explorer SHALL start a debug session for that test
2. THE Test Explorer SHALL respect breakpoints set in test code during debug sessions
3. THE Test Explorer SHALL allow stepping through test code using standard VS Code debug controls
4. THE Test Explorer SHALL display variable values in the debug panel during test execution
5. THE Test Explorer SHALL support debugging of fixtures and conftest.py files

### Requirement 5

**User Story:** Como um testador, eu quero que o Test Explorer reconheça automaticamente a configuração pytest existente, para que eu não precise reconfigurar o framework.

#### Acceptance Criteria

1. THE Test Explorer SHALL read pytest configuration from pytest.ini file
2. THE Test Explorer SHALL respect existing conftest.py fixtures and configurations
3. THE Test Explorer SHALL use the project's virtual environment for test execution
4. THE Test Explorer SHALL apply pytest markers and custom configurations during test discovery
5. THE Test Explorer SHALL support parametrized tests and display each parameter combination as a separate test item

### Requirement 6

**User Story:** Como um testador, eu quero configurar opções de execução de testes através de settings, para que eu possa personalizar o comportamento do Test Explorer.

#### Acceptance Criteria

1. THE Workspace Settings SHALL allow configuration of pytest arguments (e.g., -v, -s, --tb=short)
2. THE Workspace Settings SHALL allow specification of test discovery patterns
3. THE Workspace Settings SHALL allow configuration of the Python interpreter path
4. THE Workspace Settings SHALL allow enabling/disabling auto test discovery
5. THE Workspace Settings SHALL persist configurations in .vscode/settings.json file
