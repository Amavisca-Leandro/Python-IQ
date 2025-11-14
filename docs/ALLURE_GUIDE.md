# Guia Completo - Allure Reports

## 📑 Índice

1. [Introdução ao Allure](#introdução-ao-allure)
2. [Instalação e Configuração](#instalação-e-configuração)
3. [Scripts de Geração](#scripts-de-geração)
4. [Decoradores Allure](#decoradores-allure)
5. [Interpretando Relatórios](#interpretando-relatórios)
6. [Recursos Avançados](#recursos-avançados)
7. [Integração CI/CD](#integração-cicd)
8. [Boas Práticas](#boas-práticas)
9. [FAQ](#faq)

---

## Introdução ao Allure

### O que é Allure?

Allure Framework é uma ferramenta de relatórios de testes flexível e leve que não apenas mostra uma representação muito concisa do que foi testado, mas também permite que todos os envolvidos no processo de desenvolvimento extraiam o máximo de informações úteis dos testes executados diariamente.

### Benefícios

- **Visual e Interativo:** Relatórios HTML modernos com gráficos e dashboards
- **Detalhamento Completo:** Cada teste mostra steps, anexos, tempo de execução
- **Categorização Automática:** Falhas são classificadas automaticamente
- **Histórico e Tendências:** Acompanhe a evolução dos testes ao longo do tempo
- **Integração Fácil:** Funciona com Pytest, JUnit, TestNG, Cucumber, etc.
- **Multiplataforma:** Windows, Linux, macOS

### Arquitetura

```
Testes (Pytest) 
    ↓
Allure Results (JSON)
    ↓
Allure CLI
    ↓
Relatório HTML
```

---

## Instalação e Configuração

### Instalação do Allure CLI

#### Windows

```cmd
# Método 1: Scoop (recomendado)
scoop install allure

# Método 2: npm
npm install -g allure-commandline

# Método 3: Download manual
# Baixe de: https://github.com/allure-framework/allure2/releases
# Extraia e adicione ao PATH
```

#### macOS

```bash
# Homebrew
brew install allure
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

### Instalação do Plugin Pytest

```bash
pip install allure-pytest
```

### Configuração do Projeto

O projeto já está configurado com:

**pytest.ini:**
```ini
[pytest]
addopts =
    --alluredir=reports/allure-results
    --clean-alluredir
```

**Estrutura de Diretórios:**
```
project/
├── reports/
│   ├── allure-results/      # Resultados JSON dos testes
│   │   ├── categories.json  # Categorias de falhas
│   │   └── environment.properties  # Metadados do ambiente
│   └── allure-report/       # Relatório HTML gerado
├── scripts/
│   ├── gerar_allure.bat     # Gerar relatório (Windows)
│   ├── gerar_allure.sh      # Gerar relatório (Unix)
│   ├── allure_server.bat    # Servidor Allure (Windows)
│   ├── allure_server.sh     # Servidor Allure (Unix)
│   ├── limpar_allure.bat    # Limpar resultados (Windows)
│   └── limpar_allure.sh     # Limpar resultados (Unix)
└── tests/
```

---

## Scripts de Geração

### gerar_allure (Windows/Unix)

Gera relatório HTML estático e abre no navegador.

**Uso:**
```bash
# Windows
scripts\gerar_allure.bat

# Unix/Linux/macOS
scripts/gerar_allure.sh
```

**O que faz:**
1. Verifica instalação do Allure CLI
2. Valida existência de resultados
3. Gera relatório com `allure generate --clean`
4. Abre automaticamente no navegador

### allure_server (Windows/Unix)

Inicia servidor local com live reload na porta 4040.

**Uso:**
```bash
# Windows
scripts\allure_server.bat

# Unix/Linux/macOS
scripts/allure_server.sh
```

**O que faz:**
1. Verifica instalação do Allure CLI
2. Valida existência de resultados
3. Inicia servidor em http://localhost:4040
4. Abre automaticamente no navegador
5. Mantém servidor rodando até Ctrl+C

**Vantagens:**
- Live reload: atualiza automaticamente quando novos testes são executados
- Não precisa regenerar o relatório manualmente

### limpar_allure (Windows/Unix)

Limpa resultados e relatórios antigos.

**Uso:**
```bash
# Windows
scripts\limpar_allure.bat

# Unix/Linux/macOS
scripts/limpar_allure.sh
```

**O que faz:**
1. Solicita confirmação do usuário
2. Remove todos os arquivos de `allure-results/`
3. Remove todos os arquivos de `allure-report/`
4. Exibe resumo da limpeza

---

## Decoradores Allure

### @allure.feature()

Agrupa testes por funcionalidade/feature.

**Exemplo:**
```python
import allure

@allure.feature("JSONPlaceholder API")
class TestUsers:
    def test_get_users(self):
        pass
```

### @allure.story()

Agrupa testes por user story dentro de uma feature.

**Exemplo:**
```python
import allure

@allure.feature("User Management")
class TestUsers:
    
    @allure.story("Create User")
    def test_create_user(self):
        pass
    
    @allure.story("Update User")
    def test_update_user(self):
        pass
```

### @allure.severity()

Define a severidade/criticidade do teste.

**Níveis:**
- `allure.severity_level.BLOCKER` - Bloqueia funcionalidade crítica
- `allure.severity_level.CRITICAL` - Funcionalidade crítica
- `allure.severity_level.NORMAL` - Funcionalidade normal (padrão)
- `allure.severity_level.MINOR` - Funcionalidade menor
- `allure.severity_level.TRIVIAL` - Funcionalidade trivial

**Exemplo:**
```python
import allure

@allure.severity(allure.severity_level.CRITICAL)
def test_user_login(self):
    pass

@allure.severity(allure.severity_level.MINOR)
def test_ui_color_scheme(self):
    pass
```

### allure.step()

Adiciona steps detalhados ao teste.

**Exemplo:**
```python
import allure

def test_user_registration():
    with allure.step("Abrir página de registro"):
        page.goto("/register")
    
    with allure.step("Preencher formulário"):
        page.fill("#name", "João Silva")
        page.fill("#email", "joao@example.com")
    
    with allure.step("Submeter formulário"):
        page.click("#submit")
    
    with allure.step("Verificar sucesso"):
        assert page.locator(".success").is_visible()
```

### @allure.title()

Define título customizado para o teste.

**Exemplo:**
```python
import allure

@allure.title("Validar criação de usuário com dados válidos")
def test_create_user_valid_data(self):
    pass

# Com parâmetros dinâmicos
@allure.title("Criar usuário: {name}")
def test_create_user(self, name):
    pass
```

### @allure.description()

Adiciona descrição detalhada ao teste.

**Exemplo:**
```python
import allure

@allure.description("""
Este teste valida o fluxo completo de criação de usuário:
1. Envia requisição POST com dados válidos
2. Verifica status code 201
3. Valida estrutura da resposta
4. Confirma que o usuário foi criado no banco
""")
def test_create_user(self):
    pass
```

### allure.attach()

Anexa arquivos, screenshots, logs ao relatório.

**Exemplo:**
```python
import allure

def test_api_response(self):
    response = requests.get("https://api.example.com/users")
    
    # Anexar JSON
    allure.attach(
        response.text,
        name="API Response",
        attachment_type=allure.attachment_type.JSON
    )
    
    # Anexar screenshot
    screenshot = page.screenshot()
    allure.attach(
        screenshot,
        name="Page Screenshot",
        attachment_type=allure.attachment_type.PNG
    )
```

**Tipos de anexo:**
- `allure.attachment_type.TEXT`
- `allure.attachment_type.JSON`
- `allure.attachment_type.XML`
- `allure.attachment_type.HTML`
- `allure.attachment_type.PNG`
- `allure.attachment_type.JPG`
- `allure.attachment_type.PDF`

### @allure.link() e @allure.issue()

Adiciona links para documentação, issues, etc.

**Exemplo:**
```python
import allure

@allure.link("https://docs.example.com/api", name="API Documentation")
@allure.issue("JIRA-123", "Bug no endpoint de usuários")
def test_users_endpoint(self):
    pass
```

### Exemplo Completo

```python
import allure
import pytest

@allure.feature("User Management")
class TestUserCRUD:
    
    @allure.story("Create User")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Criar usuário com dados válidos")
    @allure.description("Valida criação de usuário via API")
    @allure.link("https://docs.api.com/users", name="API Docs")
    def test_create_user(self, api_client):
        with allure.step("Preparar dados do usuário"):
            user_data = {
                "name": "João Silva",
                "email": "joao@example.com"
            }
        
        with allure.step("Enviar requisição POST"):
            response = api_client.post("/users", json=user_data)
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Validar resposta"):
            assert response.status_code == 201
            assert response.json()["name"] == user_data["name"]
```

---

## Interpretando Relatórios

### Dashboard (Overview)

O dashboard principal mostra:

- **Total de testes:** Passed, Failed, Broken, Skipped
- **Gráfico de pizza:** Distribuição visual dos resultados
- **Severidade:** Distribuição por criticidade
- **Duração:** Tempo total de execução
- **Tendências:** Comparação com execuções anteriores

### Suites

Agrupa testes por arquivo/módulo de teste.

### Graphs

- **Status Chart:** Distribuição de status
- **Severity Chart:** Distribuição por severidade
- **Duration Chart:** Testes mais lentos
- **Retry Trend:** Tentativas de retry

### Timeline

Visualização temporal da execução dos testes, mostrando:
- Quando cada teste foi executado
- Duração de cada teste
- Testes executados em paralelo

### Behaviors

Agrupa testes por Features e Stories (usando decoradores).

### Packages

Agrupa testes por estrutura de pacotes Python.

### Categories

Classificação automática de falhas baseada em `categories.json`:
- Product Defects
- Test Defects
- Timeout Issues
- Connection Issues
- Element Not Found
- Authentication Failures
- Database Issues
- Ignored Tests

---

## Recursos Avançados

### Histórico e Tendências

Para habilitar histórico:

```bash
# Copiar histórico da execução anterior
cp -r reports/allure-report/history reports/allure-results/history

# Gerar novo relatório (mantém histórico)
allure generate reports/allure-results -o reports/allure-report
```

### Categorias Personalizadas

Edite `reports/allure-results/categories.json`:

```json
[
  {
    "name": "Minha Categoria",
    "description": "Descrição da categoria",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*padrão de erro.*"
  }
]
```

### Environment Properties

Edite `reports/allure-results/environment.properties`:

```properties
Environment=Production
Browser=Chrome
Version=1.2.3
```

### Retries

Configure retries no pytest:

```python
# conftest.py
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if hasattr(item, "_allure_retry"):
            item._allure_retry += 1
        else:
            item._allure_retry = 1
```

---

## Integração CI/CD

### GitHub Actions

```yaml
name: Tests with Allure

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/ --alluredir=reports/allure-results
    
    - name: Get Allure history
      uses: actions/checkout@v3
      if: always()
      continue-on-error: true
      with:
        ref: gh-pages
        path: gh-pages
    
    - name: Allure Report
      uses: simple-elf/allure-report-action@master
      if: always()
      with:
        allure_results: reports/allure-results
        allure_history: allure-history
        keep_reports: 20
    
    - name: Deploy to GitHub Pages
      if: always()
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_branch: gh-pages
        publish_dir: allure-history
```

### GitLab CI

```yaml
stages:
  - test
  - report

test:
  stage: test
  script:
    - pip install -r requirements.txt
    - pytest tests/ --alluredir=reports/allure-results
  artifacts:
    paths:
      - reports/allure-results
    expire_in: 1 week

allure:
  stage: report
  image: frankescobar/allure-docker-service
  script:
    - allure generate reports/allure-results -o reports/allure-report
  artifacts:
    paths:
      - reports/allure-report
    expire_in: 1 month
  only:
    - main
```

### Jenkins

```groovy
pipeline {
    agent any
    
    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest tests/ --alluredir=reports/allure-results'
            }
        }
        
        stage('Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'reports/allure-results']]
                ])
            }
        }
    }
}
```

---

## Boas Práticas

### 1. Use Decoradores Consistentemente

```python
# ✅ BOM
@allure.feature("User Management")
@allure.story("Create User")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_user():
    pass

# ❌ RUIM
def test_create_user():
    pass
```

### 2. Adicione Steps Significativos

```python
# ✅ BOM
with allure.step("Fazer login com credenciais válidas"):
    login(username, password)

# ❌ RUIM
login(username, password)
```

### 3. Anexe Informações Relevantes

```python
# ✅ BOM - Anexa response em caso de falha
response = api.get("/users")
if response.status_code != 200:
    allure.attach(response.text, "Error Response", allure.attachment_type.JSON)

# ❌ RUIM - Não anexa informações de debug
response = api.get("/users")
assert response.status_code == 200
```

### 4. Use Severidade Apropriada

- **BLOCKER:** Sistema não funciona
- **CRITICAL:** Funcionalidade principal quebrada
- **NORMAL:** Funcionalidade secundária
- **MINOR:** UI/UX issues
- **TRIVIAL:** Typos, formatação

### 5. Organize por Features e Stories

```python
@allure.feature("E-commerce")
class TestCheckout:
    
    @allure.story("Add to Cart")
    def test_add_product_to_cart(self):
        pass
    
    @allure.story("Payment")
    def test_process_payment(self):
        pass
```

### 6. Mantenha Histórico

```bash
# Antes de gerar novo relatório
cp -r reports/allure-report/history reports/allure-results/history
```

### 7. Configure Categories Personalizadas

Adapte `categories.json` para os tipos de falhas do seu projeto.

---

## FAQ

### Como adicionar screenshots automaticamente em falhas?

```python
# conftest.py
import allure
import pytest

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="Screenshot on Failure",
                attachment_type=allure.attachment_type.PNG
            )
```

### Como executar apenas testes de uma severidade?

```bash
pytest -m "allure.severity_level.CRITICAL"
```

### Como limpar histórico antigo?

```bash
rm -rf reports/allure-report/history
```

### Relatório não mostra testes

**Causas comuns:**
1. `allure-pytest` não instalado: `pip install allure-pytest`
2. `--alluredir` não configurado no pytest.ini
3. Testes não foram executados antes de gerar relatório

### Como integrar com Jira?

Use `@allure.issue()`:

```python
@allure.issue("PROJ-123", "Bug description")
def test_something():
    pass
```

Configure link pattern no Allure:
```bash
allure generate --clean reports/allure-results \
  --issue-pattern https://jira.company.com/browse/%s
```

### Posso usar Allure com outros frameworks?

Sim! Allure suporta:
- Pytest (Python)
- JUnit (Java)
- TestNG (Java)
- Cucumber (BDD)
- Jest (JavaScript)
- Mocha (JavaScript)
- PHPUnit (PHP)
- NUnit (C#)

---

## 🔗 Recursos Adicionais

- [Documentação Oficial](https://docs.qameta.io/allure/)
- [Allure Pytest Plugin](https://docs.qameta.io/allure/#_pytest)
- [Demo Report](https://demo.qameta.io/allure/)
- [GitHub Allure2](https://github.com/allure-framework/allure2)
- [Guia Rápido](ALLURE_QUICK_START.md)
