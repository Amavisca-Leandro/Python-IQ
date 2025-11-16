"""
UI-related step definitions for BDD tests with Playwright.

This module provides step definitions for UI interactions using Page Object Model.
It integrates pytest-bdd with Playwright and existing Page Objects to create
readable, maintainable BDD scenarios for frontend testing.

Steps:
- Navigation steps: Navigate to pages, wait for page load
- Form interaction steps: Fill fields, click buttons, check checkboxes
- Validation steps: Verify elements, check visibility, validate redirects
- Authentication steps: Login, logout, session verification
"""

import allure
import logging
from typing import Dict, Any
from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page, expect

from core.ui.pages.login_page import LoginPage
from core.ui.pages.dashboard_page import DashboardPage
from core.ui.pages.user_profile_page import UserProfilePage
from core.config.settings import get_settings

logger = logging.getLogger(__name__)

# Allure feature and story decorators for this module
allure.feature("UI Testing")
allure.story("Frontend User Interface")


# ============================================================================
# NAVIGATION STEPS
# ============================================================================

@given("I am on the login page")
@allure.story("Navigation")
def navigate_to_login_page(bdd_context, page: Page):
    """
    Navigate to the login page.

    Args:
        bdd_context: BDD context for storing page objects
        page: Playwright page fixture

    Example in feature file:
        Given I am on the login page
    """
    with allure.step("Navigate to login page"):
        settings = get_settings()
        login_page = LoginPage(page, base_url=settings.frontend_base_url)
        login_page.navigate_to()

        # Store page object in context for later use
        bdd_context.login_page = login_page
        bdd_context.page = page

        allure.attach(
            login_page.get_current_url(),
            name="Current URL",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info("Navigated to login page")


@given("I am logged in")
@given("I am on the dashboard")
@allure.story("Authentication")
def user_is_logged_in(bdd_context, authenticated_page: Page):
    """
    Ensure user is logged in and on dashboard.

    Uses the authenticated_page fixture which handles login automatically.

    Args:
        bdd_context: BDD context for storing page objects
        authenticated_page: Authenticated Playwright page fixture

    Example in feature file:
        Given I am logged in
        Given I am on the dashboard
    """
    with allure.step("Verify user is logged in"):
        settings = get_settings()
        dashboard_page = DashboardPage(authenticated_page, base_url=settings.frontend_base_url)
        dashboard_page.wait_for_page_load()

        # Store page objects in context
        bdd_context.dashboard_page = dashboard_page
        bdd_context.page = authenticated_page

        # Verify dashboard is loaded
        assert dashboard_page.is_dashboard_loaded(), "Dashboard did not load correctly"

        allure.attach(
            authenticated_page.url,
            name="Dashboard URL",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info("User is logged in and on dashboard")


@when(parsers.parse('I navigate to the "{page_name}" page'))
@allure.story("Navigation")
def navigate_to_page(bdd_context, page_name: str):
    """
    Navigate to a specific page from dashboard.

    Args:
        bdd_context: BDD context containing dashboard_page
        page_name: Name of the page to navigate to (profile, settings, etc.)

    Example in feature file:
        When I navigate to the "profile" page
        When I navigate to the "settings" page
    """
    with allure.step(f"Navigate to {page_name} page"):
        dashboard_page = bdd_context.dashboard_page
        settings = get_settings()

        page_name_lower = page_name.lower()

        if page_name_lower == "profile":
            dashboard_page.navigate_to_profile()
            bdd_context.profile_page = UserProfilePage(
                bdd_context.page,
                base_url=settings.frontend_base_url
            )
            bdd_context.profile_page.wait_for_page_load()
        elif page_name_lower == "settings":
            dashboard_page.navigate_to_settings()
        elif page_name_lower == "home" or page_name_lower == "dashboard":
            dashboard_page.navigate_to_home()
        else:
            raise ValueError(f"Unknown page: {page_name}")

        allure.attach(
            bdd_context.page.url,
            name=f"{page_name} Page URL",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info(f"Navigated to {page_name} page")


# ============================================================================
# FORM INTERACTION STEPS
# ============================================================================

@when(parsers.parse('I fill the "{field}" field with "{value}"'))
@allure.story("Form Interaction")
def fill_field_with_value(bdd_context, field: str, value: str):
    """
    Fill a form field with a value.

    Args:
        bdd_context: BDD context containing current page
        field: Field name (username, password, email, etc.)
        value: Value to fill

    Example in feature file:
        When I fill the "username" field with "testuser"
        When I fill the "email" field with "test@example.com"
    """
    with allure.step(f"Fill '{field}' field with '{value}'"):
        page = bdd_context.page

        field_lower = field.lower()

        # Try to fill based on common field names
        if field_lower in ["username", "user", "login"]:
            selector = "input[name='username'], input#username, input[type='text']"
        elif field_lower in ["password", "senha"]:
            selector = "input[name='password'], input#password, input[type='password']"
        elif field_lower in ["email", "e-mail"]:
            selector = "input[name='email'], input#email, input[type='email']"
        elif field_lower in ["phone", "telefone"]:
            selector = "input[name='phone'], input#phone"
        else:
            # Try generic selector
            selector = f"input[name='{field}'], input#{field}"

        page.fill(selector, value)

        allure.attach(
            f"Field: {field}\nValue: {value}",
            name="Field Input",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info(f"Filled '{field}' field with value")


@when('I fill the login form with valid credentials')
@allure.story("Authentication")
def fill_login_form_valid(bdd_context):
    """
    Fill the login form with valid credentials from settings.

    Args:
        bdd_context: BDD context containing login_page

    Example in feature file:
        When I fill the login form with valid credentials
    """
    with allure.step("Fill login form with valid credentials"):
        settings = get_settings()
        login_page = bdd_context.login_page

        login_page.fill_username(settings.auth_user)
        login_page.fill_password(settings.auth_password)

        allure.attach(
            f"Username: {settings.auth_user}",
            name="Login Credentials",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info("Filled login form with valid credentials")


@when(parsers.parse('I fill the login form with username "{username}" and password "{password}"'))
@allure.story("Authentication")
def fill_login_form_custom(bdd_context, username: str, password: str):
    """
    Fill the login form with custom credentials.

    Args:
        bdd_context: BDD context containing login_page
        username: Username to enter
        password: Password to enter

    Example in feature file:
        When I fill the login form with username "testuser" and password "wrongpass"
    """
    with allure.step(f"Fill login form with username '{username}'"):
        login_page = bdd_context.login_page

        login_page.fill_username(username)
        login_page.fill_password(password)

        allure.attach(
            f"Username: {username}\nPassword: [HIDDEN]",
            name="Login Attempt",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info(f"Filled login form with username: {username}")


@when('I click the login button')
@when('I submit the login form')
@allure.story("Authentication")
def click_login_button(bdd_context):
    """
    Click the login button to submit the form.

    Args:
        bdd_context: BDD context containing login_page

    Example in feature file:
        When I click the login button
        When I submit the login form
    """
    with allure.step("Click login button"):
        login_page = bdd_context.login_page
        login_page.click_login_button()

        logger.info("Clicked login button")


@when(parsers.parse('I click the "{button_name}" button'))
@allure.story("Form Interaction")
def click_button(bdd_context, button_name: str):
    """
    Click a button by name.

    Args:
        bdd_context: BDD context containing page
        button_name: Name of the button to click

    Example in feature file:
        When I click the "Save" button
        When I click the "Cancel" button
    """
    with allure.step(f"Click '{button_name}' button"):
        page = bdd_context.page

        # Try multiple selectors
        button_name_lower = button_name.lower()
        selectors = [
            f"button:has-text('{button_name}')",
            f"button[type='submit']:has-text('{button_name}')",
            f"input[type='submit'][value='{button_name}']",
            f"a:has-text('{button_name}')"
        ]

        for selector in selectors:
            try:
                page.click(selector, timeout=2000)
                logger.info(f"Clicked '{button_name}' button")
                return
            except:
                continue

        raise Exception(f"Button '{button_name}' not found")


@when('I check the remember me checkbox')
@allure.story("Form Interaction")
def check_remember_me(bdd_context):
    """
    Check the remember me checkbox.

    Args:
        bdd_context: BDD context containing login_page

    Example in feature file:
        When I check the remember me checkbox
    """
    with allure.step("Check remember me checkbox"):
        login_page = bdd_context.login_page

        if hasattr(login_page, 'check_remember_me'):
            login_page.check_remember_me()
        else:
            page = bdd_context.page
            page.check("input[type='checkbox'][name='remember'], input#remember")

        logger.info("Checked remember me checkbox")


# ============================================================================
# AUTHENTICATION STEPS
# ============================================================================

@when('I perform login')
@when('I log in')
@allure.story("Authentication")
def perform_login(bdd_context):
    """
    Perform complete login action (fill form + submit).

    Args:
        bdd_context: BDD context containing login_page

    Example in feature file:
        When I perform login
        When I log in
    """
    with allure.step("Perform login"):
        settings = get_settings()
        login_page = bdd_context.login_page

        login_page.login(
            username=settings.auth_user,
            password=settings.auth_password
        )

        logger.info("Performed login")


@when('I logout')
@when('I perform logout')
@allure.story("Authentication")
def perform_logout(bdd_context):
    """
    Perform logout action.

    Args:
        bdd_context: BDD context containing dashboard_page

    Example in feature file:
        When I logout
        When I perform logout
    """
    with allure.step("Perform logout"):
        dashboard_page = bdd_context.dashboard_page
        dashboard_page.logout()

        logger.info("Performed logout")


# ============================================================================
# VALIDATION STEPS
# ============================================================================

@then("I should be redirected to the dashboard")
@then("I should see the dashboard")
@allure.story("Validation")
def verify_dashboard_redirect(bdd_context):
    """
    Verify user was redirected to dashboard.

    Args:
        bdd_context: BDD context containing page

    Example in feature file:
        Then I should be redirected to the dashboard
        Then I should see the dashboard
    """
    with allure.step("Verify redirect to dashboard"):
        page = bdd_context.page
        settings = get_settings()

        # Wait for dashboard URL
        page.wait_for_url("**/dashboard", timeout=10000)

        # Create dashboard page object if not exists
        if not hasattr(bdd_context, 'dashboard_page'):
            bdd_context.dashboard_page = DashboardPage(page, base_url=settings.frontend_base_url)

        dashboard_page = bdd_context.dashboard_page
        dashboard_page.wait_for_page_load()

        # Verify dashboard is loaded
        assert dashboard_page.is_dashboard_loaded(), "Dashboard did not load"

        # Take screenshot
        dashboard_page.take_screenshot("dashboard_loaded")

        allure.attach(
            page.url,
            name="Dashboard URL",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info("Verified redirect to dashboard")


@then("I should be redirected to the login page")
@then("I should see the login page")
@allure.story("Validation")
def verify_login_page_redirect(bdd_context):
    """
    Verify user was redirected to login page.

    Args:
        bdd_context: BDD context containing page

    Example in feature file:
        Then I should be redirected to the login page
        Then I should see the login page
    """
    with allure.step("Verify redirect to login page"):
        page = bdd_context.page
        settings = get_settings()

        # Wait for login URL
        page.wait_for_url("**/login", timeout=10000)

        # Create login page object if not exists
        if not hasattr(bdd_context, 'login_page'):
            bdd_context.login_page = LoginPage(page, base_url=settings.frontend_base_url)

        login_page = bdd_context.login_page
        login_page.wait_for_page_load()

        # Verify login form is visible
        assert login_page.is_visible(login_page.LOGIN_FORM), "Login form not visible"

        allure.attach(
            page.url,
            name="Login Page URL",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info("Verified redirect to login page")


@then("I should see an error message")
@then("an error message should be displayed")
@allure.story("Validation")
def verify_error_message_displayed(bdd_context):
    """
    Verify that an error message is displayed.

    Args:
        bdd_context: BDD context containing login_page or page

    Example in feature file:
        Then I should see an error message
        Then an error message should be displayed
    """
    with allure.step("Verify error message is displayed"):
        login_page = bdd_context.login_page

        # Wait for error message
        login_page.wait_for_selector(login_page.ERROR_MESSAGE, timeout=5000)

        # Verify error message is visible
        assert login_page.has_error_message(), "Error message not displayed"

        # Get error message text
        error_text = login_page.get_error_message()

        allure.attach(
            error_text,
            name="Error Message",
            attachment_type=allure.attachment_type.TEXT
        )

        # Take screenshot
        login_page.take_screenshot("error_message_displayed")

        logger.info(f"Verified error message: {error_text}")


@then(parsers.parse('I should see the element "{element}"'))
@then(parsers.parse('the element "{element}" should be visible'))
@allure.story("Validation")
def verify_element_visible(bdd_context, element: str):
    """
    Verify that a specific element is visible.

    Args:
        bdd_context: BDD context containing page
        element: Element selector or name

    Example in feature file:
        Then I should see the element "user-dropdown"
        Then the element ".success-message" should be visible
    """
    with allure.step(f"Verify element '{element}' is visible"):
        page = bdd_context.page

        # Try as selector first
        try:
            element_locator = page.locator(element)
            expect(element_locator).to_be_visible(timeout=5000)
        except:
            # Try as text content
            element_locator = page.locator(f"text={element}")
            expect(element_locator).to_be_visible(timeout=5000)

        allure.attach(
            element,
            name="Visible Element",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info(f"Verified element '{element}' is visible")


@then("the login form should be visible")
@allure.story("Validation")
def verify_login_form_visible(bdd_context):
    """
    Verify that the login form is visible.

    Args:
        bdd_context: BDD context containing login_page

    Example in feature file:
        Then the login form should be visible
    """
    with allure.step("Verify login form is visible"):
        login_page = bdd_context.login_page

        assert login_page.is_visible(login_page.LOGIN_FORM), "Login form not visible"

        logger.info("Verified login form is visible")


@then("I should be authenticated")
@then("I should be logged in")
@allure.story("Validation")
def verify_user_authenticated(bdd_context):
    """
    Verify that user is authenticated.

    Args:
        bdd_context: BDD context containing dashboard_page

    Example in feature file:
        Then I should be authenticated
        Then I should be logged in
    """
    with allure.step("Verify user is authenticated"):
        dashboard_page = bdd_context.dashboard_page

        # Check for user-specific elements
        assert dashboard_page.is_user_dropdown_visible(), "User dropdown not visible"

        # Get username if possible
        if hasattr(dashboard_page, 'get_username'):
            username = dashboard_page.get_username()
            allure.attach(
                username,
                name="Authenticated User",
                attachment_type=allure.attachment_type.TEXT
            )

        logger.info("Verified user is authenticated")


@then(parsers.parse('the page URL should contain "{url_part}"'))
@allure.story("Validation")
def verify_url_contains(bdd_context, url_part: str):
    """
    Verify that the current URL contains a specific part.

    Args:
        bdd_context: BDD context containing page
        url_part: Part of URL to check for

    Example in feature file:
        Then the page URL should contain "/dashboard"
        Then the page URL should contain "/profile"
    """
    with allure.step(f"Verify URL contains '{url_part}'"):
        page = bdd_context.page
        current_url = page.url

        assert url_part in current_url, \
            f"URL does not contain '{url_part}'. Current URL: {current_url}"

        allure.attach(
            current_url,
            name="Current URL",
            attachment_type=allure.attachment_type.TEXT
        )

        logger.info(f"Verified URL contains: {url_part}")


@then("I should be on the dashboard")
@allure.story("Validation")
def verify_on_dashboard(bdd_context):
    """
    Verify that user is currently on the dashboard.

    Args:
        bdd_context: BDD context containing dashboard_page

    Example in feature file:
        Then I should be on the dashboard
    """
    with allure.step("Verify user is on dashboard"):
        dashboard_page = bdd_context.dashboard_page
        dashboard_page.wait_for_page_load()

        assert dashboard_page.is_dashboard_loaded(), "Not on dashboard"

        logger.info("Verified user is on dashboard")
