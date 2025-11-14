# Como Ver os Testes BDD no Test Explorer

## ✅ Status Atual

Os testes BDD estão **implementados e funcionando corretamente**:
- **92 testes BDD** descobertos com sucesso
- Todos os arquivos de teste estão corretos
- pytest-bdd está configurado corretamente

## 🔧 Problema

O Test Explorer do Kiro IDE não está mostrando o diretório `tests/bdd/` na árvore de testes.

## 🎯 Solução

### Passo 1: Atualizar Configuração (JÁ FEITO ✅)

Atualizei o arquivo `.vscode/settings.json` removendo o parâmetro `--headed` que estava causando conflito.

### Passo 2: Recarregar o Test Explorer

**Escolha UMA das opções abaixo:**

#### Opção A: Refresh Tests (RECOMENDADO)
1. Pressione `Ctrl+Shift+P` (Windows/Linux) ou `Cmd+Shift+P` (Mac)
2. Digite: `Test: Refresh Tests`
3. Pressione Enter
4. Aguarde alguns segundos

#### Opção B: Reload Window
1. Pressione `Ctrl+Shift+P` (Windows/Linux) ou `Cmd+Shift+P` (Mac)
2. Digite: `Developer: Reload Window`
3. Pressione Enter
4. Aguarde a janela recarregar

#### Opção C: Reiniciar Kiro IDE
1. Feche completamente o Kiro IDE
2. Reabra o projeto
3. Aguarde a indexação completa

### Passo 3: Verificar no Test Explorer

Após recarregar, você deverá ver no Test Explorer:

```
tests/
├── bdd/                                    ← NOVO!
│   ├── test_posts_api.py (16 testes)
│   ├── test_users_api.py (30 testes)
│   ├── test_data_management.py (14 testes)
│   ├── test_end_to_end_integration.py (9 testes)
│   ├── test_database_steps.py (5 testes)
│   ├── test_api_steps_validation.py (3 testes)
│   ├── test_explorer_verification.py (13 testes)
│   └── test_bdd_context.py (2 testes)
├── examples/
├── frontend/
├── integration/
└── jsonplaceholder/
```

## 📊 Testes BDD Disponíveis

### API Tests (46 testes)
- **test_posts_api.py** - 16 cenários de teste da API de Posts
- **test_users_api.py** - 30 cenários de teste da API de Users

### Database Tests (19 testes)
- **test_data_management.py** - 14 cenários de gerenciamento de dados
- **test_database_steps.py** - 5 cenários de steps de database

### Integration Tests (9 testes)
- **test_end_to_end_integration.py** - 9 cenários de integração completa

### Validation Tests (16 testes)
- **test_api_steps_validation.py** - 3 cenários de validação de API steps
- **test_explorer_verification.py** - 13 cenários de verificação do Test Explorer
- **test_bdd_context.py** - 2 cenários de contexto BDD

**Total: 92 testes BDD** ✅

## 🎮 Como Usar os Testes BDD

### Executar Teste Individual
1. Expanda o diretório `tests/bdd/` no Test Explorer
2. Expanda o arquivo de teste desejado
3. Clique no ▶️ ao lado do teste
4. Veja o resultado inline

### Executar Todos os Testes de um Arquivo
1. Clique no ▶️ ao lado do nome do arquivo
2. Todos os testes daquele arquivo serão executados

### Filtrar por Tags
1. Use o campo de filtro no topo do Test Explorer
2. Digite: `@smoke`, `@api`, `@crud`, `@database`, etc.
3. Apenas testes com aquela tag serão exibidos

### Debugar um Teste
1. Clique no 🐛 ao lado do teste
2. Defina breakpoints nos arquivos em `tests/bdd/steps/`
3. O debugger irá parar nos breakpoints
4. Inspecione variáveis e execute passo a passo

## 🔍 Verificação Manual

Se ainda não aparecer, execute no terminal para confirmar que os testes existem:

```bash
# Listar todos os testes BDD
pytest --collect-only tests/bdd/ -q

# Executar um teste específico
pytest tests/bdd/test_posts_api.py::test_get_all_posts -v

# Executar todos os testes BDD
pytest tests/bdd/ -v
```

## 📁 Estrutura dos Arquivos BDD

```
tests/bdd/
├── features/                    # Arquivos .feature (Gherkin)
│   ├── api/
│   │   ├── posts.feature
│   │   └── users.feature
│   ├── database/
│   │   └── data_management.feature
│   └── integration/
│       └── end_to_end.feature
│
├── steps/                       # Step definitions (Python)
│   ├── api_steps.py
│   ├── database_steps.py
│   ├── common_steps.py
│   └── assertions_steps.py
│
├── test_*.py                    # Arquivos de teste (pytest-bdd)
└── conftest.py                  # Fixtures BDD
```

## ❓ Troubleshooting

### Problema: Ainda não vejo os testes

**Solução 1:** Limpar cache do pytest
```bash
# Windows
rmdir /s /q .pytest_cache
rmdir /s /q tests\bdd\__pycache__

# Linux/Mac
rm -rf .pytest_cache
rm -rf tests/bdd/__pycache__
```

Depois recarregue o Test Explorer.

**Solução 2:** Verificar Python interpreter
1. Pressione `Ctrl+Shift+P`
2. Digite: `Python: Select Interpreter`
3. Selecione o interpretador correto (deve ser o do venv)

**Solução 3:** Verificar extensão Python
1. Certifique-se de que a extensão Python está instalada
2. Verifique se está atualizada
3. Recarregue a janela

### Problema: Testes aparecem mas não executam

**Solução:** Instalar dependências
```bash
pip install -r requirements.txt
```

### Problema: Erro "pytest-bdd not found"

**Solução:** Instalar pytest-bdd
```bash
pip install pytest-bdd
```

## 📞 Suporte

Se após seguir todos os passos os testes ainda não aparecerem:

1. Execute: `python refresh_tests.py`
2. Copie a saída completa
3. Verifique se há erros
4. Compartilhe os logs para análise

## ✅ Checklist

- [x] Testes BDD implementados (92 testes)
- [x] pytest-bdd instalado e configurado
- [x] Arquivos .feature criados
- [x] Step definitions implementados
- [x] pytest.ini configurado
- [x] .vscode/settings.json atualizado
- [ ] Test Explorer recarregado ← **VOCÊ ESTÁ AQUI**
- [ ] Testes visíveis no Test Explorer

## 🎉 Próximos Passos

Após os testes aparecerem no Test Explorer:

1. ✅ Execute alguns testes para verificar que funcionam
2. ✅ Experimente debugar um teste
3. ✅ Filtre testes por tags (@smoke, @api, etc.)
4. ✅ Explore os arquivos .feature para entender os cenários
5. ✅ Leia a documentação em `tests/bdd/TEST_EXPLORER_VERIFICATION.md`

---

**Última atualização:** 14/11/2025
**Status:** Testes implementados e funcionando ✅
**Ação necessária:** Recarregar Test Explorer
