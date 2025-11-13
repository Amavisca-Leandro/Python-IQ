# Design Document - VS Code Test Explorer Integration

## Overview

Esta solução integra o VS Code Test Explorer nativo ao framework de automação de testes Python existente, permitindo execução visual de testes pytest através da interface do Kiro. A implementação foca em configuração de workspace settings e documentação, sem necessidade de código adicional, aproveitando a extensão Python oficial do VS Code.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Kiro/VS Code IDE                      │
│  ┌────────────────────────────────────────────────────┐ │
│  │          Python Extension (Microsoft)              │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │         Test Explorer UI                     │ │ │
│  │  │  - Tree View                                 │ │ │
│  │  │  - Run/Debug Buttons                         │ │ │
│  │  │  - Status Icons                              │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  │                      ↓                             │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │         pytest Test Adapter                  │ │ │
│  │  │  - Test Discovery                            │ │ │
│  │  │  - Test Execution                            │ │ │
│  │  │  - Result Parsing                            │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              Workspace Configuration                     │
│  .vscode/settings.json                                  │
│  - python.testing.pytestEnabled: true                   │
│  - python.testing.pytestArgs: [...]                     │
│  - python.testing.cwd: ${workspaceFolder}              │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│           Existing Test Framework                        │
│  - pytest.ini                                           │
│  - conftest.py files                                    │
│  - tests/ directory structure                           │
│  - core/ framework modules                              │
└─────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

1. **Test Discovery Flow:**
   - User opens workspace → Python Extension loads
   - Extension reads `.vscode/settings.json` → Identifies pytest as test framework
   - pytest adapter scans `tests/` directory → Reads `pytest.ini` and `conftest.py`
   - Test tree is built → Displayed in Test Explorer sidebar

2. **Test Execution Flow:**
   - User clicks Run button → Test Explorer triggers pytest command
   - pytest executes with configured args → Uses virtual environment
   - Results stream back → Test Explorer updates UI in real-time
   - Pass/fail status shown → Inline decorations appear in editor

3. **Debug Flow:**
   - User clicks Debug button → VS Code debugger attaches to pytest process
   - Breakpoints are respected → Execution pauses at breakpoints
   - User inspects variables → Steps through code
   - Debug session ends → Results displayed in Test Explorer

## Components and Interfaces

### 1. Workspace Settings Configuration

**File:** `.vscode/settings.json`

**Purpose:** Configure Python extension to recognize and execute pytest tests

**Key Settings:**

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": [
    "-v",
    "--tb=short",
    "--color=yes"
  ],
  "python.testing.cwd": "${workspaceFolder}",
  "python.testing.autoTestDiscoverOnSaveEnabled": true,
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe"
}
```

**Configuration Options:**

- `pytestEnabled`: Ativa o pytest como framework de testes
- `pytestArgs`: Argumentos passados ao pytest durante execução
- `cwd`: Diretório de trabalho para execução de testes
- `autoTestDiscoverOnSaveEnabled`: Auto-descoberta ao salvar arquivos
- `defaultInterpreterPath`: Caminho para o interpretador Python (virtual environment)

### 2. Launch Configuration (Debug)

**File:** `.vscode/launch.json`

**Purpose:** Configurar debug de testes individuais

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Debug Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
        "-v",
        "-s",
        "${file}"
      ],
      "console": "integratedTerminal",
      "justMyCode": false,
      "env": {
        "PYTEST_CURRENT_TEST": ""
      }
    }
  ]
}
```

### 3. Extensions Recommendations

**File:** `.vscode/extensions.json`

**Purpose:** Recomendar extensões necessárias aos usuários

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance"
  ]
}
```

### 4. Test Explorer UI Components

**Built-in Components (provided by Python Extension):**

- **Test Tree View:** Hierarquia de testes no sidebar
- **Run/Debug Buttons:** Ícones de play e debug em cada nível
- **Status Icons:** Indicadores visuais (✓, ✗, ○, ⊘)
- **Output Panel:** Logs de execução de testes
- **Inline Decorations:** Marcadores no código mostrando status

**User Interactions:**

- Click em ícone de play → Executa teste(s)
- Click em ícone de debug → Inicia debug session
- Click em teste falhado → Navega para linha do erro
- Hover sobre teste → Mostra tooltip com informações
- Right-click → Menu contextual com opções adicionais

## Data Models

### Test Item Structure (Internal to VS Code)

```typescript
interface TestItem {
  id: string;              // e.g., "tests/test_users.py::test_get_user"
  label: string;           // e.g., "test_get_user"
  uri: Uri;                // File path
  range: Range;            // Line numbers in file
  children: TestItem[];    // Nested tests (parametrized, classes)
  status: TestStatus;      // not_run | passed | failed | skipped
  error?: TestError;       // Failure message and traceback
  duration?: number;       // Execution time in ms
}

