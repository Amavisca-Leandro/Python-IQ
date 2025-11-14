# Guia Rápido - Allure Reports

## 📊 O que é Allure?

Allure é um framework de relatórios de testes que gera relatórios HTML interativos e visualmente atraentes. Ele transforma resultados de testes em relatórios detalhados com:

- 📈 Dashboard com estatísticas e gráficos
- 🎯 Categorização automática de falhas
- 📝 Histórico de execuções e tendências
- 🔍 Detalhamento de cada teste com steps
- 📸 Anexos (screenshots, logs, vídeos)
- ⏱️ Métricas de tempo e performance

## 🚀 Instalação Rápida

### Windows

```cmd
# Usando Scoop (recomendado)
scoop install allure

# Usando npm
npm install -g allure-commandline
```

### macOS

```bash
# Usando Homebrew
brew install allure
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

### Verificar Instalação

```bash
allure --version
```

## ⚡ Comandos Essenciais

### 1. Executar Testes e Gerar Resultados

```bash
# Executar todos os testes
pytest tests/ --alluredir=reports/allure-results

# Executar testes específicos
pytest tests/jsonplaceholder/ --alluredir=reports/allure-results

# Executar com marcadores
pytest -m smoke --alluredir=reports/allure-results
```

### 2. Gerar Relatório HTML (Método Fácil)

**Windows:**
```cmd
cd scripts
gerar_allure.bat
```

**Unix/Linux/macOS:**
```bash
cd scripts
chmod +x gerar_allure.sh  # Apenas primeira vez
./gerar_allure.sh
```

### 3. Iniciar Servidor Allure (Método Fácil)

**Windows:**
```cmd
cd scripts
allure_server.bat
```

**Unix/Linux/macOS:**
```bash
cd scripts
chmod +x allure_server.sh  # Apenas primeira vez
./allure_server.sh
```

### 4. Limpar Resultados Antigos

**Windows:**
```cmd
cd scripts
limpar_allure.bat
```

**Unix/Linux/macOS:**
```bash
cd scripts
chmod +x limpar_allure.sh  # Apenas primeira vez
./limpar_allure.sh
```

## 🎯 Workflow Básico

```bash
# 1. Limpar resultados antigos (opcional)
scripts/limpar_allure.bat

# 2. Executar testes
pytest tests/ --alluredir=reports/allure-results

# 3. Gerar e visualizar relatório
scripts/gerar_allure.bat
# OU iniciar servidor com live reload
scripts/allure_server.bat
```

## 🔧 Comandos Allure CLI (Avançado)

```bash
# Gerar relatório estático
allure generate --clean reports/allure-results -o reports/allure-report

# Abrir relatório existente
allure open reports/allure-report

# Iniciar servidor (porta padrão 4040)
allure serve reports/allure-results -p 4040

# Limpar relatório antigo
allure generate --clean reports/allure-results
```

## 🐛 Solução de Problemas Rápida

### "Allure CLI not found"
- **Solução:** Instale o Allure CLI usando um dos métodos acima
- **Verificar:** `allure --version`

### "No test results found"
- **Solução:** Execute os testes primeiro: `pytest tests/ --alluredir=reports/allure-results`
- **Verificar:** Confira se existe a pasta `reports/allure-results` com arquivos `.json`

### "Permission denied" (Unix/Linux/macOS)
- **Solução:** Torne os scripts executáveis: `chmod +x scripts/*.sh`

### "Port 4040 already in use"
- **Solução:** Pare o servidor Allure existente (Ctrl+C) ou mude a porta no script

### Relatório vazio ou sem testes
- **Causa:** Testes não geraram resultados Allure
- **Solução:** Certifique-se que `pytest-allure` está instalado: `pip install allure-pytest`
- **Verificar:** `pytest.ini` deve ter `--alluredir=reports/allure-results`

## 📚 Próximos Passos

- Leia o [Guia Completo do Allure](ALLURE_GUIDE.md) para recursos avançados
- Aprenda sobre [decoradores Allure](ALLURE_GUIDE.md#decoradores-allure) para melhorar seus relatórios
- Configure [categorias personalizadas](ALLURE_GUIDE.md#categorias-de-falhas) para classificação automática

## 🔗 Links Úteis

- [Documentação Oficial Allure](https://docs.qameta.io/allure/)
- [Allure Pytest Plugin](https://docs.qameta.io/allure/#_pytest)
- [Exemplos de Relatórios](https://demo.qameta.io/allure/)
