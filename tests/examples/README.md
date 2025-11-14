# 🎯 Exemplos de Testes de UI

Esta pasta contém exemplos práticos de como usar o framework de testes de UI com Playwright.

## 🚀 Começando AGORA

### 1. Instalar Playwright (se ainda não instalou)

```bash
pip install playwright pytest-playwright
playwright install chromium
```

### 2. Executar o Exemplo Mais Simples

```bash
# Com navegador visível (recomendado para aprender)
pytest tests/examples/test_exemplo_basico.py -v --headed

# Modo lento para ver as ações (1 segundo entre cada ação)
pytest tests/examples/test_exemplo_basico.py -v --headed --slowmo=1000

# Modo headless (sem abrir navegador)
pytest tests/examples/test_exemplo_basico.py -v
```

## 📁 Arquivos de Exemplo

### `test_exemplo_basico.py` ⭐ COMECE AQUI
Exemplos super simples para você começar:
- Abrir Google
- Fazer busca no Google
- Abrir Wikipedia
- Buscar na Wikipedia

**Execute:**
```bash
pytest tests/examples/test_exemplo_basico.py -v --headed
```

### `test_google_search.py`
Exemplos intermediários usando Google:
- Verificar homepage
- Testar busca
- Testar "Estou com sorte"

**Execute:**
```bash
pytest tests/examples/test_google_search.py -v --headed
```

### `test_wikipedia.py`
Exemplo avançado com Page Object Model:
- Uso de classes para organizar código
- Reutilização de código
- Testes mais complexos

**Execute:**
```bash
pytest tests/examples/test_wikipedia.py -v --headed
```

## 🎓 Guias

- **`GUIA_RAPIDO.md`** - Guia completo com todos os comandos e dicas

## 💡 Comandos Úteis

```bash
# Ver o navegador em ação (modo headed)
pytest tests/examples/ -v --headed

# Modo lento (ver cada ação)
pytest tests/examples/ -v --headed --slowmo=1000

# Executar teste específico
pytest tests/examples/test_exemplo_basico.py::test_abrir_google -v --headed

# Executar com Firefox
pytest tests/examples/ -v --headed --browser firefox

# Capturar screenshots em falhas
pytest tests/examples/ -v --screenshot=on

# Capturar vídeos
pytest tests/examples/ -v --video=on
```

## 🎯 Próximos Passos

1. **Execute os exemplos básicos** para ver como funciona
2. **Leia o GUIA_RAPIDO.md** para aprender os comandos
3. **Crie seu próprio teste** baseado nos exemplos
4. **Use Page Objects** para organizar melhor seu código

## 🆘 Precisa de Ajuda?

### Erro: "playwright not found"
```bash
pip install playwright pytest-playwright
playwright install
```

### Erro: "Browser not found"
```bash
playwright install chromium
```

### Teste muito rápido, não consigo ver
```bash
pytest tests/examples/test_exemplo_basico.py -v --headed --slowmo=2000
```

### Quero pausar o teste para inspecionar
Adicione no seu teste:
```python
page.pause()  # Abre o Playwright Inspector
```

## 🎨 Personalize Seus Testes

### Criar novo teste

1. Crie arquivo `test_meu_teste.py` nesta pasta
2. Use este template:

```python
import pytest
from playwright.sync_api import Page, expect

def test_meu_primeiro_teste(page: Page):
    """Descrição do que o teste faz."""
    # Navegar para site
    page.goto("https://exemplo.com")
    
    # Interagir com elementos
    page.fill("input[name='campo']", "valor")
    page.click("button")
    
    # Verificar resultado
    expect(page.locator(".resultado")).to_be_visible()
```

3. Execute:
```bash
pytest tests/examples/test_meu_teste.py -v --headed
```

## 📚 Recursos Adicionais

- [Documentação Playwright](https://playwright.dev/python/)
- [Seletores CSS](https://www.w3schools.com/cssref/css_selectors.php)
- [Guia Rápido](GUIA_RAPIDO.md)

---

**Dica:** Sempre execute com `--headed` quando estiver aprendendo para ver o que está acontecendo! 🎯
