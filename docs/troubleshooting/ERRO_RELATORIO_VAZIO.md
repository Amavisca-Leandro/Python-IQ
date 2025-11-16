# 🔧 Solução: Relatório Vazio (0 tests)

## ❌ Problema

O relatório HTML foi gerado mas mostra:
- "0 tests took 0 ms"
- Erros de import
- Nenhum teste executado

## 🎯 Causas Comuns

1. **Ambiente virtual não ativado**
2. **Dependências não instaladas**
3. **Caminho incorreto**
4. **Problemas de import**

## ✅ Soluções

### Solução 1: Script Simples (RECOMENDADO)

Criamos um script mais robusto para você:

```
Duplo clique em: scripts\relatorio_simples.bat
```

Este script:
- ✅ Ativa o ambiente virtual automaticamente
- ✅ Verifica dependências
- ✅ Usa caminhos absolutos
- ✅ Mostra erros claramente

### Solução 2: Diagnóstico

Primeiro, vamos ver o que está acontecendo:

```
Duplo clique em: scripts\diagnostico.bat
```

Isso vai mostrar:
- Versão do Python
- Versão do pytest
- Testes disponíveis
- Pacotes instalados

### Solução 3: Instalação Manual

```bash
# 1. Ativar ambiente virtual
.venv\Scripts\activate

# 2. Instalar dependências
pip install pytest pytest-html pytest-playwright playwright

# 3. Instalar navegadores
playwright install chromium

# 4. Verificar instalação
python -m pytest --version
python -m pip show pytest-html

# 5. Listar testes
python -m pytest tests/examples/ --collect-only

# 6. Gerar relatório
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html -v
```

### Solução 4: Via Test Explorer

Use o Test Explorer do VS Code:

1. Clique no ícone 🧪 (Testing)
2. Clique em 🔄 (Refresh Tests)
3. Execute os testes normalmente
4. Depois gere o relatório:
```bash
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html
```

## 🔍 Verificações

### 1. Verificar se ambiente virtual está ativo

```bash
# Deve mostrar o caminho do .venv
where python
```

Deve mostrar algo como:
```
C:\projects\python-iq\.venv\Scripts\python.exe
```

### 2. Verificar se pytest está instalado

```bash
python -m pytest --version
```

Deve mostrar:
```
pytest 8.4.0
```

### 3. Verificar se testes são encontrados

```bash
python -m pytest tests/examples/ --collect-only
```

Deve listar os testes:
```
<Module test_exemplo_basico.py>
  <Function test_abrir_google>
  <Function test_buscar_no_google>
  ...
```

### 4. Verificar imports

```bash
python -c "import pytest; import playwright; print('OK')"
```

Deve mostrar:
```
OK
```

## 🎯 Teste Rápido

Execute este comando para testar:

```bash
# Ativar ambiente
.venv\Scripts\activate

# Teste simples
python -m pytest tests/examples/test_exemplo_basico.py::test_abrir_google -v

# Se funcionar, gere o relatório
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html -v
```

## 📋 Checklist

Verifique cada item:

- [ ] Ambiente virtual ativado (`.venv\Scripts\activate`)
- [ ] pytest instalado (`python -m pytest --version`)
- [ ] pytest-html instalado (`pip show pytest-html`)
- [ ] playwright instalado (`pip show playwright`)
- [ ] Navegadores instalados (`playwright install chromium`)
- [ ] Testes são encontrados (`pytest --collect-only`)
- [ ] Imports funcionam (`python -c "import pytest"`)

## 🆘 Ainda com Erro?

### Reinstalação Completa

```bash
# 1. Desativar ambiente virtual
deactivate

# 2. Deletar ambiente virtual
rmdir /s /q .venv

# 3. Criar novo
python -m venv .venv

# 4. Ativar
.venv\Scripts\activate

# 5. Atualizar pip
python -m pip install --upgrade pip

# 6. Instalar dependências
pip install -r requirements.txt

# 7. Instalar navegadores
playwright install chromium

# 8. Testar
python -m pytest tests/examples/test_exemplo_basico.py::test_abrir_google -v

# 9. Gerar relatório
python -m pytest tests/examples/ --html=reports/relatorio.html --self-contained-html -v
```

## 💡 Dicas

### Use python -m pytest

Sempre use `python -m pytest` ao invés de apenas `pytest`:

```bash
# ✅ CORRETO
python -m pytest tests/examples/

# ❌ PODE DAR ERRO
pytest tests/examples/
```

### Verifique o diretório

Sempre execute a partir da raiz do projeto:

```bash
# Ver onde está
cd

# Ir para raiz do projeto
cd C:\projects\python-iq

# Executar
python -m pytest tests/examples/
```

### Use caminhos absolutos

Se tiver problemas com caminhos relativos:

```bash
python -m pytest "C:\projects\python-iq\tests\examples" --html="C:\projects\python-iq\reports\relatorio.html" --self-contained-html
```

## 🎉 Solução Rápida

**Forma mais fácil de resolver:**

1. Execute o diagnóstico:
```
Duplo clique em: scripts\diagnostico.bat
```

2. Use o script simples:
```
Duplo clique em: scripts\relatorio_simples.bat
```

3. Se ainda não funcionar, reinstale tudo:
```bash
.venv\Scripts\activate
pip install --force-reinstall pytest pytest-html pytest-playwright
playwright install chromium
```

**Depois teste:**
```bash
python -m pytest tests/examples/test_exemplo_basico.py::test_abrir_google -v --html=reports/teste.html --self-contained-html
```

Se este teste funcionar, o problema está resolvido! 🎯
