"""
Exemplo avançado de teste de UI - Wikipedia.

Este exemplo demonstra o uso do padrão Page Object Model.
"""

import pytest
from playwright.sync_api import Page, expect


class WikipediaHomePage:
    """Page Object para a página inicial da Wikipedia."""
    
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.locator("input[name='search']")
        self.search_button = page.locator("button[type='submit']")
    
    def navigate(self):
        """Navegar para a Wikipedia."""
        self.page.goto("https://pt.wikipedia.org")
        self.page.wait_for_load_state("networkidle")
    
    def search(self, term: str):
        """Realizar uma busca."""
        self.search_input.fill(term)
        self.search_button.click()
        self.page.wait_for_load_state("networkidle")
    
    def is_loaded(self) -> bool:
        """Verificar se a página carregou."""
        return self.search_input.is_visible()


class WikipediaArticlePage:
    """Page Object para uma página de artigo da Wikipedia."""
    
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator("h1.firstHeading")
        self.content = page.locator("#mw-content-text")
        self.toc = page.locator("#toc")
    
    def get_title(self) -> str:
        """Obter título do artigo."""
        return self.title.text_content()
    
    def has_table_of_contents(self) -> bool:
        """Verificar se tem índice."""
        return self.toc.is_visible()
    
    def click_section(self, section_name: str):
        """Clicar em uma seção do índice."""
        section_link = self.page.locator(f"text={section_name}")
        section_link.first.click()


@pytest.mark.frontend
class TestWikipedia:
    """Testes de exemplo usando a Wikipedia."""
    
    def test_wikipedia_homepage_loads(self, page: Page):
        """Verificar se a página inicial da Wikipedia carrega."""
        wiki_home = WikipediaHomePage(page)
        wiki_home.navigate()
        
        assert wiki_home.is_loaded()
        expect(page).to_have_title("*Wikipedia*")
    
    def test_wikipedia_search(self, page: Page):
        """Testar busca na Wikipedia."""
        # Navegar e buscar
        wiki_home = WikipediaHomePage(page)
        wiki_home.navigate()
        wiki_home.search("Python (linguagem de programação)")
        
        # Verificar artigo
        article = WikipediaArticlePage(page)
        title = article.get_title()
        
        assert "Python" in title
        expect(article.content).to_be_visible()
    
    def test_wikipedia_article_has_toc(self, page: Page):
        """Verificar se artigos têm índice."""
        # Navegar para artigo específico
        page.goto("https://pt.wikipedia.org/wiki/Brasil")
        page.wait_for_load_state("networkidle")
        
        # Verificar índice
        article = WikipediaArticlePage(page)
        assert article.has_table_of_contents()
        
        # Verificar título
        title = article.get_title()
        assert "Brasil" in title
    
    def test_wikipedia_language_switch(self, page: Page):
        """Testar troca de idioma."""
        # Ir para artigo em português
        page.goto("https://pt.wikipedia.org/wiki/Python_(linguagem_de_programação)")
        page.wait_for_load_state("networkidle")
        
        # Clicar no link de idioma (English)
        language_link = page.locator("a[lang='en']").first
        
        if language_link.is_visible():
            language_link.click()
            page.wait_for_load_state("networkidle")
            
            # Verificar que mudou para inglês
            assert "en.wikipedia.org" in page.url
