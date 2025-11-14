# 🎯 Como Usar o Test Explorer do VS Code

## 📋 Pré-requisitos

1. **Extensão Python** instalada no VS Code
2. **Pytest** instalado no projeto

## 🚀 Ativando o Test Explorer

### Passo 1: Abrir o Test Explorer

Existem 3 formas:

**Opção A:** Clique no ícone de "Testing" (frasco de laboratório 🧪) na barra lateral esquerda

**Opção B:** Use o atalho `Ctrl+Shift+P` e digite "Test: Focus on Test Explorer View"

**Opção C:** Menu: `View` → `Testing`

### Passo 2: Descobrir os Testes

1. No painel Test Explorer, clique no botão **"Refresh Tests"** (ícone de atualizar)
2. Aguarde alguns segundos enquanto o VS Code descobre todos os testes
3. Você verá uma árvore com todos os arquivos e testes

## 🎮 Como Usar

### Executar Testes

#### Executar TODOS os testes
- Clique no botão ▶️ (Play) ao lado de "tests" no topo da árvore

#### Executar testes de uma pasta
- Clique no ▶️ ao lado da pasta (ex: `tests/examples`)

#### Executar um arquivo específico
- Clique no ▶️ ao lado do arquivo (ex: `test_exemplo_basico.py`)

#### Executar um teste específico
- Clique no ▶️ ao lado do nome do teste (ex: `test_abrir_google`)

### Visualizar Resultados

- ✅ **Verde** = Teste passou
- ❌ **Vermelho** = Teste falhou
- ⏸️ **Cinza** = Teste não executado ainda

### Ver Detalhes de Falha

1. Clique no teste que falhou
2. Veja o erro no painel inferior
3. Clique em "Go to Test" para ir direto no código

### Debug de Testes

1. Clique com botão direito no teste
2. Selecione **"Debug Test"**
3. Use breakpoints normalmente (F9)

## 🎨 Recursos Úteis

### Executar com Navegador Visível

O arquivo `.vscode/settings.json` já está configurado com `--headed`, então os testes de UI vão abrir o navegador automaticamente!

### Executar Teste Atual

Quando estiver editando um arquivo de teste:
- `Ctrl+Shift+P` → "Test: Run Test at Cursor"
- Ou clique no ícone ▶️ que aparece ao lado da função de teste

### Executar Testes Automaticamente

Para executar testes automaticamente quando salvar:
1. `Ctrl+Shift+P` → "Preferences: Open Settings (UI)"
2. Busque por "python testing auto"
3. Marque "Python > Testing: Auto Test Discover On Save Enabled"

## 📊 Visualização em Árvore

```
📁 tests
  📁 examples
    📄 test_exemplo_basico.py
      ✅ test_abrir_google
      ✅ test_buscar_no_google
      ✅ test_abrir_wikipedia
      ✅ test_buscar_na_wikipedia
    📄 test_google_search.py
      ✅ test_google_homepage_loads
      ✅ test_google_search_functionality
  📁 frontend
    📄 test_login.py
    📄 test_user_journey.py
```

## 🎯 Atalhos Úteis

| Ação | Atalho |
|------|--------|
| Abrir Test Explorer | `Ctrl+Shift+P` → "Test: Focus" |
| Executar teste atual | `Ctrl+Shift+P` → "Test: Run Test at Cursor" |
| Debug teste atual | `Ctrl+Shift+P` → "Test: Debug Test at Cursor" |
| Executar todos | Clique no ▶️ no topo |
| Atualizar lista | Clique no 🔄 |

## 💡 Dicas

### 1. Filtrar Testes

Use a barra de busca no Test Explorer para filtrar:
- Digite "google" para ver só testes do Google
- Digite "frontend" para ver só testes de frontend

### 2. Executar Testes Falhados

Clique no ícone de "Run Failed Tests" para re-executar apenas os que falharam

### 3. Ver Output Completo

Clique em "Show Output" no painel de teste para ver logs detalhados

### 4. Configurar Pytest Args

Edite `.vscode/settings.json` para adicionar argumentos:

```json
{
  "python.testing.pytestArgs": [
    "tests",
    "-v",
    "--headed",           // Mostrar navegador
    "--slowmo=1000",      // Modo lento
    "--screenshot=on",    // Screenshots em falhas
    "-k", "google"        // Executar só testes com "google" no nome
  ]
}
```

## 🐛 Troubleshooting

### Testes não aparecem?

1. Verifique se pytest está instalado: `pip list | grep pytest`
2. Clique em "Refresh Tests" no Test Explorer
3. Verifique o Output: `View` → `Output` → Selecione "Python Test Log"

### Erro "No tests discovered"?

1. Verifique se os arquivos começam com `test_`
2. Verifique se as funções começam com `test_`
3. Verifique se está no diretório correto

### Testes não executam?

1. Verifique o interpretador Python: Clique na barra inferior onde mostra a versão do Python
2. Selecione o ambiente virtual correto (`.venv`)

## 🎓 Exemplo Prático

1. Abra o Test Explorer (ícone 🧪 na lateral)
2. Clique em "Refresh Tests"
3. Expanda `tests` → `examples` → `test_exemplo_basico.py`
4. Clique no ▶️ ao lado de `test_abrir_google`
5. Veja o navegador abrir e o teste executar!
6. Veja o ✅ verde quando passar

## 🎉 Pronto!

Agora você pode executar testes com apenas um clique, sem precisar da linha de comando! 🚀

---

**Dica:** Mantenha o Test Explorer aberto na lateral enquanto desenvolve. Assim você pode executar testes rapidamente enquanto codifica!
