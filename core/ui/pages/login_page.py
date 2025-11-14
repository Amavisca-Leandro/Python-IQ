"""
Login Page Object for authentication flows.

This module provides the LoginPage class for handling login interactions
including username/password authentication, error validation, and navigation.
"""

import logging
from typing import Optional

from playwright.sync_api import Page

from core.ui.base_page import BasePage


logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """
    Page Object for the Login page.
    
    This class encapsulates all interactions with the login page including:
    - Username and password input
    - Login button interaction
    - Error message validation
    - Remember me checkbox
    - Forgot password link
    - Social login options
    
    Attributes:
        All locators are defined as class constants for easy maintenance
    
    Example:
        >>> login_page = LoginPage(page)
        >>> login_page.navigate_to()
        >>> login_page.login("user@example.com", "password123")
        >>> assert login_page.is_logged_in()
    """
    
    # ============================================================================
    # LOCATORS
    # ============================================================================
    
    # Input fields
    USERNAME_INPUT = "#username"
    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#password"
    
    # Buttons
    LOGIN_BUTTON = "#login-button"
    SUBMIT_BUTTON = "button[type='submit']"
    
    # Links
    FORGOT_PASSWORD_LINK = "a[href*='forgot-password']"
    SIGNUP_LINK = "a[href*='signup']"
    
    # Messages
    ERROR_MESSAGE = ".error-message"
    SUCCESS_MESSAGE = ".success-message"
    VALIDATION_ERROR = ".validation-error"
    
    # Other elements
    REMEMBER_ME_CHECKBOX = "#remember-me"
    SHOW_PASSWORD_BUTTON = "#show-password"
    
    # Social login
    GOOGLE_LOGIN_BUTTON = "#google-login"
    FACEBOOK_LOGIN_BUTTON = "#facebook-login"
    
    # Page identifiers
    LOGIN_FORM = "#login-form"
    PAGE_TITLE = "h1"
    
    def __init__(self, page: Page, base_url: str = ""):
        """
        Initialize LoginPage.
        
        Args:
            page: Playwright Page instance
            base_url: Base URL for the application
        """
        super().__init__(page, base_url)
        logger.info("LoginPage initialized")
    
    # ============================================================================
    # NAVIGATION METHODS
    # ============================================================================
    
    def navigate_to(self, wait_until: str = "networkidle") -> None:
        """
        Navigate to the login page.
        
        Args:
            wait_until: When to consider navigation complete
        """
        super().navigate_to("/login", wait_until=wait_until)
        self.wait_for_page_load()
    
    def wait_for_page_load(self, timeout: Optional[int] = None) -> None:
        """
        Wait for login page to fully load.
        
        Args:
            timeout: Custom timeout in milliseconds
        """
        logger.info("Waiting for login page to load")
        self.wait_for_selector(self.LOGIN_FORM, timeout=timeout)
        logger.info("Login page loaded")
    
    # ============================================================================
    # LOGIN METHODS
    # ============================================================================
    
    def login(
        self,
        username: str,
        password: str,
        remember_me: bool = False,
        use_email: bool = False
    ) -> None:
        """
        Perform login with username/email and password.
        
        Args:
            username: Username or email
            password: Password
            remember_me: Check "Remember me" checkbox
            use_email: Use email field instead of username field
        
        Example:
            >>> login_page.login("user@example.com", "password123")
            >>> login_page.login("testuser", "pass", remember_me=True)
        """
        logger.info(f"Logging in with username: {username}")
        
        # Fill username/email
        if use_email and self.is_visible(self.EMAIL_INPUT):
            self.fill_email(username)
        else:
            self.fill_username(username)
        
        # Fill password
        self.fill_password(password)
        
        # Check remember me if requested
        if remember_me:
            self.check_remember_me()
        
        # Click login button
        self.click_login_button()
        
        logger.info("Login form submitted")
    
    def fill_username(self, username: str) -> None:
        """
        Fill the username field.
        
        Args:
            username: Username to fill
        """
        logger.debug(f"Filling username: {username}")
        self.fill(self.USERNAME_INPUT, username)
    
    def fill_email(self, email: str) -> None:
        """
        Fill the email field.
        
        Args:
            email: Email to fill
        """
        logger.debug(f"Filling email: {email}")
        self.fill(self.EMAIL_INPUT, email)
    
    def fill_password(self, password: str) -> None:
        """
        Fill the password field.
        
        Args:
            password: Password to fill
        """
        logger.debug("Filling password")
        self.fill(self.PASSWORD_INPUT, password)
    
    def click_login_button(self) -> None:
        """
        Click the login button.
        """
        logger.debug("Clicking login button")
        
        # Try primary login button first, fallback to submit button
        if self.is_visible(self.LOGIN_BUTTON):
            self.click(self.LOGIN_BUTTON)
        else:
            self.click(self.SUBMIT_BUTTON)
    
    def check_remember_me(self) -> None:
        """
        Check the "Remember me" checkbox.
        """
        logger.debug("Checking remember me checkbox")
        self.check(self.REMEMBER_ME_CHECKBOX)
    
    def toggle_password_visibility(self) -> None:
        """
        Toggle password visibility (show/hide).
        """
        logger.debug("Toggling password visibility")
        self.click(self.SHOW_PASSWORD_BUTTON)
    
    # ============================================================================
    # SOCIAL LOGIN METHODS
    # ============================================================================
    
    def login_with_google(self) -> None:
        """
        Click Google login button.
        
        Note:
            This only clicks the button. Handling OAuth flow
            requires additional setup in tests.
        """
        logger.info("Clicking Google login button")
        self.click(self.GOOGLE_LOGIN_BUTTON)
    
    def login_with_facebook(self) -> None:
        """
        Click Facebook login button.
        
        Note:
            This only clicks the button. Handling OAuth flow
            requires additional setup in tests.
        """
        logger.info("Clicking Facebook login button")
        self.click(self.FACEBOOK_LOGIN_BUTTON)
    
    # ============================================================================
    # NAVIGATION LINKS
    # ============================================================================
    
    def click_forgot_password(self) -> None:
        """
        Click the "Forgot password" link.
        """
        logger.info("Clicking forgot password link")
        self.click(self.FORGOT_PASSWORD_LINK)
    
    def click_signup(self) -> None:
        """
        Click the "Sign up" link.
        """
        logger.info("Clicking signup link")
        self.click(self.SIGNUP_LINK)
    
    # ============================================================================
    # VALIDATION METHODS
    # ============================================================================
    
    def get_error_message(self) -> str:
        """
        Get the error message text.
        
        Returns:
            str: Error message text
        
        Example:
            >>> error = login_page.get_error_message()
            >>> assert "Invalid credentials" in error
        """
        logger.debug("Getting error message")
        return self.get_text(self.ERROR_MESSAGE)
    
    def get_validation_error(self) -> str:
        """
        Get validation error text (field-level errors).
        
        Returns:
            str: Validation error text
        """
        logger.debug("Getting validation error")
        return self.get_text(self.VALIDATION_ERROR)
    
    def get_success_message(self) -> str:
        """
        Get success message text.
        
        Returns:
            str: Success message text
        """
        logger.debug("Getting success message")
        return self.get_text(self.SUCCESS_MESSAGE)
    
    def has_error_message(self) -> bool:
        """
        Check if error message is displayed.
        
        Returns:
            bool: True if error message is visible
        """
        return self.is_visible(self.ERROR_MESSAGE)
    
    def has_validation_error(self) -> bool:
        """
        Check if validation error is displayed.
        
        Returns:
            bool: True if validation error is visible
        """
        return self.is_visible(self.VALIDATION_ERROR)
    
    def is_login_button_enabled(self) -> bool:
        """
        Check if login button is enabled.
        
        Returns:
            bool: True if login button is enabled
        """
        if self.is_visible(self.LOGIN_BUTTON):
            return self.is_enabled(self.LOGIN_BUTTON)
        return self.is_enabled(self.SUBMIT_BUTTON)
    
    def is_logged_in(self, timeout: int = 5000) -> bool:
        """
        Check if login was successful by checking if login form is gone.
        
        Args:
            timeout: Timeout in milliseconds
        
        Returns:
            bool: True if login form is no longer visible
        
        Note:
            This is a basic check. More robust validation should be done
            in the DashboardPage or by checking for specific elements.
        """
        try:
            self.wait_for_selector(
                self.LOGIN_FORM,
                state="hidden",
                timeout=timeout
            )
            logger.info("Login successful - form hidden")
            return True
        except Exception:
            logger.warning("Login form still visible")
            return False
    
    # ============================================================================
    # UTILITY METHODS
    # ============================================================================
    
    def get_page_title_text(self) -> str:
        """
        Get the page title text.
        
        Returns:
            str: Page title text
        """
        return self.get_text(self.PAGE_TITLE)
    
    def clear_form(self) -> None:
        """
        Clear all form fields.
        """
        logger.info("Clearing login form")
        
        if self.is_visible(self.USERNAME_INPUT):
            self.fill(self.USERNAME_INPUT, "")
        
        if self.is_visible(self.EMAIL_INPUT):
            self.fill(self.EMAIL_INPUT, "")
        
        self.fill(self.PASSWORD_INPUT, "")
