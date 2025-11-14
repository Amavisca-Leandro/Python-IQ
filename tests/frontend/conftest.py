"""
Frontend test fixtures for Playwright automation.

This module provides fixtures for frontend testing including:
- Browser configuration with Brazilian locale
- Authenticated page fixtures
- Multi-browser support (Chromium, Firefox, WebKit)
- Automatic screenshot capture on test failures
"""

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page
from typing import Dict, Any
from core.config.settings import get_settings
from core.ui.pages.login_page import LoginPage


@pytest.fixture(scope="session")
def browser_context_args() -> Dict[str, Any]:
    """
    Configure browser context with Brazilian locale and settings.
    
    Returns:
        Dict with browser context configuration including:
        - Brazilian locale (pt-BR)
        - Timezone (America/Sao_Paulo)
        - Viewport size
        - User agent
    """
    settings = get_settings()
    
    return {
        "locale": "pt-BR",
        "timezone_id": "America/Sao_Paulo",
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "accept_downloads": True,
        "ignore_https_errors": settings.env == "dev",  # Only ignore in dev
        "record_video_dir": "reports/videos" if not settings.headless else None,
        "record_video_size": {"width": 1920, "height": 1080},
    }


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """
    Create a new page for each test with automatic cleanup.
    
    Args:
        context: Browser context from pytest-playwright
        
    Yields:
        Page: New page instance
    """
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def authenticated_page(page: Page) -> Page:
    """
    Create an authenticated page by performing automatic login.
    
    This fixture:
    1. Navigates to login page
    2. Performs login with credentials from settings
    3. Waits for successful authentication
    4. Returns authenticated page ready for testing
    
    Args:
        page: Page instance from page fixture
        
    Returns:
        Page: Authenticated page instance
        
    Raises:
        AssertionError: If login fails
    """
    settings = get_settings()
    login_page = LoginPage(page)
    
    # Navigate to login page
    page.goto(settings.frontend_base_url)
    
    # Perform login
    login_page.login(
        username=settings.auth_user,
        password=settings.auth_password
    )
    
    # Verify successful login (wait for dashboard or home page)
    page.wait_for_url("**/dashboard", timeout=10000)
    
    return page


@pytest.fixture(scope="function")
def chromium_page(playwright) -> Page:
    """
    Create a Chromium browser page for cross-browser testing.
    
    Args:
        playwright: Playwright instance
        
    Yields:
        Page: Chromium page instance
    """
    browser = playwright.chromium.launch(headless=get_settings().headless)
    context = browser.new_context(**browser_context_args())
    page = context.new_page()
    
    yield page
    
    page.close()
    context.close()
    browser.close()


@pytest.fixture(scope="function")
def firefox_page(playwright) -> Page:
    """
    Create a Firefox browser page for cross-browser testing.
    
    Args:
        playwright: Playwright instance
        
    Yields:
        Page: Firefox page instance
    """
    browser = playwright.firefox.launch(headless=get_settings().headless)
    context = browser.new_context(**browser_context_args())
    page = context.new_page()
    
    yield page
    
    page.close()
    context.close()
    browser.close()


@pytest.fixture(scope="function")
def webkit_page(playwright) -> Page:
    """
    Create a WebKit browser page for cross-browser testing.
    
    Args:
        playwright: Playwright instance
        
    Yields:
        Page: WebKit page instance
    """
    browser = playwright.webkit.launch(headless=get_settings().headless)
    context = browser.new_context(**browser_context_args())
    page = context.new_page()
    
    yield page
    
    page.close()
    context.close()
    browser.close()



@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture screenshots on test failures.
    
    This hook:
    1. Runs after each test
    2. Checks if test failed
    3. Captures screenshot if page fixture is available
    4. Attaches screenshot to Allure report
    
    Args:
        item: Test item
        call: Test call information
    """
    outcome = yield
    rep = outcome.get_result()
    
    # Only capture screenshot on test failure during call phase
    if rep.when == "call" and rep.failed:
        # Check if test has page fixture
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            try:
                # Capture screenshot
                screenshot = page.screenshot()
                
                # Attach to Allure report
                allure.attach(
                    screenshot,
                    name=f"Screenshot on Failure - {item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # Also capture page HTML for debugging
                html = page.content()
                allure.attach(
                    html,
                    name=f"Page HTML - {item.name}",
                    attachment_type=allure.attachment_type.HTML
                )
                
                # Capture console logs if available
                try:
                    console_logs = page.evaluate("() => window.console.logs || []")
                    if console_logs:
                        allure.attach(
                            str(console_logs),
                            name=f"Console Logs - {item.name}",
                            attachment_type=allure.attachment_type.TEXT
                        )
                except Exception:
                    pass  # Console logs might not be available
                    
            except Exception as e:
                # If screenshot capture fails, log the error
                allure.attach(
                    f"Failed to capture screenshot: {str(e)}",
                    name="Screenshot Error",
                    attachment_type=allure.attachment_type.TEXT
                )
