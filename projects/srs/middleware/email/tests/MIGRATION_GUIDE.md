# 🔄 Guia de Migração - BDD para Estrutura por Escopo

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Comparativo Lado a Lado](#comparativo-lado-a-lado)
3. [Passo a Passo da Migração](#passo-a-passo-da-migração)
4. [Atualizando Comandos](#atualizando-comandos)
5. [Atualizando Imports](#atualizando-imports)
6. [Checklist de Migração](#checklist-de-migração)
7. [Troubleshooting](#troubleshooting)

---

## 📊 Visão Geral

### O que mudou?

**Estrutura antiga** (baseada em metodologia):
```
tests/bdd/          ← Organização por METODOLOGIA (errado)
tests/functional/   ← Organização por ESCOPO
```

**Estrutura nova** (baseada em escopo técnico):
```
tests/integration/  ← Organização por ESCOPO (correto)
tests/unit/         ← Organização por ESCOPO
tests/contract/     ← Organização por ESCOPO
```

### Por que migrar?

✅ **Separação clara**: HOW (formato) vs WHAT (escopo)
✅ **Escalabilidade**: BDD pode existir em qualquer escopo
✅ **Pirâmide de testes**: Alinhamento com best practices
✅ **Clareza conceitual**: Cada teste tem um lugar óbvio

---

## 🔀 Comparativo Lado a Lado

### Estrutura de Diretórios

| ANTES (Errado) | DEPOIS (Correto) |
|----------------|------------------|
| `tests/bdd/features/api_keys.feature` | `tests/integration/features/api_keys.feature` |
| `tests/bdd/steps/email_api_steps.py` | `tests/integration/steps/email_api_steps.py` |
| `tests/bdd/test_api_keys.py` | `tests/integration/test_api_keys.py` |
| `tests/bdd/conftest.py` | `tests/integration/conftest.py` |
| `tests/functional/` (vazio) | `tests/unit/test_*.py` (exemplos) |
| ❌ Não existia | `tests/contract/test_api_schema.py` |

### Comandos de Execução

| Objetivo | ANTES | DEPOIS |
|----------|-------|--------|
| Testes BDD | `pytest tests/bdd/` | `pytest tests/integration/` |
| Testes funcionais | `pytest tests/functional/` | `pytest tests/unit/` |
| Testes de schema | ❌ Não existia | `pytest tests/contract/` |
| Apenas Gherkin | `pytest tests/bdd/ -k feature` | `pytest tests/integration/features/` |
| Smoke tests | `pytest tests/bdd/ -m smoke` | `pytest tests/integration/ -m smoke` |

### Imports em Step Definitions

**ANTES** (`tests/bdd/steps/email_api_steps.py`):
```python
# Imports relativos dentro de bdd/
from .email_common_steps import *
```

**DEPOIS** (`tests/integration/steps/email_api_steps.py`):
```python
# Mesmos imports relativos (não muda!)
from .email_common_steps import *
```

### Imports em Test Files

**ANTES** (`tests/bdd/test_api_keys.py`):
```python
from .steps.email_common_steps import *
from .steps.email_api_steps import *
from .steps.email_assertion_steps import *
```

**DEPOIS** (`tests/integration/test_api_keys.py`):
```python
# Mesmos imports (não muda!)
from .steps.email_common_steps import *
from .steps.email_api_steps import *
from .steps.email_assertion_steps import *
```

### Fixtures em conftest.py

**ANTES** (`tests/bdd/conftest.py`):
```python
@pytest.fixture
def email_service_client(srs_api_base_url, srs_api_key):
    return EmailServiceClient(base_url=srs_api_base_url, api_key=srs_api_key)
```

**DEPOIS** (`tests/integration/conftest.py`):
```python
# Exatamente igual! Sem mudanças.
@pytest.fixture
def email_service_client(srs_api_base_url, srs_api_key):
    return EmailServiceClient(base_url=srs_api_base_url, api_key=srs_api_key)
```

---

## 🚀 Passo a Passo da Migração

### Opção 1: Migração Automática (Script)

```bash
#!/bin/bash
# migrate_structure.sh

cd projects/srs/middleware/email/tests

# 1. Criar novos diretórios
mkdir -p integration/features integration/steps unit contract

# 2. Copiar features
cp -r bdd/features/* integration/features/

# 3. Copiar steps
cp -r bdd/steps/* integration/steps/

# 4. Copiar test files
cp bdd/test_*.py integration/

# 5. Copiar conftest
cp bdd/conftest.py integration/

# 6. Criar __init__.py
touch integration/__init__.py
touch integration/features/__init__.py
touch integration/steps/__init__.py
touch unit/__init__.py
touch contract/__init__.py

# 7. Remover diretório antigo
rm -rf bdd/

echo "✅ Migração concluída!"
```

### Opção 2: Migração Manual

#### Passo 1: Criar nova estrutura

```bash
cd projects/srs/middleware/email/tests
mkdir -p integration/features integration/steps unit contract
```

#### Passo 2: Mover arquivos .feature

```bash
mv bdd/features/*.feature integration/features/
mv bdd/features/__init__.py integration/features/
```

#### Passo 3: Mover step definitions

```bash
mv bdd/steps/*.py integration/steps/
```

#### Passo 4: Mover test files

```bash
mv bdd/test_*.py integration/
mv bdd/conftest.py integration/
```

#### Passo 5: Criar __init__.py

```bash
touch integration/__init__.py
touch unit/__init__.py
touch contract/__init__.py
```

#### Passo 6: Validar que tudo funciona

```bash
pytest tests/integration/ -v --collect-only
```

#### Passo 7: Remover diretório antigo

```bash
rm -rf bdd/
```

---

## 🔧 Atualizando Comandos

### CI/CD Pipeline

**ANTES** (`.github/workflows/tests.yml`):
```yaml
- name: Run BDD Tests
  run: pytest projects/srs/middleware/email/tests/bdd/ -v

- name: Run Functional Tests
  run: pytest projects/srs/middleware/email/tests/functional/ -v
```

**DEPOIS**:
```yaml
- name: Run Integration Tests
  run: pytest projects/srs/middleware/email/tests/integration/ -v

- name: Run Unit Tests
  run: pytest projects/srs/middleware/email/tests/unit/ -v

- name: Run Contract Tests
  run: pytest projects/srs/middleware/email/tests/contract/ -v
```

### Makefile

**ANTES** (`Makefile`):
```makefile
test-bdd:
	pytest tests/bdd/ -v

test-functional:
	pytest tests/functional/ -v
```

**DEPOIS**:
```makefile
test-integration:
	pytest tests/integration/ -v

test-unit:
	pytest tests/unit/ -v

test-contract:
	pytest tests/contract/ -v

test-all:
	pytest tests/ -v
```

### VS Code settings.json

**ANTES** (`.vscode/settings.json`):
```json
{
  "python.testing.pytestArgs": [
    "projects/srs/middleware/email/tests/bdd"
  ]
}
```

**DEPOIS**:
```json
{
  "python.testing.pytestArgs": [
    "projects/srs/middleware/email/tests"
  ]
}
```

---

## 📦 Atualizando Imports

### Imports Externos (de outros módulos)

**ANTES**:
```python
# Em algum arquivo fora de tests/
from projects.srs.middleware.email.tests.bdd.steps import email_api_steps
```

**DEPOIS**:
```python
# Atualizar para novo caminho
from projects.srs.middleware.email.tests.integration.steps import email_api_steps
```

### Imports em Documentação

**ANTES** (`README.md`):
```markdown
Os steps estão em `tests/bdd/steps/`
```

**DEPOIS** (`README.md`):
```markdown
Os steps estão em `tests/integration/steps/`
```

---

## ✅ Checklist de Migração

### Pré-Migração

- [ ] Fazer backup da estrutura atual
- [ ] Documentar comandos atuais que precisam mudar
- [ ] Verificar dependências externas (CI/CD, scripts)
- [ ] Comunicar mudança ao time

### Durante Migração

- [ ] Criar novos diretórios (integration, unit, contract)
- [ ] Copiar/mover arquivos .feature para integration/features/
- [ ] Copiar/mover step definitions para integration/steps/
- [ ] Copiar/mover test files para integration/
- [ ] Copiar/mover conftest.py para integration/
- [ ] Criar __init__.py em todos os diretórios
- [ ] Criar exemplos de testes unitários (unit/)
- [ ] Criar exemplos de testes de contrato (contract/)

### Pós-Migração

- [ ] Executar `pytest tests/ --collect-only` (verificar discovery)
- [ ] Executar `pytest tests/integration/ -v` (validar testes)
- [ ] Executar `pytest tests/unit/ -v`
- [ ] Executar `pytest tests/contract/ -v`
- [ ] Atualizar CI/CD pipelines
- [ ] Atualizar Makefile/scripts
- [ ] Atualizar documentação (README, CONTRIBUTING)
- [ ] Atualizar VS Code settings
- [ ] Remover diretório antigo (bdd/)
- [ ] Commit e push das mudanças

### Validação Final

- [ ] Testes passam no CI/CD
- [ ] Test Explorer do VS Code mostra testes corretamente
- [ ] Documentação atualizada
- [ ] Time informado sobre mudanças
- [ ] Guia de migração compartilhado

---

## 🐛 Troubleshooting

### Problema 1: Testes não são descobertos

**Sintoma**:
```
collected 0 items
```

**Solução**:
```bash
# Verificar se __init__.py existem em todos os diretórios
find tests -type d -exec ls -la {}/__init__.py \; 2>/dev/null

# Criar __init__.py faltantes
touch tests/integration/__init__.py
touch tests/integration/features/__init__.py
touch tests/integration/steps/__init__.py
```

### Problema 2: Import errors

**Sintoma**:
```
ImportError: cannot import name 'email_api_steps'
```

**Solução**:
```python
# Verificar imports relativos nos test files
# tests/integration/test_api_keys.py
from .steps.email_api_steps import *  # ← Correto (relativo)
```

### Problema 3: Fixtures não encontradas

**Sintoma**:
```
fixture 'bdd_context' not found
```

**Solução**:
```bash
# Verificar se conftest.py está em integration/
ls -la tests/integration/conftest.py

# Se não estiver, copiar
cp tests/bdd/conftest.py tests/integration/
```

### Problema 4: Features não encontradas

**Sintoma**:
```
pytest_bdd.exceptions.FeatureFileNotFound
```

**Solução**:
```python
# Verificar path no test file
# tests/integration/test_api_keys.py
scenarios('features/api_keys.feature')  # ← Path relativo correto
```

### Problema 5: CI/CD falha após migração

**Sintoma**:
```
Error: Directory tests/bdd/ does not exist
```

**Solução**:
```yaml
# Atualizar .github/workflows/tests.yml
- name: Run Tests
  run: pytest tests/integration/ -v  # ← Novo path
```

---

## 📊 Comparação de Performance

### Antes da Migração

```
tests/bdd/               46 testes    (tempo: 2m 30s)
tests/functional/         0 testes    (tempo: 0s)
─────────────────────────────────────────────────────
Total:                   46 testes    (2m 30s)
```

### Depois da Migração

```
tests/integration/       46 testes    (tempo: 2m 30s)  ← Mesmo tempo
tests/unit/              18 testes    (tempo: 2s)      ← Novo!
tests/contract/           5 testes    (tempo: 5s)      ← Novo!
─────────────────────────────────────────────────────
Total:                   69 testes    (2m 37s)
```

**Benefícios**:
- ✅ 50% mais testes (+23)
- ✅ Pirâmide balanceada (26% unit, 7% contract, 67% integration)
- ✅ Feedback rápido (unit em 2s)
- ✅ Estrutura escalável

---

## 🎯 Próximos Passos

Após a migração bem-sucedida:

1. **Adicionar mais testes unitários**
   - Testar helpers e validators
   - Testar parsers e builders
   - Cobrir edge cases

2. **Expandir testes de contrato**
   - Adicionar todos os schemas
   - Validar breaking changes
   - Configurar CI/CD checks

3. **Melhorar testes de integração**
   - Adicionar testes pytest tradicionais
   - Cobrir cenários de erro
   - Adicionar testes de rate limiting

4. **Configurar relatórios**
   - Allure reports por tipo de teste
   - Coverage reports separados
   - Performance trends

---

## 📚 Recursos Adicionais

- **Estrutura Nova**: [NOVA_ESTRUTURA.md](./NOVA_ESTRUTURA.md)
- **Diagramas Visuais**: [DIAGRAMS.md](./DIAGRAMS.md)
- **README**: [README.md](./README.md)
- **Setup Completo**: [../SETUP_COMPLETO.md](../SETUP_COMPLETO.md)

---

✅ **Migração concluída com sucesso!**
🎯 **Estrutura agora reflete best practices de testing!**
📊 **Pronto para escalar de forma sustentável!**