enum TestStatus {
  NotRun = 0,
  Queued = 1,
  Running = 2,
  Passed = 3,
  Failed = 4,
  Skipped = 5,
  Errored = 6
}
```

### pytest Output Parsing

O Python Extension parseia a saída do pytest automaticamente:

```
tests/test_users.py::test_get_user PASSED [10%]
tests/test_users.py::test_create_user FAILED [20%]
```

Mapeamento para Test Explorer:
- `PASSED` → Status: Passed (green checkmark)
- `FAILED` → Status: Failed (red X) + error message
- `SKIPPED` → Status: Skipped (gray circle)
- `ERROR` → Status: Errored (red exclamation)

## Error Handling

### Common Issues and Solutions

#### 1. Tests Not Discovered

**Symptoms:**
- Test Explorer shows "No tests discovered"
- Empty test tree

**Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| pytest not installed in venv | Install: `pip install pytest` |
| Wrong Python interpreter selected | Select correct interpreter via Command Palette |
| Invalid pytest.ini configuration | Validate pytest.ini syntax |
| Tests outside configured paths | Update `python.testing.pytestArgs` to include test paths |

**Diagnostic Steps:**
1. Check Output panel → Python Test Log
2. Verify interpreter: `python --version` in terminal
3. Manual test: `pytest --collect-only`

#### 2. Tests Fail in Explorer but Pass in CLI

**Symptoms:**
- Tests pass when running `pytest` in terminal
- Same tests fail in Test Explorer

**Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| Different working directory | Set `python.testing.cwd` to `${workspaceFolder}` |
| Environment variables not set | Add env vars to `.vscode/settings.json` |
| Different Python interpreter | Ensure Test Explorer uses same venv as terminal |

#### 3. Debug Breakpoints Not Hit

**Symptoms:**
- Breakpoints ignored during debug
- Debug session runs without stopping

**Causes & Solutions:**

| Cause | Solution |
|-------|----------|
| `justMyCode` enabled | Set `"justMyCode": false` in launch.json |
| Breakpoint in fixture | Ensure conftest.py is not excluded |
| Optimized code execution | Add `--no-cov` to pytest args if using coverage |

### Error Messages

**Configuration Errors:**

```json
{
  "error": "pytest not found",
  "solution": "Install pytest: pip install pytest",
  "documentation": "https://docs.pytest.org/en/stable/getting-started.html"
}
```

**Runtime Errors:**

Test Explorer will display pytest errors inline:
- Import errors → Shown in test tree with error icon
- Syntax errors → Highlighted in editor
- Assertion failures → Full traceback in Output panel

## Testing Strategy

### Validation Steps

#### 1. Test Discovery Validation

**Objective:** Verify all tests are discovered correctly

**Steps:**
1. Open Test Explorer sidebar
2. Expand all test folders
3. Verify count matches: `pytest --collect-only | grep "test session starts"`
4. Check all test files are present
5. Verify parametrized tests show multiple entries

**Expected Results:**
- All test files visible in tree
- Correct hierarchy (folders → files → functions)
- Parametrized tests expanded with each parameter set

#### 2. Test Execution Validation

**Objective:** Verify tests execute correctly from UI

**Test Cases:**

| Test Case | Action | Expected Result |
|-----------|--------|-----------------|
| Single test | Click play on one test | Only that test runs, status updates |
| Test file | Click play on file | All tests in file run |
| Test folder | Click play on folder | All tests in folder run recursively |
| All tests | Click "Run All Tests" | Entire suite executes |
| Parallel execution | Run multiple tests | Tests queue and execute |

#### 3. Debug Validation

**Objective:** Verify debugging works correctly

**Steps:**
1. Set breakpoint in test function
2. Click debug icon on test
3. Verify execution pauses at breakpoint
4. Inspect variables in Debug panel
5. Step through code (F10, F11)
6. Continue execution (F5)

**Expected Results:**
- Breakpoint hit successfully
- Variables show correct values
- Step commands work
- Test completes after continue

#### 4. Integration Validation

**Objective:** Verify integration with existing framework

**Validation Points:**
- ✓ pytest.ini settings respected
- ✓ conftest.py fixtures available
- ✓ Custom markers work
- ✓ Allure reports still generate
- ✓ Environment variables loaded
- ✓ Database fixtures work

#### 5. Performance Validation

**Objective:** Ensure Test Explorer doesn't slow down IDE

**Metrics:**
- Test discovery time: < 5 seconds for 100+ tests
- UI responsiveness: No lag when expanding tree
- Memory usage: < 100MB additional RAM
- Test execution: Same speed as CLI

### User Acceptance Testing

**Scenario 1: New User Setup**
1. User opens project in Kiro
2. Prompted to install Python extension
3. Extension auto-discovers tests
4. User clicks play on first test
5. Test runs successfully

**Scenario 2: Daily Testing Workflow**
1. User modifies code
2. Saves file → Tests auto-discover
3. Clicks play on affected tests
4. Reviews results inline
5. Fixes failures and re-runs

**Scenario 3: Debugging Failed Test**
1. Test fails in Test Explorer
2. User clicks on failure
3. Navigates to failure line
4. Sets breakpoint
5. Clicks debug button
6. Inspects variables and finds issue

## Configuration Examples

### Minimal Configuration

For basic pytest support:

```json
{
  "python.testing.pytestEnabled": true
}
```

### Recommended Configuration

For optimal experience:

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "-v",
    "--tb=short",
    "--color=yes",
    "--maxfail=1"
  ],
  "python.testing.cwd": "${workspaceFolder}",
  "python.testing.autoTestDiscoverOnSaveEnabled": true,
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
  "python.envFile": "${workspaceFolder}/.env"
}
```

