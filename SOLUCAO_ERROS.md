# 🔧 Solução de Erros Comuns

## ❌ Erro: "file or directory not found: tests/examples/"

### Causa
O script não está encontrando a pasta de testes.

### Solução 1: Use o caminho correto

Execute o script a partir da raiz do projeto:

```bash
# Certifique-se de estar na pasta raiz do projeto
cd C:\projects\python-iq

# Execute o script
scripts\run_ui_mode.bat
```

### Solução 2: Execute direto com pytest

```bash
# Ative o ambiente virtual
.venv\Scripts\activate

# Execute os testes
python -m pytest tests/examples/ --headed --slowmo=1000 -v
```

### Solução 3: Use o script simples

Criamos um script mais simples para você:

```bash
# Duplo clique em:
scripts\testar_google.bat
```

---

## ❌ Erro: "pytest not installed"

### Solução

```bash
# Ative o ambiente virtual
.venv\Scripts\activate

# Instale pytest
pip install pytest pytest-playwright

# Instale os navegadores
playwright install chromium
```

---

## ❌ Erro: "No module named 'playwright'"

### Solução

```bash
# Ative o ambiente virtual
.venv\Scripts\activate

# Instale playwright
pip install playwright pytest-playwright

# Instale os navegadores
playwright install
```

---

## ❌ Navegador não abre

### Solução 1: Instalar navegadores

```bash
playwright install chromium
```

### Solução 2: Verificar se está usando --headed

```bash
pytest tests/examples/ --headed
```

---

## ❌ Testes não aparecem no Test Explorer

### Solução 1: Refresh

1. Clique no ícone 🔄 "Refresh Tests" no Test Explorer

### Solução 2: Verificar interpretador Python

1. Pressione `Ctrl+Shift+P`
2. Digite "Python: Select Interpreter"
3. Selecione o interpretador do `.venv`

### Solução 3: Reinstalar pytest

```bash
.venv\Scripts\activate
pip uninstall pytest pytest-playwright
pip install pytest pytest-playwright
```

---

## 🎯 Teste Rápido - Verificar se está tudo OK

Execute estes comandos para verificar:

```bash
# 1. Ativar ambiente virtual
.venv\Scripts\activate

# 2. Verificar pytest
python -m pytest --version

# 3. Verificar playwright
playwright --version

# 4. Listar testes
python -m pytest tests/examples/ --collect-only

# 5. Executar um teste simples
python -m pytest tests/examples/test_exemplo_basico.py::test_abrir_google --headed -v
```

Se todos os comandos funcionarem, está tudo OK! ✅

---

## 🚀 Forma Mais Fácil de Executar

### Opção 1: Test Explorer do VS Code

1. Abra VS Code
2. Clique no ícone 🧪 (Testing)
3. Clique em 🔄 (Refresh)
4. Clique no ▶️ ao lado de qualquer teste

### Opção 2: Script Simples

```bash
# Duplo clique em:
scripts\testar_google.bat
```

### Opção 3: Linha de Comando

```bash
# Na raiz do projeto
python -m pytest tests/examples/test_exemplo_basico.py --headed -v
```

---

## 📝 Checklist de Instalação

Verifique se você tem tudo instalado:

- [ ] Python 3.11+ instalado
- [ ] Ambiente virtual criado (`.venv`)
- [ ] Ambiente virtual ativado
- [ ] pytest instalado: `pip list | grep pytest`
- [ ] playwright instalado: `pip list | grep playwright`
- [ ] Navegadores instalados: `playwright install chromium`

---

## 🆘 Ainda com Problemas?

### Reinstalação Completa

```bash
# 1. Deletar ambiente virtual
rmdir /s /q .venv

# 2. Criar novo ambiente
python -m venv .venv

# 3. Ativar
.venv\Scripts\activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Instalar navegadores
playwright install chromium

# 6. Testar
python -m pytest tests/examples/test_exemplo_basico.py::test_abrir_google --headed -v
```

---

## 💡 Dicas

### Sempre execute a partir da raiz do projeto

```bash
# ERRADO (dentro de scripts/)
cd scripts
run_ui_mode.bat

# CERTO (na raiz)
cd C:\projects\python-iq
scripts\run_ui_mode.bat
```

### Use python -m pytest ao invés de pytest

```bash
# Mais confiável
python -m pytest tests/examples/ --headed

# Pode dar erro se PATH não estiver configurado
pytest tests/examples/ --headed
```

### Verifique o ambiente virtual

```bash
# Ver qual Python está sendo usado
where python

# Deve mostrar algo como:
# C:\projects\python-iq\.venv\Scripts\python.exe
```

---

## 📞 Comandos Úteis para Debug

```bash
# Ver versões instaladas
python --version
python -m pytest --version
playwright --version

# Ver pacotes instalados
pip list

# Ver onde está o Python
where python

# Listar testes sem executar
python -m pytest tests/examples/ --collect-only

# Executar com mais informações
python -m pytest tests/examples/ --headed -v -s

# Ver ajuda do pytest
python -m pytest --help
```

---

## ✅ Teste de Verificação Final

Execute este comando para ter certeza que está tudo funcionando:

```bash
python -m pytest tests/examples/test_exemplo_basico.py::test_abrir_google --headed --slowmo=2000 -v -s
```

Se o navegador abrir, ir para o Google e o teste passar, está tudo OK! 🎉
