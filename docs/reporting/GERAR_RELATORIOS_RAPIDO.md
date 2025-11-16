# 🚀 Gerar Relatórios - Guia Rápido

## ⚡ 3 Formas Mais Fáceis

### 1️⃣ Menu Interativo (RECOMENDADO)
```
Duplo clique em: scripts\menu_relatorios.bat
```
Escolha qual relatório quer gerar no menu!

### 2️⃣ Relatório dos Exemplos
```
Duplo clique em: scripts\gerar_relatorio_examples.bat
```
Gera relatório dos testes em `tests/examples/`

### 3️⃣ Relatório Completo
```
Duplo clique em: scripts\gerar_relatorio_completo.bat
```
Gera relatório de TODOS os testes

---

## 💻 Via Linha de Comando

### Último Suite Executado (Examples)
```bash
# Ativar ambiente
.venv\Scripts\activate

# Gerar relatório
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html -v

# Abrir relatório
start reports\relatorio.html
```

### Outros Suites

```bash
# Frontend
python -m pytest tests/frontend/ --html=reports/frontend.html --self-contained-html -v

# API
python -m pytest tests/jsonplaceholder/ --html=reports/api.html --self-contained-html -v

# Integração
python -m pytest tests/integration/ --html=reports/integration.html --self-contained-html -v

# Todos
python -m pytest tests/ --html=reports/completo.html --self-contained-html -v
```

---

## 📊 O Que Você Vai Ver no Relatório

```
┌─────────────────────────────────────────────────────┐
│  Test Report                                        │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Summary                                             │
│  ┌────────────────────────────────────────────┐    │
│  │  Total: 10 tests                            │    │
│  │  ✅ Passed: 8 (80%)                         │    │
│  │  ❌ Failed: 2 (20%)                         │    │
│  │  Duration: 45.2s                            │    │
│  └────────────────────────────────────────────┘    │
│                                                      │
│  Results                                             │
│  ✅ test_abrir_google          2.1s                 │
│  ✅ test_buscar_no_google      3.4s                 │
│  ❌ test_login_invalido        5.2s                 │
│     └─ Error details...                             │
│        [Screenshot] [Logs]                          │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Comandos Rápidos

```bash
# Básico
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html

# Com screenshots
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html --screenshot=on

# Detalhado
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html -v -s

# Abrir automaticamente
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html && start reports\relatorio.html
```

---

## 📁 Onde Ficam os Relatórios

```
reports/
├── relatorio_examples.html      ← Testes de exemplo
├── relatorio_frontend.html      ← Testes de UI
├── relatorio_api.html           ← Testes de API
├── relatorio_integration.html   ← Testes de integração
└── relatorio_completo.html      ← Todos os testes
```

---

## 💡 Dica Rápida

**Quer gerar relatório do que acabou de executar?**

1. Execute os testes normalmente (Test Explorer ou script)
2. Depois execute:
```bash
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html
```

**O relatório abre automaticamente!** 🎉

---

## 🆘 Problemas?

### pytest-html não instalado?
```bash
pip install pytest-html
```

### Relatório não abre?
```bash
start reports\relatorio.html
```

### Quer relatório mais bonito?
```bash
# Instalar Allure
pip install allure-pytest
scoop install allure

# Gerar
python -m pytest tests/examples/ --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## 📚 Documentação Completa

Para mais opções e detalhes, veja:
- **[COMO_GERAR_RELATORIOS.md](COMO_GERAR_RELATORIOS.md)** - Guia completo

---

## 🎉 Resumo

**Forma mais fácil:**
```
Duplo clique em: scripts\menu_relatorios.bat
```

**Forma mais rápida:**
```bash
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html
start reports\relatorio.html
```

**Pronto!** 🚀
