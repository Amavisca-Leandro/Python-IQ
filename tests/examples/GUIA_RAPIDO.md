# Guia Rápido - Testes de UI com Playwright

## 🚀 Como Executar os Testes de Exemplo

### 1. Instalar Playwright (se ainda não instalou)

```bash
# Instalar o Playwright
pip install playwright

# Instalar os navegadores
playwright install
```

### 2. Executar os Testes

```bash
# Executar todos os testes de exemplo
pytest tests/examples/ -v

# Executar teste específico
pytest tests/examples/test_google_search.py -v

# Executar com navegador visível (não headless)
pytest tests/examples/test_google_search.py -v --headed

# Executar em modo lento (para ver as ações)
pytest tests/examples/test_google_search.py -v --headed --slowmo=1000
```

### 3. Executar com Diferentes Navegadores

```bash
# Chromium (padrão)
pytest tests/examples/ --browser chromium

# Firefox
pytest tests/examples/ --browser firefox

# WebKit (Safari)
pytest tests/examples/ --browser webkit

# Todos os navegadores
pytest tests/examples/ --browser chromium --browser firefox --browser webkit
```

## 📝 Estrutura Básica de um Teste

### Teste Simples

```python
import pytest
from playwright.sync_api import Page, expect

def test_exemplo_simples(page: Page):
    # 1. Navegar para a página
    page.goto("https://exemplo.com")
    
    # 2. Interagir com elementos
    page.locator("input[name='campo']").fill("texto")
    page.locator("button").click()
    
    # 3. Verificar resultados
    expect(page.locator(".resultado")).to_be_visible()
```

### Teste com Page Object

```python
class MinhaPage:
    def __init__(self, page: Page):
        self.page = page
        self.campo = page.locator("input[name='campo']")
        self.botao = page.locator("button")
    
    def preencher_e_enviar(self, texto: str):
        self.campo.fill(texto)
        self.botao.click()

def test_com_page_object(page: Page):
    minha_page = MinhaPage(page)
    minha_page.preencher_e_enviar("teste")
```

## 🎯 Principais Comandos do Playwright

### Navegação

```python
# Ir para URL
page.goto("https://exemplo.com")

# Voltar
page.go_back()

# Avançar
page.go_forward()

# Recarregar
page.reload()
```

### Localizar Elementos

```python
# Por seletor CSS
page.locator("button.submit")

# Por texto
page.locator("text=Clique aqui")

# Por role
page.locator("role=button[name='Enviar']")

# Por ID
page.locator("#meu-id")

# Por atributo
page.locator("input[name='email']")
```

### Interações

```python
# Clicar
page.locator("button").click()

# Preencher texto
page.locator("input").fill("texto")

# Pressionar tecla
page.locator("input").press("Enter")

# Selecionar opção
page.locator("select").select_option("valor")

# Marcar checkbox
page.locator("input[type='checkbox']").check()

# Desmarcar checkbox
page.locator("input[type='checkbox']").uncheck()

# Fazer upload de arquivo
page.locator("input[type='file']").set_input_files("caminho/arquivo.pdf")
```

### Verificações (Assertions)

```python
from playwright.sync_api import expect

# Verificar visibilidade
expect(page.locator("button")).to_be_visible()

# Verificar texto
expect(page.locator("h1")).to_have_text("Título")

# Verificar URL
expect(page).to_have_url("https://exemplo.com/pagina")

# Verificar título
expect(page).to_have_title("Meu Site")

# Verificar atributo
expect(page.locator("input")).to_have_attribute("disabled", "")

# Verificar contagem
expect(page.locator(".item")).to_have_count(5)
```

### Esperas

```python
# Esperar elemento estar visível
page.locator("button").wait_for(state="visible")

# Esperar navegação
page.wait_for_url("**/resultado")

# Esperar por timeout específico
page.wait_for_timeout(2000)  # 2 segundos

# Esperar rede ficar idle
page.wait_for_load_state("networkidle")
```

## 🎨 Configurações Úteis

### No arquivo pytest.ini

```ini
[pytest]
# Executar com navegador visível
addopts = --headed

# Modo lento (ver ações)
addopts = --slowmo=500

# Capturar screenshots em falhas
addopts = --screenshot=on

# Capturar vídeos
addopts = --video=on
```

### No arquivo .env

```env
# Configurações do navegador
HEADLESS=false
SLOW_MO=1000
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080

# URLs para testar
FRONTEND_BASE_URL=https://seu-site.com
```

## 📸 Capturar Screenshots e Vídeos

```python
def test_com_screenshot(page: Page):
    page.goto("https://exemplo.com")
    
    # Capturar screenshot
    page.screenshot(path="screenshot.png")
    
    # Screenshot de elemento específico
    page.locator(".elemento").screenshot(path="elemento.png")
    
    # Screenshot de página inteira
    page.screenshot(path="pagina-completa.png", full_page=True)
```

## 🔍 Debug

```python
def test_com_debug(page: Page):
    page.goto("https://exemplo.com")
    
    # Pausar execução para debug
    page.pause()
    
    # Imprimir HTML do elemento
    print(page.locator("div").inner_html())
    
    # Imprimir texto
    print(page.locator("h1").text_content())
```

## 💡 Dicas

1. **Use `expect()` ao invés de `assert`** - Tem retry automático
2. **Prefira locators por role ou texto** - Mais resilientes
3. **Evite `wait_for_timeout()`** - Use esperas específicas
4. **Use Page Objects** - Código mais organizado e reutilizável
5. **Capture screenshots em falhas** - Facilita debug

## 📚 Exemplos Prontos

- `test_google_search.py` - Exemplo básico com Google
- `test_wikipedia.py` - Exemplo avançado com Page Objects

## 🆘 Problemas Comuns

### Elemento não encontrado
```python
# ❌ Errado - pode falhar se elemento demora
page.locator("button").click()

# ✅ Correto - espera automática
expect(page.locator("button")).to_be_visible()
page.locator("button").click()
```

### Timeout
```python
# Aumentar timeout específico
page.locator("button").click(timeout=30000)  # 30 segundos

# Ou configurar globalmente no conftest.py
page.set_default_timeout(30000)
```

### Elemento coberto por outro
```python
# Forçar clique
page.locator("button").click(force=True)

# Ou rolar até o elemento
page.locator("button").scroll_into_view_if_needed()
page.locator("button").click()
```

## 🎓 Próximos Passos

1. Crie seus próprios Page Objects em `core/ui/pages/`
2. Use as fixtures do `tests/frontend/conftest.py`
3. Integre com API e Database como nos exemplos de integração
4. Configure relatórios HTML com Allure

Boa sorte com seus testes! 🚀
