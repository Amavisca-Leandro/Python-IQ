"""
Base Page Object with common functionality for Playwright automation.

This module provides a BasePage class that wraps Playwright functionality
with logging, error handling, and automatic screenshot capture on failures.
"""

import logging
from typing import Optional, List, Any
from pathlib import Path
from datetime import datetime

from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError


logger = logging.getLogger(__name__)


class BasePage:
    """
    Base Page Object class with common functionality for all page objects.
    
    This class provides:
    - Wrapper over Playwright with detailed logging
    - Standardized methods for common actions (click, fill, wait)
    - Automatic screenshot capture on failures
    - Error handling and retry logic
    - Wait strategies for element interactions
    
    Attributes:
        page: Playwright Page instance
        base_url: Base URL for the application
        timeout: Default timeout for operations in milliseconds
        screenshot_dir: Directory for storing screenshots
    
    Example:
        >>> class LoginPage(BasePage):
        ...     def __init__(self, page: Page):
        ...         super().__init__(page, base_url="https://app.example.com")
        ...     
        ...     def login(self, username: str, password: str):
        ...         self.fill("#username", username)
        ...         self.fill("#password", password)
        ...         self.click("#login-button")
    """
    
    def __init__(
        self,
        page: Page,
        base_url: str = "",
        timeout: int = 30000,
        screenshot_dir: str = "reports/screenshots"
    ):
        """
        Initialize BasePage with Playwright page instance.
        
        Args:
            page: Playwright Page instance
            base_url: Base URL for the application
            timeout: Default timeout in milliseconds (default: 30000)
            screenshot_dir: Directory for screenshots (default: reports/screenshots)
        """
        self.page = page
        self.base_url = base_url
        self.timeout = timeout
        self.screenshot_dir = Path(screenshot_dir)
        
        # Create screenshot directory if it doesn't exist
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"BasePage initialized with base_url: {base_url}, timeout: {timeout}ms")
    
    # ============================================================================
    # NAVIGATION METHODS
    # ============================================================================
    
    def navigate_to(self, path: str = "", wait_until: str = "networkidle") -> None:
        """
        Navigate to a URL or path.
        
        Args:
            path: URL path to navigate to (appended to base_url if relative)
            wait_until: When to consider navigation complete
                       Options: 'load', 'domcontentloaded', 'networkidle', 'commit'
        
        Raises:
            PlaywrightTimeoutError: If navigation times out
        
        Example:
            >>> page.navigate_to("/login")
            >>> page.navigate_to("https://example.com/dashboard")
        """
        url = f"{self.base_url}{path}" if not path.startswith("http") else path
        
        logger.info(f"Navigating to: {url}")
        
        try:
            self.page.goto(url, wait_until=wait_until, timeout=self.timeout)
            logger.info(f"Successfully navigated to: {url}")
        except PlaywrightTimeoutError as e:
            logger.error(f"Navigation timeout to {url}: {e}")
            self._take_screenshot(f"navigation_timeout_{self._get_timestamp()}")
            raise
        except Exception as e:
            logger.error(f"Navigation failed to {url}: {e}")
            self._take_screenshot(f"navigation_error_{self._get_timestamp()}")
            raise
    
    def reload(self, wait_until: str = "networkidle") -> None:
        """
        Reload the current page.
        
        Args:
            wait_until: When to consider reload complete
        """
        logger.info("Reloading page")
        try:
            self.page.reload(wait_until=wait_until, timeout=self.timeout)
            logger.info("Page reloaded successfully")
        except Exception as e:
            logger.error(f"Page reload failed: {e}")
            self._take_screenshot(f"reload_error_{self._get_timestamp()}")
            raise
    
    def go_back(self, wait_until: str = "networkidle") -> None:
        """
        Navigate back in browser history.
        
        Args:
            wait_until: When to consider navigation complete
        """
        logger.info("Navigating back")
        try:
            self.page.go_back(wait_until=wait_until, timeout=self.timeout)
            logger.info("Navigated back successfully")
        except Exception as e:
            logger.error(f"Go back failed: {e}")
            raise
    
    # ============================================================================
    # ELEMENT INTERACTION METHODS
    # ============================================================================
    
    def click(
        self,
        selector: str,
        timeout: Optional[int] = None,
        force: bool = False,
        button: str = "left"
    ) -> None:
        """
        Click on an element.
        
        Args:
            selector: CSS selector or text selector
            timeout: Custom timeout in milliseconds (uses default if None)
            force: Force click even if element is not actionable
            button: Mouse button to click ('left', 'right', 'middle')
        
        Raises:
            PlaywrightTimeoutError: If element not found within timeout
        
        Example:
            >>> page.click("#submit-button")
            >>> page.click("text=Login")
            >>> page.click("#menu", button="right")
        """
        timeout = timeout or self.timeout
        logger.info(f"Clicking element: {selector}")
        
        try:
            self.wait_for_selector(selector, timeout=timeout)
            self.page.click(selector, timeout=timeout, force=force, button=button)
            logger.info(f"Successfully clicked: {selector}")
        except PlaywrightTimeoutError as e:
            logger.error(f"Click timeout on {selector}: {e}")
            self._take_screenshot(f"click_timeout_{self._sanitize_selector(selector)}")
            raise
        except Exception as e:
            logger.error(f"Click failed on {selector}: {e}")
            self._take_screenshot(f"click_error_{self._sanitize_selector(selector)}")
            raise
    
    def fill(
        self,
        selector: str,
        value: str,
        timeout: Optional[int] = None,
        clear_first: bool = True
    ) -> None:
        """
        Fill an input field with text.
        
        Args:
            selector: CSS selector for the input field
            value: Text to fill
            timeout: Custom timeout in milliseconds
            clear_first: Clear field before filling
        
        Example:
            >>> page.fill("#username", "test_user")
            >>> page.fill("#email", "test@example.com", clear_first=False)
        """
        timeout = timeout or self.timeout
        logger.info(f"Filling element {selector} with value: {value}")
        
        try:
            self.wait_for_selector(selector, timeout=timeout)
            
            if clear_first:
                self.page.fill(selector, "", timeout=timeout)
            
            self.page.fill(selector, value, timeout=timeout)
            logger.info(f"Successfully filled {selector}")
        except PlaywrightTimeoutError as e:
            logger.error(f"Fill timeout on {selector}: {e}")
            self._take_screenshot(f"fill_timeout_{self._sanitize_selector(selector)}")
            raise
        except Exception as e:
            logger.error(f"Fill failed on {selector}: {e}")
            self._take_screenshot(f"fill_error_{self._sanitize_selector(selector)}")
            raise
    
    def type_text(
        self,
        selector: str,
        text: str,
        delay: int = 0,
        timeout: Optional[int] = None
    ) -> None:
        """
        Type text character by character (simulates real typing).
        
        Args:
            selector: CSS selector for the input field
            text: Text to type
            delay: Delay between keystrokes in milliseconds
            timeout: Custom timeout in milliseconds
        
        Example:
            >>> page.type_text("#search", "automation", delay=100)
        """
        timeout = timeout or self.timeout
        logger.info(f"Typing text into {selector}: {text}")
        
        try:
            self.wait_for_selector(selector, timeout=timeout)
            self.page.type(selector, text, delay=delay, timeout=timeout)
            logger.info(f"Successfully typed into {selector}")
        except Exception as e:
            logger.error(f"Type failed on {selector}: {e}")
            self._take_screenshot(f"type_error_{self._sanitize_selector(selector)}")
            raise
    
    def select_option(
        self,
        selector: str,
        value: Optional[str] = None,
        label: Optional[str] = None,
        index: Optional[int] = None,
        timeout: Optional[int] = None
    ) -> None:
        """
        Select an option from a dropdown.
        
        Args:
            selector: CSS selector for the select element
            value: Option value to select
            label: Option label to select
            index: Option index to select
            timeout: Custom timeout in milliseconds
        
        Example:
            >>> page.select_option("#country", value="BR")
            >>> page.select_option("#country", label="Brazil")
            >>> page.select_option("#country", index=0)
        """
        timeout = timeout or self.timeout
        logger.info(f"Selecting option in {selector}")
        
        try:
            self.wait_for_selector(selector, timeout=timeout)
            
            if value:
                self.page.select_option(selector, value=value, timeout=timeout)
            elif label:
                self.page.select_option(selector, label=label, timeout=timeout)
            elif index is not None:
                self.page.select_option(selector, index=index, timeout=timeout)
            else:
                raise ValueError("Must provide value, label, or index")
            
            logger.info(f"Successfully selected option in {selector}")
        except Exception as e:
            logger.error(f"Select option failed on {selector}: {e}")
            self._take_screenshot(f"select_error_{self._sanitize_selector(selector)}")
            raise
    
    def check(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Check a checkbox or radio button.
        
        Args:
            selector: CSS selector for the checkbox/radio
            timeout: Custom timeout in milliseconds
        
        Example:
            >>> page.check("#terms-checkbox")
        """
        timeout = timeout or self.timeout
        logger.info(f"Checking element: {selector}")
        
        try:
            self.wait_for_selector(selector, timeout=timeout)
            self.page.check(selector, timeout=timeout)
            logger.info(f"Successfully checked {selector}")
        except Exception as e:
            logger.error(f"Check failed on {selector}: {e}")
            self._take_screenshot(f"check_error_{self._sanitize_selector(selector)}")
            raise
    
    def uncheck(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Uncheck a checkbox.
        
        Args:
            selector: CSS selector for the checkbox
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        logger.info(f"Unchecking element: {selector}")
        
        try:
            self.wait_for_selector(selector, timeout=timeout)
            self.page.uncheck(selector, timeout=timeout)
            logger.info(f"Successfully unchecked {selector}")
        except Exception as e:
            logger.error(f"Uncheck failed on {selector}: {e}")
            raise
    
    # ============================================================================
    # WAIT METHODS
    # ============================================================================
    
    def wait_for_selector(
        self,
        selector: str,
        state: str = "visible",
        timeout: Optional[int] = None
    ) -> Locator:
        """
        Wait for an element to be in a specific state.
        
        Args:
            selector: CSS selector for the element
            state: Element state to wait for
                   Options: 'attached', 'detached', 'visible', 'hidden'
            timeout: Custom timeout in milliseconds
        
        Returns:
            Locator: Playwright Locator for the element
        
        Example:
            >>> page.wait_for_selector("#loading-spinner", state="hidden")
            >>> page.wait_for_selector("#content", state="visible")
        """
        timeout = timeout or self.timeout
        logger.debug(f"Waiting for selector {selector} to be {state}")
        
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state=state, timeout=timeout)
            logger.debug(f"Selector {selector} is {state}")
            return locator
        except PlaywrightTimeoutError as e:
            logger.error(f"Wait timeout for {selector} to be {state}: {e}")
            self._take_screenshot(f"wait_timeout_{self._sanitize_selector(selector)}")
            raise
    
    def wait_for_url(
        self,
        url: str,
        timeout: Optional[int] = None,
        wait_until: str = "load"
    ) -> None:
        """
        Wait for URL to match a pattern.
        
        Args:
            url: URL pattern to wait for (can be string or regex)
            timeout: Custom timeout in milliseconds
            wait_until: When to consider navigation complete
        
        Example:
            >>> page.wait_for_url("/dashboard")
            >>> page.wait_for_url("**/profile/**")
        """
        timeout = timeout or self.timeout
        logger.info(f"Waiting for URL: {url}")
        
        try:
            self.page.wait_for_url(url, timeout=timeout, wait_until=wait_until)
            logger.info(f"URL matched: {url}")
        except PlaywrightTimeoutError as e:
            logger.error(f"Wait for URL timeout: {url}: {e}")
            self._take_screenshot(f"url_timeout_{self._get_timestamp()}")
            raise
    
    def wait_for_load_state(
        self,
        state: str = "load",
        timeout: Optional[int] = None
    ) -> None:
        """
        Wait for page to reach a specific load state.
        
        Args:
            state: Load state to wait for
                   Options: 'load', 'domcontentloaded', 'networkidle'
            timeout: Custom timeout in milliseconds
        
        Example:
            >>> page.wait_for_load_state("networkidle")
        """
        timeout = timeout or self.timeout
        logger.debug(f"Waiting for load state: {state}")
        
        try:
            self.page.wait_for_load_state(state, timeout=timeout)
            logger.debug(f"Load state reached: {state}")
        except Exception as e:
            logger.error(f"Wait for load state failed: {e}")
            raise
    
    def wait_for_timeout(self, timeout: int) -> None:
        """
        Wait for a specific amount of time (use sparingly).
        
        Args:
            timeout: Time to wait in milliseconds
        
        Note:
            Prefer explicit waits over fixed timeouts when possible.
        
        Example:
            >>> page.wait_for_timeout(1000)  # Wait 1 second
        """
        logger.debug(f"Waiting for {timeout}ms")
        self.page.wait_for_timeout(timeout)
    
    # ============================================================================
    # ELEMENT QUERY METHODS
    # ============================================================================
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Get text content of an element.
        
        Args:
            selector: CSS selector for the element
            timeout: Custom timeout in milliseconds
        
        Returns:
            str: Text content of the element
        
        Example:
            >>> username = page.get_text("#username-display")
        """
        timeout = timeout or self.timeout
        logger.debug(f"Getting text from: {selector}")
        
        try:
            self.wait_for_selector(selector, timeout=timeout)
            text = self.page.text_content(selector, timeout=timeout)
            logger.debug(f"Text from {selector}: {text}")
            return text or ""
        except Exception as e:
            logger.error(f"Get text failed on {selector}: {e}")
            raise
    
    def get_attribute(
        self,
        selector: str,
        attribute: str,
        timeout: Optional[int] = None
    ) -> Optional[str]:
        """
        Get attribute value of an element.
        
        Args:
            selector: CSS selector for the element
            attribute: Attribute name
            timeout: Custom timeout in milliseconds
        
        Returns:
            Optional[str]: Attribute value or None
        
        Example:
            >>> href = page.get_attribute("#link", "href")
            >>> disabled = page.get_attribute("#button", "disabled")
        """
        timeout = timeout or self.timeout
        logger.debug(f"Getting attribute {attribute} from: {selector}")
        
        try:
            self.wait_for_selector(selector, timeout=timeout)
            value = self.page.get_attribute(selector, attribute, timeout=timeout)
            logger.debug(f"Attribute {attribute} from {selector}: {value}")
            return value
        except Exception as e:
            logger.error(f"Get attribute failed on {selector}: {e}")
            raise
    
    def is_visible(self, selector: str, timeout: int = 1000) -> bool:
        """
        Check if an element is visible.
        
        Args:
            selector: CSS selector for the element
            timeout: Timeout in milliseconds (short timeout for quick check)
        
        Returns:
            bool: True if visible, False otherwise
        
        Example:
            >>> if page.is_visible("#error-message"):
            ...     print("Error is displayed")
        """
        try:
            self.page.wait_for_selector(
                selector,
                state="visible",
                timeout=timeout
            )
            return True
        except PlaywrightTimeoutError:
            return False
    
    def is_enabled(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        Check if an element is enabled.
        
        Args:
            selector: CSS selector for the element
            timeout: Custom timeout in milliseconds
        
        Returns:
            bool: True if enabled, False otherwise
        """
        timeout = timeout or self.timeout
        try:
            self.wait_for_selector(selector, timeout=timeout)
            return self.page.is_enabled(selector, timeout=timeout)
        except Exception:
            return False
    
    def is_checked(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        Check if a checkbox/radio is checked.
        
        Args:
            selector: CSS selector for the element
            timeout: Custom timeout in milliseconds
        
        Returns:
            bool: True if checked, False otherwise
        """
        timeout = timeout or self.timeout
        try:
            self.wait_for_selector(selector, timeout=timeout)
            return self.page.is_checked(selector, timeout=timeout)
        except Exception:
            return False
    
    def get_elements_count(self, selector: str) -> int:
        """
        Get count of elements matching selector.
        
        Args:
            selector: CSS selector for the elements
        
        Returns:
            int: Number of matching elements
        
        Example:
            >>> count = page.get_elements_count(".list-item")
        """
        return self.page.locator(selector).count()
    
    # ============================================================================
    # SCREENSHOT & DEBUGGING METHODS
    # ============================================================================
    
    def take_screenshot(self, name: str, full_page: bool = False) -> Path:
        """
        Take a screenshot of the current page.
        
        Args:
            name: Screenshot filename (without extension)
            full_page: Capture full scrollable page
        
        Returns:
            Path: Path to the saved screenshot
        
        Example:
            >>> page.take_screenshot("login_page")
            >>> page.take_screenshot("full_dashboard", full_page=True)
        """
        return self._take_screenshot(name, full_page)
    
    def _take_screenshot(self, name: str, full_page: bool = False) -> Path:
        """
        Internal method to take screenshot with error handling.
        
        Args:
            name: Screenshot filename
            full_page: Capture full scrollable page
        
        Returns:
            Path: Path to the saved screenshot
        """
        try:
            screenshot_path = self.screenshot_dir / f"{name}.png"
            self.page.screenshot(path=str(screenshot_path), full_page=full_page)
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return Path()
    
    def get_page_title(self) -> str:
        """
        Get the page title.
        
        Returns:
            str: Page title
        """
        title = self.page.title()
        logger.debug(f"Page title: {title}")
        return title
    
    def get_current_url(self) -> str:
        """
        Get the current page URL.
        
        Returns:
            str: Current URL
        """
        url = self.page.url
        logger.debug(f"Current URL: {url}")
        return url
    
    def get_console_logs(self) -> List[str]:
        """
        Get console logs from the browser.
        
        Returns:
            List[str]: List of console messages
        
        Note:
            Console logs must be captured using page.on("console") event.
        """
        # This requires setting up console log capture in fixtures
        # Implementation depends on how console logs are stored
        logger.debug("Getting console logs")
        return []
    
    # ============================================================================
    # UTILITY METHODS
    # ============================================================================
    
    def execute_script(self, script: str, *args: Any) -> Any:
        """
        Execute JavaScript in the page context.
        
        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script
        
        Returns:
            Any: Result of the script execution
        
        Example:
            >>> page.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            >>> result = page.execute_script("return document.title")
        """
        logger.debug(f"Executing script: {script[:50]}...")
        try:
            result = self.page.evaluate(script, *args)
            logger.debug(f"Script executed successfully")
            return result
        except Exception as e:
            logger.error(f"Script execution failed: {e}")
            raise
    
    def scroll_to_element(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Scroll element into view.
        
        Args:
            selector: CSS selector for the element
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        logger.debug(f"Scrolling to element: {selector}")
        
        try:
            locator = self.wait_for_selector(selector, timeout=timeout)
            locator.scroll_into_view_if_needed(timeout=timeout)
            logger.debug(f"Scrolled to {selector}")
        except Exception as e:
            logger.error(f"Scroll to element failed: {e}")
            raise
    
    def hover(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Hover over an element.
        
        Args:
            selector: CSS selector for the element
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        logger.debug(f"Hovering over: {selector}")
        
        try:
            self.wait_for_selector(selector, timeout=timeout)
            self.page.hover(selector, timeout=timeout)
            logger.debug(f"Hovered over {selector}")
        except Exception as e:
            logger.error(f"Hover failed on {selector}: {e}")
            raise
    
    def press_key(self, key: str, selector: Optional[str] = None) -> None:
        """
        Press a keyboard key.
        
        Args:
            key: Key to press (e.g., 'Enter', 'Escape', 'Tab')
            selector: Optional selector to focus before pressing key
        
        Example:
            >>> page.press_key("Enter", "#search-input")
            >>> page.press_key("Escape")
        """
        logger.debug(f"Pressing key: {key}")
        
        try:
            if selector:
                self.page.press(selector, key)
            else:
                self.page.keyboard.press(key)
            logger.debug(f"Key pressed: {key}")
        except Exception as e:
            logger.error(f"Press key failed: {e}")
            raise
    
    @staticmethod
    def _sanitize_selector(selector: str) -> str:
        """
        Sanitize selector for use in filenames.
        
        Args:
            selector: CSS selector
        
        Returns:
            str: Sanitized selector
        """
        return selector.replace("#", "").replace(".", "").replace(" ", "_")[:50]
    
    @staticmethod
    def _get_timestamp() -> str:
        """
        Get current timestamp for filenames.
        
        Returns:
            str: Timestamp string
        """
        return datetime.now().strftime("%Y%m%d_%H%M%S")
