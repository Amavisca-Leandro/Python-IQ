# 🚀 Início Rápido - Execute Testes em 3 Passos

## ⚡ Método 1: Test Explorer do VS Code (RECOMENDADO)

### Passo 1: Abrir Test Explorer
Na barra lateral esquerda do VS Code, clique no ícone 🧪 **"Testing"**

```
┌─────────────────────────────────────┐
│  VS Code                            │
├─────────────────────────────────────┤
│  📁 Explorer                        │
│  🔍 Search                          │
│  🔀 Source Control                  │
│  🐛 Run and Debug                   │
│  🧪 Testing          ← CLIQUE AQUI │  ⭐
│  📦 Extensions                      │
└─────────────────────────────────────┘
```

### Passo 2: Atualizar Lista de Testes
Clique no botão 🔄 **"Refresh Tests"** no topo do painel

### Passo 3: Executar Teste
Clique no ▶️ ao lado de qualquer teste

```
📁 tests
  📁 examples
    📄 test_exemplo_basico.py
      ▶️ test_abrir_google          ← CLIQUE AQUI
      ▶️ test_buscar_no_google
      ▶️ test_abrir_wikipedia
```

**Pronto!** O navegador vai abrir e executar o teste! ✅

---

## ⚡ Método 2: Duplo Clique (MAIS FÁCIL)

### Passo 1: Abrir Pasta
Abra a pasta `scripts` no Windows Explorer

### Passo 2: Duplo Clique
Dê duplo clique em: **`run_ui_mode.bat`**

### Passo 3: Assistir
Veja o navegador abrir e executar os testes automaticamente!

**Pronto!** Sem linha de comando! 🎉

---

## ⚡ Método 3: Relatório HTML (BONITO)

### Passo 1: Duplo Clique
Dê duplo clique em: **`scripts/gerar_relatorio_html.bat`**

### Passo 2: Aguardar
Aguarde os testes executarem (alguns segundos)

### Passo 3: Ver Relatório
O relatório HTML abre automaticamente no navegador!

**Pronto!** Relatório lindo para compartilhar! 📊

---

## 🎯 Qual Método Usar?

| Situação | Método Recomendado |
|----------|-------------------|
| Desenvolvendo testes | Test Explorer (Método 1) |
| Quer ver o navegador | Duplo Clique (Método 2) |
| Compartilhar resultados | Relatório HTML (Método 3) |
| Debug de teste | Test Explorer + F9 (breakpoint) |

---

## 📝 Primeiro Teste - Passo a Passo

### 1. Abra o Test Explorer
Clique no ícone 🧪 na lateral do VS Code

### 2. Encontre o teste
```
tests → examples → test_exemplo_basico.py → test_abrir_google
```

### 3. Execute
Clique no ▶️ ao lado de `test_abrir_google`

### 4. Veja o resultado
- ✅ Verde = Passou
- ❌ Vermelho = Falhou

### 5. Ver detalhes
Clique no teste para ver logs e detalhes

---

## 🎨 Personalize a Execução

### Ver o navegador (modo headed)

**No Test Explorer:**
Já está configurado! Os testes abrem o navegador automaticamente.

**Arquivo de configuração:**
`.vscode/settings.json` já tem `--headed` configurado

### Modo lento (ver as ações)

Edite `.vscode/settings.json` e adicione:
```json
{
  "python.testing.pytestArgs": [
    "tests",
    "-v",
    "--headed",
    "--slowmo=1000"  ← Adicione esta linha
  ]
}
```

### Capturar screenshots

Adicione:
```json
"--screenshot=on"
```

---

## 🐛 Debug de Teste

### Método 1: Breakpoint no VS Code

1. Abra o arquivo do teste
2. Clique na margem esquerda (linha fica com bolinha vermelha)
3. Clique com botão direito no teste no Test Explorer
4. Selecione **"Debug Test"**
5. Use F10 para avançar linha por linha

### Método 2: Pausar no código

Adicione no teste:
```python
def test_exemplo(page):
    page.goto("https://google.com")
    page.pause()  # ← Pausa aqui
```

---

## 💡 Dicas Rápidas

### ✅ Executar teste específico
Clique no ▶️ ao lado do nome do teste

### ✅ Executar todos de uma pasta
Clique no ▶️ ao lado da pasta

### ✅ Executar todos os testes
Clique no ▶️ no topo da árvore

### ✅ Re-executar testes falhados
Clique no ícone "Run Failed Tests"

### ✅ Filtrar testes
Use a barra de busca no Test Explorer

---

## 🎓 Próximos Passos

1. ✅ Execute `test_abrir_google` no Test Explorer
2. ✅ Execute `test_buscar_no_google` para ver busca
3. ✅ Dê duplo clique em `scripts/run_ui_mode.bat`
4. ✅ Gere um relatório HTML
5. ✅ Crie seu próprio teste!

---

## 📚 Documentação Completa

- **Guia Completo:** [COMO_EXECUTAR_TESTES.md](COMO_EXECUTAR_TESTES.md)
- **Test Explorer Detalhado:** [docs/COMO_USAR_TEST_EXPLORER.md](docs/COMO_USAR_TEST_EXPLORER.md)
- **Todas as Interfaces:** [docs/INTERFACES_GRAFICAS_TESTES.md](docs/INTERFACES_GRAFICAS_TESTES.md)
- **Exemplos de Código:** [tests/examples/README.md](tests/examples/README.md)

---

## 🆘 Problemas?

### Test Explorer não mostra testes?
1. Clique em 🔄 "Refresh Tests"
2. Aguarde alguns segundos
3. Verifique se pytest está instalado: `pip list | grep pytest`

### Navegador não abre?
Verifique se `--headed` está em `.vscode/settings.json`

### Testes muito rápidos?
Adicione `--slowmo=1000` nas configurações

---

## 🎉 Pronto para Começar!

**Agora é só:**
1. Abrir Test Explorer (🧪)
2. Clicar em Refresh (🔄)
3. Clicar em Run (▶️)

**Sem linha de comando! Sem complicação!** 🚀

---

**Dica Final:** Mantenha o Test Explorer aberto enquanto desenvolve. Assim você pode executar testes com um clique enquanto codifica! 💡
