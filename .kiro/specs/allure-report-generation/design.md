# Design Document - Allure Report Generation

## Overview

Este design implementa um sistema completo de geração e visualização de relatórios Allure para o framework de testes Python + Playwright existente. A solução fornece scripts automatizados, documentação em português e melhorias nos testes para maximizar o valor dos relatórios Allure.

O sistema aproveita a infraestrutura existente (allure-pytest já instalado, resultados em `reports/allure-results/`) e adiciona camadas de automação e documentação para tornar o Allure acessível a todos os membros da equipe.

## Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Test Execution Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Pytest     │  │  Playwright  │  │ Allure-Pytest│      │
│  │   Runner     │──│   Browser    │──│   Plugin     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Allure Results Storage                    │
│              reports/allure-results/*.json                   │
│         (containers, results, attachments, history)          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Report Generation Scripts                   │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ gerar_allure.bat │  │ allure_server.bat│                │
│  │ (Generate+Open)  │  │ (Local Server)   │                │
│  └──────────────────┘  └──────────────────┘                │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ limpar_allure.bat│  │ gerar_allure.sh  │                │
│  │ (Clean Results)  │  │ (Unix version)   │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Allure CLI Tool                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  allure generate --clean -o reports/allure-report    │  │
│  │  allure serve reports/allure-results                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    HTML Report Output                        │
│              reports/allure-report/index.html                │
│         (Dashboard, Graphs, Test Details, History)           │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
project-root/
├── scripts/
│   ├── gerar_allure.bat              # Windows: Generate + Open
│   ├── gerar_allure.sh               # Unix: Generate + Open
│   ├── allure_server.bat             # Windows: Start local server
│   ├── allure_server.sh              # Unix: Start local server
│   ├── limpar_allure.bat             # Windows: Clean old results
│   └── limpar_allure.sh              # Unix: Clean old results
├── reports/
│   ├── allure-results/               # JSON results (existing)
│   ├── allure-report/                # Generated HTML report (new)
│   └── allure-history/               # Historical data (new)
├── docs/
│   ├── ALLURE_GUIDE.md               # Complete Allure guide (new)
│   └── ALLURE_QUICK_START.md         # Quick start guide (new)
└── tests/
    └── (existing test files with Allure decorators)
```

## Components and Interfaces

### 1. Report Generation Scripts

#### gerar_allure.bat / gerar_allure.sh
**Purpose:** Generate Allure HTML report and open in browser

**Interface:**
```batch
# Windows
gerar_allure.bat

# Unix
./gerar_allure.sh
```

**Behavior:**
1. Check if Allure CLI is installed
2. Verify allure-results directory exists and has files
3. Generate report: `allure generate --clean reports/allure-results -o reports/allure-report`
4. Open report in default browser
5. Display success message with report location

**Error Handling:**
- Allure not installed → Display installation instructions
- No results found → Prompt user to run tests first
- Generation fails → Display error and suggest troubleshooting

#### allure_server.bat / allure_server.sh
**Purpose:** Start Allure local server for live report viewing

**Interface:**
```batch
# Windows
allure_server.bat

# Unix
./allure_server.sh
```

**Behavior:**
1. Check if Allure CLI is installed
2. Verify allure-results directory exists
3. Start server: `allure serve reports/allure-results -p 4040`
4. Display server URL (http://localhost:4040)
5. Keep server running until Ctrl+C

**Features:**
- Custom port (4040) to avoid conflicts
- Auto-opens browser
- Live reload on new test results

#### limpar_allure.bat / limpar_allure.sh
**Purpose:** Clean old Allure results before new test run

**Interface:**
```batch
# Windows
limpar_allure.bat

# Unix
./limpar_allure.sh
```

**Behavior:**
1. Prompt user for confirmation
2. Delete contents of `reports/allure-results/`
3. Delete contents of `reports/allure-report/`
4. Preserve directory structure
5. Display cleanup summary

### 2. Allure Configuration

#### pytest.ini Enhancement
**Current Configuration:**
```ini
addopts =
    --alluredir=reports/allure-results
```

**Enhanced Configuration:**
```ini
[pytest]
# ... existing config ...

# Allure Configuration
addopts =
    --alluredir=reports/allure-results
    --clean-alluredir

# Allure Categories (for failure classification)
# Create allure-results/categories.json automatically
```

#### categories.json
**Purpose:** Classify test failures into categories

**Location:** `reports/allure-results/categories.json`

**Content:**
```json
[
  {
    "name": "Product Defects",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*AssertionError.*"
  },
  {
    "name": "Test Defects",
    "matchedStatuses": ["broken"],
    "messageRegex": ".*"
  },
  {
    "name": "Timeout Issues",
    "matchedStatuses": ["broken"],
    "messageRegex": ".*TimeoutError.*"
  }
]
```

### 3. Test Enhancements with Allure Decorators

#### Feature Organization
```python
import allure

@allure.feature("JSONPlaceholder API")
@allure.story("User Management")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_user():
    with allure.step("Send GET request to /users/1"):
        response = client.get("/users/1")
    
    with allure.step("Verify response status is 200"):
        assert response.status_code == 200
    
    with allure.step("Verify user data structure"):
        assert "name" in response.json()
```

#### Severity Levels
- **BLOCKER:** Critical functionality broken
- **CRITICAL:** Major features not working
- **NORMAL:** Standard test cases
- **MINOR:** Edge cases
- **TRIVIAL:** UI/cosmetic issues

#### Attachment Strategy
```python
@pytest.fixture(autouse=True)
def attach_on_failure(request, page):
    yield
    if request.node.rep_call.failed:
        allure.attach(
            page.screenshot(),
            name="failure_screenshot",
            attachment_type=allure.attachment_type.PNG
        )
```

## Data Models

### Allure Result Structure
```json
{
  "uuid": "unique-test-id",
  "name": "test_get_user",
  "fullName": "tests.test_users.test_get_user",
  "status": "passed",
  "statusDetails": {
    "message": "",
    "trace": ""
  },
  "start": 1699999999000,
  "stop": 1700000000000,
  "labels": [
    {"name": "feature", "value": "JSONPlaceholder API"},
    {"name": "story", "value": "User Management"},
    {"name": "severity", "value": "critical"}
  ],
  "steps": [
    {
      "name": "Send GET request to /users/1",
      "status": "passed",
      "start": 1699999999100,
      "stop": 1699999999500
    }
  ],
  "attachments": []
}
```

## Error Handling

### Installation Check
```batch
@echo off
where allure >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Allure CLI not found!
    echo.
    echo Please install Allure:
    echo   1. Using Scoop: scoop install allure
    echo   2. Using npm: npm install -g allure-commandline
    echo   3. Manual: https://docs.qameta.io/allure/#_installing_a_commandline
    exit /b 1
)
```

### Results Validation
```batch
if not exist "reports\allure-results\*.json" (
    echo [WARNING] No test results found!
    echo.
    echo Please run tests first:
    echo   pytest tests/ --alluredir=reports/allure-results
    exit /b 1
)
```

### Generation Failure
```batch
allure generate --clean reports/allure-results -o reports/allure-report
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to generate Allure report
    echo.
    echo Troubleshooting:
    echo   - Check if allure-results contains valid JSON files
    echo   - Try: allure generate --clean reports/allure-results
    echo   - Check Allure version: allure --version
    exit /b 1
)
```

## Testing Strategy

### Validation Tests

1. **Script Functionality Tests**
   - Verify scripts execute without errors
   - Test error handling for missing Allure CLI
   - Test error handling for empty results
   - Verify report generation completes successfully

2. **Report Content Tests**
   - Verify HTML report is generated
   - Check dashboard displays correct statistics
   - Verify test categorization works
   - Confirm attachments are included

3. **Cross-Platform Tests**
   - Test batch scripts on Windows
   - Test shell scripts on Unix/Linux
   - Verify path handling across platforms

### Integration Tests

1. **End-to-End Workflow**
   ```bash
   # Clean old results
   ./scripts/limpar_allure.sh
   
   # Run tests
   pytest tests/jsonplaceholder/ --alluredir=reports/allure-results
   
   # Generate report
   ./scripts/gerar_allure.sh
   
   # Verify report exists
   test -f reports/allure-report/index.html
   ```

2. **Decorator Validation**
   - Run tests with Allure decorators
   - Verify features appear in report
   - Verify severity levels are correct
   - Confirm steps are captured

## Documentation Structure

### ALLURE_QUICK_START.md
**Sections:**
1. O que é Allure?
2. Instalação do Allure CLI
3. Comandos Rápidos
4. Interpretando o Relatório
5. Troubleshooting

### ALLURE_GUIDE.md
**Sections:**
1. Introdução ao Allure
2. Instalação Detalhada
3. Gerando Relatórios
4. Usando Decorators
5. Anexando Evidências
6. Histórico de Execuções
7. Categorização de Falhas
8. Integração CI/CD
9. Melhores Práticas
10. FAQ

## Performance Considerations

### Report Generation Time
- **Target:** < 10 seconds for 1000 tests
- **Optimization:** Use `--clean` flag to avoid incremental builds
- **Caching:** Preserve history for trend analysis

### Storage Management
- **Results:** Keep last 5 executions (~50MB each)
- **Reports:** Keep last 3 generated reports (~20MB each)
- **Cleanup:** Automated cleanup script for old data

## Security Considerations

### Sensitive Data
- Avoid logging credentials in test steps
- Sanitize API responses before attachment
- Use environment variables for secrets

### Report Access
- Reports are local files (no authentication needed)
- For CI/CD: Use artifact storage with access controls
- Consider hosting on internal server with authentication

## Deployment Strategy

### Phase 1: Core Scripts
1. Create generation scripts (Windows + Unix)
2. Test on local environment
3. Document basic usage

### Phase 2: Documentation
1. Write quick start guide
2. Create comprehensive guide
3. Add troubleshooting section

### Phase 3: Test Enhancements
1. Add Allure decorators to critical tests
2. Implement screenshot attachment
3. Add step descriptions

### Phase 4: CI/CD Integration (Future)
1. Add Allure generation to pipeline
2. Publish reports as artifacts
3. Set up trend analysis

## Maintenance Plan

### Regular Tasks
- Update Allure CLI when new versions release
- Review and update categories.json
- Clean old results (monthly)
- Update documentation with new features

### Monitoring
- Track report generation time
- Monitor storage usage
- Collect user feedback on report usefulness
