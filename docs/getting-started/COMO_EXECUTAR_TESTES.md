# 🎯 Como Executar Testes - Guia Completo

## 🎨 Opções de Interface Gráfica (SEM linha de comando!)

### ⭐ OPÇÃO 1: Test Explorer do VS Code (MAIS FÁCIL)

**Você já tem isso no VS Code!**

1. Clique no ícone 🧪 **"Testing"** na barra lateral esquerda
2. Clique em **"Refresh Tests"** (ícone 🔄)
3. Clique no ▶️ ao lado de qualquer teste para executar

**Pronto!** O teste vai executar e você verá o resultado com ✅ ou ❌

📖 **Guia detalhado:** [docs/COMO_USAR_TEST_EXPLORER.md](docs/COMO_USAR_TEST_EXPLORER.md)

---

### 🎮 OPÇÃO 2: Playwright UI Mode (MELHOR para Frontend)

**Interface visual incrível para testes de UI!**

**Forma 1: Clique duplo no arquivo**
- Dê duplo clique em: `scripts/run_ui_mode.bat`

**Forma 2: Via linha de comando**
```bash
pytest tests/examples/ --headed --slowmo=500
```

**O que você vai ver:**
- Navegador abrindo automaticamente
- Cada ação acontecendo devagar
- Resultados em tempo real

---

### 📊 OPÇÃO 3: Relatório HTML (BONITO para compartilhar)

**Gera um relatório HTML lindo!**

**Forma 1: Clique duplo no arquivo**
- Dê duplo clique em: `scripts/gerar_relatorio_html.bat`
- O relatório abre automaticamente no navegador

**Forma 2: Via linha de comando**
```bash
pytest tests/examples/ --html=reports/relatorio.html --self-contained-html
start reports/relatorio.html
```

---

## 🚀 Quick Start - Teste AGORA

### Passo 1: Escolha um método

**Método A: VS Code Test Explorer** (Recomendado)
1. Abra VS Code
2. Clique no ícone 🧪 na lateral
3. Clique em "Refresh Tests"
4. Clique no ▶️ ao lado de `test_abrir_google`

**Método B: Duplo Clique**
1. Vá na pasta `scripts`
2. Dê duplo clique em `run_ui_mode.bat`
3. Veja o navegador abrir e executar os testes

**Método C: Relatório HTML**
1. Dê duplo clique em `scripts/gerar_relatorio_html.bat`
2. Veja o relatório abrir no navegador

---

## 📁 Estrutura de Testes

```
tests/
├── examples/              ⭐ COMECE AQUI
│   ├── test_exemplo_basico.py      # Testes super simples
│   ├── test_google_search.py       # Exemplos com Google
│   └── test_wikipedia.py           # Exemplo avançado
│
├── frontend/              # Testes de UI da sua aplicação
│   ├── test_login.py
│   ├── test_user_journey.py
│   └── test_ui_backend_db_integration.py
│
└── jsonplaceholder/       # Testes de API
    ├── test_users.py
    ├── test_posts.py
    └── test_comments.py
```

---

## 🎯 Executando Testes Específicos

### No Test Explorer (VS Code)

```
📁 tests
  📁 examples
    📄 test_exemplo_basico.py
      ▶️ test_abrir_google          ← Clique aqui para executar só este
      ▶️ test_buscar_no_google
```

### Via Linha de Comando

```bash
# Executar um teste específico
pytest tests/examples/test_exemplo_basico.py::test_abrir_google -v --headed

# Executar todos os testes de uma pasta
pytest tests/examples/ -v --headed

# Executar testes que contém "google" no nome
pytest tests/examples/ -k "google" -v --headed
```

---

## 🎨 Opções de Visualização

### Modo Headed (Ver o navegador)
```bash
pytest tests/examples/ --headed
```

### Modo Lento (Ver as ações)
```bash
pytest tests/examples/ --headed --slowmo=1000
```

### Modo Debug (Pausar e inspecionar)
```python
def test_exemplo(page):
    page.goto("https://google.com")
    page.pause()  # ← Pausa aqui para você inspecionar
```

---

## 📊 Tipos de Relatórios

