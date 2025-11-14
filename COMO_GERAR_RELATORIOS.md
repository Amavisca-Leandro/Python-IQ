# 📊 Como Gerar Relatórios de Testes

## 🚀 Formas Rápidas (Duplo Clique)

### 1. Relatório dos Testes de Exemplo
```
Duplo clique em: scripts\gerar_relatorio_examples.bat
```
Gera relatório apenas dos testes em `tests/examples/`

### 2. Relatório Completo (Todos os Testes)
```
Duplo clique em: scripts\gerar_relatorio_completo.bat
```
Gera relatório de TODOS os testes do projeto

### 3. Relatório Personalizado
```
Duplo clique em: scripts\gerar_relatorio_html.bat
```
Gera relatório configurável

---

## 💻 Via Linha de Comando

### Relatório de uma Suite Específica

```bash
# Ativar ambiente virtual
.venv\Scripts\activate

# Testes de exemplo
python -m pytest tests/examples/ --html=reports/examples.html --self-contained-html -v

# Testes de frontend
python -m pytest tests/frontend/ --html=reports/frontend.html --self-contained-html -v

# Testes de API
python -m pytest tests/jsonplaceholder/ --html=reports/api.html --self-contained-html -v

# Testes de integração
python -m pytest tests/integration/ --html=reports/integration.html --self-contained-html -v
```

### Relatório de um Arquivo Específico

```bash
# Apenas test_exemplo_basico.py
python -m pytest tests/examples/test_exemplo_basico.py --html=reports/basico.html --self-contained-html -v

# Apenas test_google_search.py
python -m pytest tests/examples/test_google_search.py --html=reports/google.html --self-contained-html -v
```

### Relatório de um Teste Específico

```bash
# Apenas o teste test_abrir_google
python -m pytest tests/examples/test_exemplo_basico.py::test_abrir_google --html=reports/google_test.html --self-contained-html -v
```

---

## 🎨 Opções de Relatório

### Relatório Básico
```bash
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html
```

### Relatório com Screenshots
```bash
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html --screenshot=on
```

### Relatório com Vídeos
```bash
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html --video=on
```

### Relatório Detalhado (verbose)
```bash
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html -v -s
```

### Relatório com Tempo de Execução
```bash
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html --durations=10
```

---

## 📋 Tipos de Relatório

### 1. HTML Report (pytest-html)

**Instalar:**
```bash
pip install pytest-html
```

**Gerar:**
```bash
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html
```

**Vantagens:**
- ✅ Fácil de usar
- ✅ Um único arquivo HTML
- ✅ Pode compartilhar por email
- ✅ Screenshots incluídos

### 2. Allure Report (Profissional)

**Instalar:**
```bash
pip install allure-pytest
scoop install allure
```

**Gerar:**
```bash
# Executar testes e gerar dados
python -m pytest tests/examples/ --alluredir=reports/allure-results

# Gerar e abrir relatório
allure serve reports/allure-results
```

**Vantagens:**
- ✅ Muito profissional
- ✅ Gráficos e estatísticas
- ✅ Histórico de execuções
- ✅ Categorização de falhas

### 3. JUnit XML (Para CI/CD)

**Gerar:**
```bash
python -m pytest tests/examples/ --junitxml=reports/junit.xml
```

**Vantagens:**
- ✅ Padrão da indústria
- ✅ Integra com Jenkins, GitLab CI, etc.
- ✅ Formato XML estruturado

---

## 🎯 Exemplos Práticos

### Exemplo 1: Relatório Rápido dos Exemplos

```bash
# Forma mais rápida
python -m pytest tests/examples/ --html=reports/examples.html --self-contained-html -v
start reports\examples.html
```

### Exemplo 2: Relatório com Screenshots de Falhas

```bash
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html --screenshot=only-on-failure
start reports\relatorio.html
```

### Exemplo 3: Relatório Completo do Projeto

```bash
python -m pytest tests/ --html=reports/completo.html --self-contained-html -v --tb=short
start reports\completo.html
```

### Exemplo 4: Relatório Apenas de Testes Falhados