### Advanced Configuration

For teams with specific needs:

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "-v",
    "--tb=short",
    "--color=yes",
    "--maxfail=1",
    "-m", "not slow",
    "--strict-markers",
    "--alluredir=allure-results"
  ],
  "python.testing.cwd": "${workspaceFolder}",
  "python.testing.autoTestDiscoverOnSaveEnabled": true,
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
  "python.envFile": "${workspaceFolder}/.env",
  "python.analysis.extraPaths": [
    "${workspaceFolder}/core"
  ]
}
```

## Documentation Structure

### User Guide Sections

1. **Quick Start**
   - Installing Python extension
   - Opening Test Explorer
   - Running first test

2. **Test Explorer Features**
   - Tree navigation
   - Run/Debug buttons
   - Status icons
   - Filtering tests

3. **Configuration Guide**
   - settings.json options
   - launch.json for debugging
   - Environment variables
   - Custom pytest args

4. **Troubleshooting**
   - Common issues
   - Diagnostic commands
   - Log locations
   - Support resources

5. **Best Practices**
   - Organizing tests for explorer
   - Using markers effectively
   - Debug strategies
   - Performance tips

## Implementation Notes

### No Code Changes Required

Esta solução é puramente baseada em configuração:
- ✓ Nenhum código Python adicional
- ✓ Nenhuma modificação nos testes existentes
- ✓ Nenhuma dependência nova no requirements.txt
- ✓ Framework existente permanece intacto

### Compatibility

- **Kiro/VS Code:** Versão 1.60+
- **Python Extension:** Versão 2023.0.0+
- **pytest:** Versão 6.0+ (já instalado)
- **Python:** 3.8+ (já configurado)

### Maintenance

- Configurações versionadas em `.vscode/`
- Documentação em `docs/test-explorer-guide.md`
- Sem código para manter
- Updates automáticos via Python Extension

## Benefits Summary

### For Testers
- ✅ Visual test execution (no CLI needed)
- ✅ Quick feedback with inline results
- ✅ Easy navigation to failures
- ✅ Debug with breakpoints

### For Developers
- ✅ Zero code changes
- ✅ Works with existing framework
- ✅ Standard VS Code tooling
- ✅ Team-friendly (config in repo)

### For Teams
- ✅ Lower barrier to entry
- ✅ Consistent testing experience
- ✅ Better test visibility
- ✅ Faster feedback loops
