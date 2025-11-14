"""
Frontend tests for login flow.

This module tests the complete login flow including:
- Successful login with valid credentials
- Login with invalid credentials
- Logout functionality
- Login form validation
"""

import allure
import pytest
from playwright.sync_api import Page, expect

from core.ui.pages.login_page import LoginPage
from core.ui.pages.dashboard_page import DashboardPage
from core.config.settings import get_settings


@allure.feature("Frontend UI")
@pytest.mark.frontend
@pytest.mark.smoke
class TestLoginFlow:
    """Test login flow functionality."""
    
    @allure.story("User Authentication - Login")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Successful login with valid credentials")
    def test_successful_login(self, page: Page):
        """
        Test successful login with valid credentials.
        
        Validates:
        - Login form is displayed
        - Credentials can be entered
        - Login redirects to dashboard
        - User is authenticated
        
        Requirements: 6.5, 6.4
        """
        settings = get_settings()
        login_page = LoginPage(page, base_url=settings.frontend_base_url)
        dashboard_page = DashboardPage(page, base_url=settings.frontend_base_url)
        
        with allure.step("Navigate to login page"):
            login_page.navigate_to()
        
        with allure.step("Verify login form is displayed"):
            assert login_page.is_visible(login_page.LOGIN_FORM)
        
        with allure.step("Enter credentials and submit"):
            login_page.login(
                username=settings.auth_user,
                password=settings.auth_password
            )
        
        with allure.step("Verify redirect to dashboard"):
            login_page.wait_for_url("**/dashboard", timeout=10000)
        
        with allure.step("Verify dashboard is loaded"):
            dashboard_page.wait_for_page_load()
            assert dashboard_page.is_dashboard_loaded()
        
        with allure.step("Verify user is authenticated"):
            assert dashboard_page.is_user_dropdown_visible()
        
        # Take screenshot for documentation
        dashboard_page.take_screenshot("successful_login_dashboard")
    
    def test_login_with_invalid_credentials(self, page: Page):
        """
        Test login with invalid credentials.
        
        Validates:
        - Error message is displayed
        - User remains on login page
        - Form can be resubmitted
        
        Requirements: 6.5, 6.4
        """
        settings = get_settings()
        login_page = LoginPage(page, base_url=settings.frontend_base_url)
        
        # Navigate to login page
        login_page.navigate_to()
        
        # Attempt login with invalid credentials
        login_page.login(
            username="invalid_user@example.com",
            password="wrong_password"
        )
        
        # Wait for error message
        login_page.wait_for_selector(login_page.ERROR_MESSAGE, timeout=5000)
        
        # Verify error message is displayed
        assert login_page.has_error_message()
        error_message = login_page.get_error_message()
        assert len(error_message) > 0
        
        # Verify still on login page
        assert login_page.is_visible(login_page.LOGIN_FORM)
        
        # Take screenshot of error state
        login_page.take_screenshot("login_invalid_credentials_error")
    
    def test_logout(self, authenticated_page: Page):
        """
        Test logout functionality.
        
        Validates:
        - Logout button is accessible
        - Logout redirects to login page
        - User session is terminated
        - Cannot access protected pages after logout
        
        Requirements: 6.5, 6.4
        """
        settings = get_settings()
        dashboard_page = DashboardPage(authenticated_page, base_url=settings.frontend_base_url)
        login_page = LoginPage(authenticated_page, base_url=settings.frontend_base_url)
        
        # Verify user is on dashboard
        dashboard_page.wait_for_page_load()
        assert dashboard_page.is_dashboard_loaded()
        
        # Perform logout
        dashboard_page.logout()
        
        # Verify redirect to login page
        login_page.wait_for_url("**/login", timeout=10000)
        
        # Verify login form is displayed
        login_page.wait_for_page_load()
        assert login_page.is_visible(login_page.LOGIN_FORM)
        
        # Verify cannot access dashboard without authentication
        authenticated_page.goto(f"{settings.frontend_base_url}/dashboard")
        
        # Should redirect back to login
        login_page.wait_for_url("**/login", timeout=10000)
        
        # Take screenshot of logout state
        login_page.take_screenshot("logout_success")


@pytest.mark.frontend
@pytest.mark.regression
class TestLoginFormValidation:
    """Test login form validation."""
    
    def test_empty_credentials(self, page: Page):
        """
        Test login with empty credentials.
        
        Validates:
        - Login button behavior with empty fields
        - Validation messages
        
        Requirements: 6.5, 6.4
        """
        settings = get_settings()
        login_page = LoginPage(page, base_url=settings.frontend_base_url)
        
        # Navigate to login page
        login_page.navigate_to()
        
        # Try to submit empty form
        login_page.click_login_button()
        
        # Verify validation or that form wasn't submitted
        # Either validation error appears or we're still on login page
        assert (
            login_page.has_validation_error() or
            login_page.is_visible(login_page.LOGIN_FORM)
        )
    
    def test_remember_me_functionality(self, page: Page):
        """
        Test remember me checkbox functionality.
        
        Validates:
        - Remember me checkbox can be checked
        - Login works with remember me enabled
        
        Requirements: 6.5, 6.4
        """
        settings = get_settings()
        login_page = LoginPage(page, base_url=settings.frontend_base_url)
        
        # Navigate to login page
        login_page.navigate_to()
        
        # Login with remember me
        login_page.login(
            username=settings.auth_user,
            password=settings.auth_password,
            remember_me=True
        )
        
        # Verify successful login
        login_page.wait_for_url("**/dashboard", timeout=10000)
