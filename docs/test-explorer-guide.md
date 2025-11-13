# Guia do Test Explorer - VS Code/Kiro

## Índice

1. [Quick Start](#quick-start)
2. [Recursos do Test Explorer](#recursos-do-test-explorer)
3. [Guia de Configuração](#guia-de-configuração)
4. [Troubleshooting](#troubleshooting)
5. [Melhores Práticas](#melhores-práticas)

---

## Quick Start

### Passo 1: Instalar a Extensão Python

Se você ainda não tem a extensão Python instalada no Kiro/VS Code:

1. Abra a paleta de comandos: `Ctrl+Shift+P` (Windows) ou `Cmd+Shift+P` (Mac)
2. Digite: `Extensions: Install Extensions`
3. Procure por: `Python` (da Microsoft)
4. Clique em **Install**

Ou simplesmente aceite a recomendação que aparece automaticamente ao abrir este projeto.

### Passo 2: Abrir o Test Explorer

Existem três formas de abrir o Test Explorer:

**Opção 1 - Ícone na Sidebar:**
- Clique no ícone de "Testing" (frasco de laboratório) na barra lateral esquerda

**Opção 2 - Paleta de Comandos:**
- `Ctrl+Shift+P` → Digite: `Test: Focus on Test Explorer View`

**Opção 3 - Atalho de Teclado:**
- Use o atalho configurado (padrão: `Ctrl+Shift+T`)

### Passo 3: Executar Seu Primeiro Teste

1. No Test Explorer, você verá uma árvore com todos os seus testes
2. Expanda as pastas para ver os arquivos de teste
3. Clique no ícone de **▶ (play)** ao lado de qualquer teste
4. Aguarde a execução e veja o resultado!

```
📁 tests/
  📁 jsonplaceholder/
    📄 test_users.py
      ✓ test_get_all_users
      ✓ test_get_user_by_id
      ✗ test_create_user
```

---

## Recursos do Test Explorer

### 1. Visualização em Árvore

O Test Explorer organiza seus testes em uma hierarquia visual:

```
📁 Pasta de Testes
  └─ 📄 Arquivo de Teste
      └─ 🧪 Função de Teste
          └─ 🔢 Teste Parametrizado (se aplicável)
```

**Ícones de Status:**
- ○ Cinza: Teste não executado
- ✓ Verde: Teste passou
- ✗ Vermelho: Teste falhou
- ⊘ Amarelo: Teste pulado (skipped)
- ⟳ Azul: Teste em execução

### 2. Botões de Execução

Cada nível da árvore tem botões de ação:

| Botão | Ação | Descrição |
|-------|------|-----------|
| ▶ | Run | Executa o teste/grupo selecionado |
| 🐛 | Debug | Inicia debug session com breakpoints |
| ↻ | Refresh | Atualiza a descoberta de testes |

**Níveis de Execução:**
- **Teste individual:** Executa apenas aquele teste
- **Arquivo:** Executa todos os testes do arquivo
- **Pasta:** Executa todos os testes da pasta recursivamente
- **Root (▶ no topo):** Executa toda a suite de testes

### 3. Resultados Inline

Após executar testes, você verá:

**No Editor de Código:**
- Decorações inline mostrando ✓ ou ✗ ao lado de cada teste
- Hover sobre o ícone para ver detalhes (tempo de execução, mensagem de erro)

**No Test Explorer:**
- Tempo de execução ao lado de cada teste
- Mensagem de erro expandível para testes falhados
- Link clicável para navegar até a linha do erro

**No Output Panel:**
- Log completo da execução do pytest
- Traceback detalhado de falhas
- Acesse via: `View → Output → Python Test Log`

### 4. Filtros e Busca

**Filtrar por Status:**
- Clique nos ícones no topo do Test Explorer:
  - ✓ Mostrar apenas testes que passaram
  - ✗ Mostrar apenas testes que falharam
  - ○ Mostrar apenas testes não executados

**Buscar Testes:**
- Use a caixa de busca no topo do Test Explorer
- Digite o nome do teste ou arquivo
- Suporta busca parcial (ex: "user" encontra "test_user_login")

### 5. Menu Contextual (Right-Click)

Clique com botão direito em qualquer teste para ver opções:
- **Run Test:** Executa o teste
- **Debug Test:** Inicia debug
- **Go to Test:** Navega para o código do teste
- **Reveal in Explorer:** Mostra o arquivo no explorador
- **Copy Test ID:** Copia o identificador do teste (útil para CLI)

---

## Guia de Configuração

### Arquivo: `.vscode/settings.json`

Este arquivo já está configurado no projeto. Aqui está o que cada opção faz:

```json
{
  // Habilita pytest como framework de testes
  "python.testing.pytestEnabled": true,
  
  // Desabilita unittest (evita conflitos)
  "python.testing.unittestEnabled": false,
  
  // Argumentos passados ao pytest durante execução
  "python.testing.pytestArgs": [
    "-v",           // Verbose: mostra mais detalhes
    "--tb=short",   // Traceback curto (mais legível)
    "--color=yes"   // Colorização da saída
  ],
  
  // Diretório de trabalho (raiz do projeto)
  "python.testing.cwd": "${workspaceFolder}",
  
  // Auto-descoberta ao salvar arquivos
  "python.testing.autoTestDiscoverOnSaveEnabled": true,
  
  // Caminho para o Python do virtual environment
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
  
  // Arquivo de variáveis de ambiente
  "python.envFile": "${workspaceFolder}/.env"
}
```

### Personalizando Argumentos do pytest

Você pode adicionar mais argumentos ao `pytestArgs`:

```json
"python.testing.pytestArgs": [
  "-v",
  "--tb=short",
  "--color=yes",
  "--maxfail=1",              // Para após primeira falha
  "-m", "not slow",           // Pula testes marcados como 'slow'
  "--strict-markers",         // Valida markers customizados
  "--alluredir=allure-results" // Gera relatórios Allure
]
```

### Configuração de Debug: `.vscode/launch.json`

Para debug avançado, o arquivo `launch.json` está configurado:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Debug Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v", "-s", "${file}"],
      "console": "integratedTerminal",
      "justMyCode": false,  // Permite debug em fixtures e libs
      "env": {
        "PYTEST_CURRENT_TEST": ""
      }
    }
  ]
}
```

**Opções importantes:**
- `justMyCode: false` → Permite debugar dentro de fixtures e bibliotecas
- `console: integratedTerminal` → Mostra output no terminal integrado
- `args: ["-s"]` → Desabilita captura de output (mostra prints)

### Variáveis de Ambiente

Se seus testes precisam de variáveis de ambiente:

**Opção 1 - Arquivo .env:**
```bash
# .env
API_BASE_URL=https://jsonplaceholder.typicode.com
API_KEY=your_api_key_here
ENVIRONMENT=development
```

O Test Explorer carrega automaticamente via `python.envFile`.

**Opção 2 - Direto no settings.json:**
```json
{
  "python.testing.pytestArgs": [...],
  "python.envFile": "${workspaceFolder}/.env",
  "terminal.integrated.env.windows": {
    "API_BASE_URL": "https://api.example.com"
  }
}
```

---

## Troubleshooting

### Problema 1: "No tests discovered"

**Sintomas:**
- Test Explorer vazio ou mostra "No tests discovered"
- Árvore de testes não aparece

**Soluções:**

1. **Verificar se pytest está instalado:**
   ```bash
   .venv\Scripts\activate
   pip list | findstr pytest
   ```
   Se não estiver instalado: `pip install pytest`

2. **Verificar interpretador Python:**
   - `Ctrl+Shift+P` → `Python: Select Interpreter`
   - Escolha: `.venv\Scripts\python.exe`

3. **Verificar pytest.ini:**
   - Abra `pytest.ini` e valide a sintaxe
   - Certifique-se que `testpaths` aponta para `tests/`

4. **Forçar redescoberta:**
   - Clique no ícone ↻ (Refresh) no Test Explorer
   - Ou: `Ctrl+Shift+P` → `Test: Refresh Tests`

5. **Verificar logs:**
   - `View → Output → Python Test Log`
   - Procure por erros de import ou sintaxe

### Problema 2: Testes passam no CLI mas falham no Explorer

**Sintomas:**
- `pytest` no terminal funciona
- Mesmos testes falham no Test Explorer

**Soluções:**

1. **Verificar diretório de trabalho:**
   ```json
   "python.testing.cwd": "${workspaceFolder}"
   ```

2. **Verificar variáveis de ambiente:**
   - Certifique-se que `.env` está sendo carregado
   - Adicione `python.envFile` no settings.json

3. **Verificar interpretador:**
   - Test Explorer deve usar o mesmo Python do terminal
   - Confirme: `Ctrl+Shift+P` → `Python: Select Interpreter`

4. **Limpar cache:**
   ```bash
   rmdir /s /q .pytest_cache
   rmdir /s /q __pycache__
   ```

### Problema 3: Breakpoints não são atingidos

**Sintomas:**
- Debug inicia mas não para nos breakpoints
- Execução passa direto pelos breakpoints

**Soluções:**

1. **Verificar justMyCode:**
   ```json
   // Em .vscode/launch.json
   "justMyCode": false
   ```

2. **Usar botão de Debug do Test Explorer:**
   - Não use F5 diretamente
   - Clique no ícone 🐛 ao lado do teste

3. **Verificar se o arquivo está salvo:**
   - Breakpoints só funcionam em arquivos salvos
   - `Ctrl+S` antes de debugar

4. **Desabilitar coverage durante debug:**
   ```json
   "python.testing.pytestArgs": [
     "-v",
     "--no-cov"  // Adicione esta linha
   ]
   ```

### Problema 4: Testes lentos ou travando

**Sintomas:**
- Test Explorer demora muito para descobrir testes
- IDE fica lento ao expandir árvore de testes

**Soluções:**

1. **Desabilitar auto-descoberta:**
   ```json
   "python.testing.autoTestDiscoverOnSaveEnabled": false
   ```

2. **Limitar escopo de descoberta:**
   ```json
   "python.testing.pytestArgs": [
     "-v",
     "tests/jsonplaceholder"  // Apenas uma pasta específica
   ]
   ```

3. **Excluir pastas grandes:**
   ```json
   "files.watcherExclude": {
     "**/.venv/**": true,
     "**/node_modules/**": true,
     "**/__pycache__/**": true
   }
   ```

### Problema 5: Fixtures não funcionam

**Sintomas:**
- Testes que usam fixtures falham
- Erro: "fixture 'nome' not found"

**Soluções:**

1. **Verificar conftest.py:**
   - Certifique-se que `conftest.py` está na pasta correta
   - Fixtures devem estar definidas em `conftest.py`

2. **Verificar imports:**
   - Fixtures não precisam ser importadas
   - pytest descobre automaticamente via `conftest.py`

3. **Verificar escopo:**
   ```python
   @pytest.fixture(scope="session")  # ou "module", "function"
   def api_client():
       return APIClient()
   ```

### Comandos Úteis para Diagnóstico

```bash
# Verificar descoberta de testes
pytest --collect-only

# Executar com mais verbosidade
pytest -vv

# Mostrar prints durante execução
pytest -s

# Executar teste específico
pytest tests/test_users.py::test_get_user

# Verificar versão do pytest
pytest --version

# Listar fixtures disponíveis
pytest --fixtures
```

---

## Melhores Práticas

### 1. Organização de Testes

**Estrutura Recomendada:**
```
tests/
├── conftest.py              # Fixtures globais
├── jsonplaceholder/
│   ├── conftest.py          # Fixtures específicas
│   ├── test_users.py
│   ├── test_posts.py
│   └── test_comments.py
└── backend/
    ├── conftest.py
    ├── test_auth.py
    └── test_database.py
```

**Benefícios:**
- Test Explorer mostra hierarquia clara
- Fácil executar grupos de testes
- Fixtures organizadas por contexto

### 2. Nomenclatura de Testes

**Boas Práticas:**
```python
# ✓ BOM: Descritivo e claro
def test_get_user_returns_200_with_valid_id():
    pass

def test_create_user_fails_with_invalid_email():
    pass

# ✗ RUIM: Vago e genérico
def test_user():
    pass

def test_1():
    pass
```

**Benefícios:**
- Fácil encontrar testes no Test Explorer
- Resultados mais legíveis
- Melhor documentação do comportamento

### 3. Uso de Markers

Organize testes com markers customizados:

```python
import pytest

@pytest.mark.smoke
def test_critical_user_flow():
    pass

@pytest.mark.slow
def test_performance_heavy_operation():
    pass

@pytest.mark.integration
def test_database_connection():
    pass
```

**Executar apenas testes específicos:**
```json
// No settings.json
"python.testing.pytestArgs": [
  "-v",
  "-m", "smoke"  // Executa apenas testes @pytest.mark.smoke
]
```

**Ou via CLI:**
```bash
pytest -m smoke
pytest -m "not slow"
pytest -m "smoke or integration"
```

### 4. Testes Parametrizados

Use parametrização para testar múltiplos cenários:

```python
@pytest.mark.parametrize("user_id,expected_status", [
    (1, 200),
    (999, 404),
    (-1, 400),
])
def test_get_user_with_various_ids(user_id, expected_status):
    response = api.get_user(user_id)
    assert response.status_code == expected_status
```

**No Test Explorer:**
```
📄 test_users.py
  🧪 test_get_user_with_various_ids[1-200]
  🧪 test_get_user_with_various_ids[999-404]
  🧪 test_get_user_with_various_ids[-1-400]
```

Cada combinação aparece como teste separado!

### 5. Debug Eficiente

**Estratégias:**

1. **Breakpoint Condicional:**
   - Right-click no breakpoint → Edit Breakpoint
   - Adicione condição: `user_id == 5`

2. **Logpoints:**
   - Right-click na margem → Add Logpoint
   - Mensagem: `User ID: {user_id}, Status: {response.status}`
   - Não para execução, apenas loga

3. **Debug Console:**
   - Durante debug, use o Debug Console
   - Execute código Python interativamente
   - Inspecione variáveis: `print(response.json())`

4. **Step Into vs Step Over:**
   - `F11` (Step Into): Entra em funções chamadas
   - `F10` (Step Over): Executa linha sem entrar em funções
   - `Shift+F11` (Step Out): Sai da função atual

### 6. Execução Seletiva

**Cenários Comuns:**

```bash
# Executar apenas testes de uma feature
# No Test Explorer: Click ▶ na pasta "jsonplaceholder"

# Executar apenas testes que falharam
# No Test Explorer: Click no filtro ✗ (Failed)

# Executar teste específico
# No Test Explorer: Click ▶ no teste individual

# Re-executar último teste
# Atalho: Ctrl+; Ctrl+R (ou via Command Palette)
```

### 7. Integração com CI/CD

O Test Explorer não substitui CI/CD, mas complementa:

**Workflow Recomendado:**
1. **Desenvolvimento:** Use Test Explorer para feedback rápido
2. **Pre-commit:** Execute suite completa no terminal
3. **CI/CD:** Pipeline executa todos os testes + relatórios

**Exemplo de script pre-commit:**
```bash
# pre-commit.sh
pytest tests/ -v --tb=short --maxfail=5
if [ $? -ne 0 ]; then
    echo "Testes falharam! Commit bloqueado."
    exit 1
fi
```

### 8. Performance

**Dicas para Testes Rápidos:**

1. **Use fixtures com escopo adequado:**
   ```python
   @pytest.fixture(scope="session")  # Reutiliza entre testes
   def api_client():
       return APIClient()
   ```

2. **Paralelização (pytest-xdist):**
   ```bash
   pip install pytest-xdist
   pytest -n auto  # Usa todos os cores
   ```

3. **Pule testes lentos durante desenvolvimento:**
   ```json
   "python.testing.pytestArgs": ["-m", "not slow"]
   ```

4. **Cache de resultados:**
   ```bash
   pytest --lf  # Last Failed: executa apenas testes que falharam
   pytest --ff  # Failed First: executa falhados primeiro
   ```

---

## Atalhos de Teclado Úteis

| Atalho | Ação |
|--------|------|
| `Ctrl+Shift+T` | Abrir Test Explorer |
| `Ctrl+; Ctrl+R` | Re-executar último teste |
| `Ctrl+; Ctrl+D` | Debug último teste |
| `Ctrl+; Ctrl+A` | Executar todos os testes |
| `F5` | Continuar debug |
| `F10` | Step Over (debug) |
| `F11` | Step Into (debug) |
| `Shift+F11` | Step Out (debug) |
| `Shift+F5` | Parar debug |

---

## Recursos Adicionais

### Documentação Oficial

- [pytest Documentation](https://docs.pytest.org/)
- [VS Code Python Testing](https://code.visualstudio.com/docs/python/testing)
- [Python Extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

### Plugins pytest Úteis

```bash
# Relatórios HTML
pip install pytest-html

# Paralelização
pip install pytest-xdist

# Coverage
pip install pytest-cov

# Allure reports
pip install allure-pytest

# Mocking
pip install pytest-mock
```

### Comunidade

- [pytest GitHub](https://github.com/pytest-dev/pytest)
- [Stack Overflow - pytest tag](https://stackoverflow.com/questions/tagged/pytest)
- [Python Testing Discord](https://discord.gg/python)

---

## Conclusão

O Test Explorer transforma a experiência de testes no Kiro/VS Code:
- ✅ Interface visual intuitiva
- ✅ Feedback instantâneo
- ✅ Debug integrado
- ✅ Zero configuração adicional

Agora você está pronto para aproveitar ao máximo o Test Explorer! 🚀

Se encontrar problemas não cobertos neste guia, consulte a seção [Troubleshooting](#troubleshooting) ou abra uma issue no repositório do projeto.