```bash
# Primeira execução
python -m pytest tests/examples/ --html=reports/primeira.html --self-contained-html

# Re-executar apenas os que falharam
python -m pytest tests/examples/ --lf --html=reports/falhados.html --self-contained-html
```

---

## 📊 Personalizar Relatório HTML

### Adicionar Título Customizado

Crie arquivo `conftest.py` na raiz:

```python
import pytest

def pytest_html_report_title(report):
    report.title = "Relatório de Testes - Meu Projeto"
```

### Adicionar Informações Extras

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call':
        # Adicionar informações extras
        extra = getattr(report, 'extra', [])
        if report.failed:
            extra.append(pytest_html.extras.text('Teste falhou!', name='Status'))
        report.extra = extra
```

---

## 🔧 Configuração Permanente

### No arquivo pytest.ini

```ini
[pytest]
addopts = 
    --html=reports/relatorio.html
    --self-contained-html
    -v
    --tb=short
```

Agora basta executar:
```bash
python -m pytest tests/examples/
```

---

## 📁 Organização de Relatórios

### Estrutura Recomendada

```
reports/
├── examples/
│   ├── relatorio_2024-01-15.html
│   └── relatorio_2024-01-16.html
├── frontend/
│   └── relatorio_ui.html
├── api/
│   └── relatorio_api.html
└── completo/
    └── relatorio_completo.html
```

### Script para Organizar por Data

```bash
# Gerar com data no nome
python -m pytest tests/examples/ --html=reports/examples/relatorio_%date:~-4,4%-%date:~-7,2%-%date:~-10,2%.html --self-contained-html
```

---

## 🎨 Relatórios Avançados

### 1. Relatório com Métricas de Performance

```bash
python -m pytest tests/examples/ --html=reports/performance.html --self-contained-html --durations=0
```

### 2. Relatório com Coverage (Cobertura de Código)

```bash
pip install pytest-cov
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html --cov=core --cov-report=html
```

### 3. Relatório Paralelo (Mais Rápido)

```bash
pip install pytest-xdist
python -m pytest tests/examples/ -n auto --html=reports/relatorio.html --self-contained-html
```

---

## 💡 Dicas

### ✅ Sempre use --self-contained-html
Gera um único arquivo que pode ser compartilhado facilmente

### ✅ Use nomes descritivos
```bash
# Bom
--html=reports/testes_google_2024-01-15.html

# Ruim
--html=report.html
```

### ✅ Adicione -v para mais detalhes
```bash
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html -v
```

### ✅ Use --tb=short para tracebacks menores
```bash
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html --tb=short
```

---

## 🆘 Problemas Comuns

### Relatório não abre automaticamente?

```bash
# Abrir manualmente
start reports\relatorio.html

# Ou no navegador padrão
python -m webbrowser reports\relatorio.html
```

### Relatório muito grande?

```bash
# Executar apenas testes rápidos
python -m pytest tests/examples/ -m "not slow" --html=reports/relatorio.html --self-contained-html
```

### Quer relatório sem executar testes?

```bash
# Apenas coletar informações
python -m pytest tests/examples/ --collect-only
```

---

## 📞 Comandos Rápidos

```bash
# Relatório básico
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html

# Relatório + abrir
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html && start reports\relatorio.html

# Relatório completo
python -m pytest tests/ --html=reports/completo.html --self-contained-html -v

# Relatório com screenshots
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html --screenshot=on

# Relatório Allure
python -m pytest tests/examples/ --alluredir=reports/allure-results && allure serve reports/allure-results
```

---

## 🎉 Resumo - Forma Mais Fácil

**Para gerar relatório do último suite que você executou:**

### Opção 1: Duplo Clique
```
scripts\gerar_relatorio_examples.bat
```

### Opção 2: Linha de Comando
```bash
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html -v
start reports\relatorio.html
```

### Opção 3: No Test Explorer
1. Execute os testes normalmente
2. Depois execute via terminal:
```bash
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html
```

**O relatório abre automaticamente no navegador!** 🎯
