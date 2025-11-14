"""
Exemplo simples de teste de UI - Busca no Google.

Este é um exemplo básico para demonstrar como testar uma página web real.
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.frontend
class TestGoogleSearch:
    """Testes de exemplo usando o Google."""
    
    def test_google_homepage_loads(self, page: Page):
        """
        Teste simples: verificar se a página do Google carrega.
        
        Este teste demonstra:
        - Navegação para uma URL
        - Verificação de título da página
        - Verificação de elemento visível
        """
        # Navegar para o Google
        page.goto("https://www.google.com")
        
        # Verificar título da página
        expect(page).to_have_title("Google")
        
        # Verificar que o campo de busca está visível
        search_box = page.locator("textarea[name='q']")
        expect(search_box).to_be_visible()
    
    def test_google_search_functionality(self, page: Page):
        """
        Teste de busca no Google.
        
        Este teste demonstra:
        - Preencher campo de texto
        - Pressionar tecla Enter
        - Esperar por navegação
        - Verificar resultados
        """
        # Navegar para o Google
        page.goto("https://www.google.com")
        
        # Preencher campo de busca
        search_box = page.locator("textarea[name='q']")
        search_box.fill("Playwright Python")
        
        # Pressionar Enter para buscar
        search_box.press("Enter")
        
        # Esperar pela página de resultados
        page.wait_for_url("**/search?q=*", timeout=10000)
        
        # Verificar que há resultados
        results = page.locator("#search")
        expect(results).to_be_visible()
        
        # Verificar que o termo de busca aparece na página
        expect(page).to_have_url("*Playwright*Python*")
    
    def test_google_im_feeling_lucky(self, page: Page):
        """
        Teste do botão 'Estou com sorte'.
        
        Este teste demonstra:
        - Interação com botões
        - Verificação de navegação
        """
        # Navegar para o Google
        page.goto("https://www.google.com")
        
        # Preencher campo de busca
        search_box = page.locator("textarea[name='q']")
        search_box.fill("Python")
        
        # Clicar no botão "Estou com sorte" (se visível)
        # Nota: Este botão pode não estar sempre visível
        lucky_button = page.locator("input[name='btnI']")
        
        if lucky_button.is_visible():
            lucky_button.click()
            
            # Verificar que navegou para algum resultado
            page.wait_for_load_state("networkidle")
            
            # Verificar que não está mais na página do Google
            assert "google.com/search" not in page.url
