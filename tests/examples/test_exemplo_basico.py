"""
Exemplo SUPER SIMPLES para começar.

Execute com: pytest tests/examples/test_exemplo_basico.py -v --headed
"""

import pytest
from playwright.sync_api import Page, expect


def test_abrir_google(page: Page):
    """Teste mais simples possível - apenas abrir o Google."""
    page.goto("https://www.google.com")
    expect(page).to_have_title("Google")
    print("✅ Google abriu com sucesso!")


def test_buscar_no_google(page: Page):
    """Teste simples de busca."""
    # Abrir Google
    page.goto("https://www.google.com")
    
    # Digitar no campo de busca
    page.fill("textarea[name='q']", "Python")
    
    # Pressionar Enter
    page.press("textarea[name='q']", "Enter")
    
    # Esperar resultados aparecerem
    page.wait_for_selector("#search")
    
    print("✅ Busca realizada com sucesso!")


def test_abrir_wikipedia(page: Page):
    """Teste simples - abrir Wikipedia em português."""
    page.goto("https://pt.wikipedia.org")
    expect(page).to_have_title("*Wikipedia*")
    print("✅ Wikipedia abriu com sucesso!")


def test_buscar_na_wikipedia(page: Page):
    """Teste simples de busca na Wikipedia."""
    # Abrir Wikipedia
    page.goto("https://pt.wikipedia.org")
    
    # Buscar por "Python"
    page.fill("input[name='search']", "Python")
    page.click("button[type='submit']")
    
    # Verificar que chegou na página de resultados
    page.wait_for_load_state("networkidle")
    
    # Verificar que tem conteúdo
    expect(page.locator("#mw-content-text")).to_be_visible()
    
    print("✅ Busca na Wikipedia realizada com sucesso!")


if __name__ == "__main__":
    print("Execute com: pytest tests/examples/test_exemplo_basico.py -v --headed")