### 1. Console (Padrão)
```bash
pytest tests/examples/ -v
```
Mostra resultados no terminal

### 2. HTML Report
```bash
pytest tests/examples/ --html=reports/report.html --self-contained-html
start reports/report.html
```
Relatório HTML bonito

### 3. Allure Report (Profissional)
```bash
# Instalar Allure primeiro
pip install allure-pytest
scoop install allure

# Gerar relatório
pytest tests/examples/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## 🎓 Exemplos Práticos

### Exemplo 1: Teste Simples no Google

**Via Test Explorer:**
1. Abra Test Explorer (🧪)
2. Navegue até: `tests/examples/test_exemplo_basico.py`
3. Clique no ▶️ ao lado de `test_buscar_no_google`
4. Veja o navegador abrir e fazer a busca!

**Via Script:**
```bash
pytest tests/examples/test_exemplo_basico.py::test_buscar_no_google -v --headed --slowmo=1000
```

### Exemplo 2: Todos os Testes de Exemplo

**Via Test Explorer:**
1. Clique no ▶️ ao lado da pasta `examples`

**Via Script:**
```bash
# Duplo clique em:
scripts/run_ui_mode.bat
```

### Exemplo 3: Gerar Relatório

**Via Script:**
```bash
# Duplo clique em:
scripts/gerar_relatorio_html.bat
```

---

## 🐛 Debug de Testes

### Opção 1: VS Code Debug

1. Coloque um breakpoint (F9) no código do teste
2. Clique com botão direito no teste
3. Selecione "Debug Test"
4. Use F10 (step over), F11 (step into), F5 (continue)

### Opção 2: Playwright Inspector

```python
def test_exemplo(page):
    page.goto("https://google.com")
    page.pause()  # ← Abre o Playwright Inspector
```

### Opção 3: Screenshots

```python
def test_exemplo(page):
    page.goto("https://google.com")
    page.screenshot(path="debug.png")  # Salva screenshot
```

---

## 💡 Dicas Importantes

### ✅ Para Aprender
- Use `--headed` para ver o navegador
- Use `--slowmo=1000` para ver as ações devagar
- Use Test Explorer do VS Code - é o mais fácil!

### ✅ Para Desenvolvimento
- Use Test Explorer para executar testes rapidamente
- Use `page.pause()` para debug
- Capture screenshots em falhas

### ✅ Para Compartilhar
- Gere relatórios HTML
- Use Allure para relatórios profissionais
- Compartilhe a pasta `reports/`

---

## 🆘 Problemas Comuns

### Test Explorer não mostra testes?

1. Clique em "Refresh Tests" (🔄)
2. Verifique se pytest está instalado: `pip list | grep pytest`
3. Veja o Output: `View` → `Output` → "Python Test Log"

### Navegador não abre?

Adicione `--headed` nos argumentos:
- No Test Explorer: Edite `.vscode/settings.json`
- Na linha de comando: `pytest --headed`

### Testes muito rápidos?

Use `--slowmo`:
```bash
pytest tests/examples/ --headed --slowmo=2000
```

### Quer pausar o teste?

Adicione no código:
```python
page.pause()
```

---

## 📚 Documentação Completa

- **Test Explorer:** [docs/COMO_USAR_TEST_EXPLORER.md](docs/COMO_USAR_TEST_EXPLORER.md)
- **Interfaces Gráficas:** [docs/INTERFACES_GRAFICAS_TESTES.md](docs/INTERFACES_GRAFICAS_TESTES.md)
- **Exemplos de Testes:** [tests/examples/README.md](tests/examples/README.md)
- **Guia Rápido Playwright:** [tests/examples/GUIA_RAPIDO.md](tests/examples/GUIA_RAPIDO.md)

---

## 🎉 Comece Agora!

**Opção Mais Fácil:**
1. Abra VS Code
2. Clique no ícone 🧪 (Testing)
3. Clique em "Refresh Tests"
4. Clique no ▶️ ao lado de qualquer teste

**Ou simplesmente:**
- Dê duplo clique em `scripts/run_ui_mode.bat`

**Pronto! Você está executando testes sem linha de comando!** 🚀
