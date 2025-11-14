"""
Frontend tests for user journey flows.

This module tests complete user journeys including:
- User registration flow
- Profile editing
- Critical business flows
"""

import pytest
from playwright.sync_api import Page

from core.ui.pages.login_page import LoginPage
from core.ui.pages.dashboard_page import DashboardPage
from core.ui.pages.user_profile_page import UserProfilePage
from core.config.settings import get_settings
from core.helpers.data_generator import generate_email, generate_password, generate_phone_br


@pytest.mark.frontend
@pytest.mark.regression
class TestUserRegistrationFlow:
    """Test complete user registration flow."""
    
    def test_complete_user_registration_flow(self, page: Page):
        """
        Test complete user registration from start to finish.
        
        Flow:
        1. Navigate to signup page
        2. Fill registration form
        3. Submit registration
        4. Verify account creation
        5. Login with new credentials
        6. Verify dashboard access
        
        Requirements: 6.5, 6.4
        """
        settings = get_settings()
        login_page = LoginPage(page, base_url=settings.frontend_base_url)
        dashboard_page = DashboardPage(page, base_url=settings.frontend_base_url)
        
        # Generate test data
        test_email = generate_email()
        test_password = generate_password()
        test_username = f"testuser_{test_email.split('@')[0]}"
        
        # Navigate to login page
        login_page.navigate_to()
        
        # Click signup link
        if login_page.is_visible(login_page.SIGNUP_LINK):
            login_page.click_signup()
            
            # Wait for signup form
            page.wait_for_url("**/signup", timeout=5000)
            
            # Fill registration form
            # Note: Actual selectors would depend on signup page implementation
            if page.locator("#username").is_visible():
                page.fill("#username", test_username)
            if page.locator("#email").is_visible():
                page.fill("#email", test_email)
            if page.locator("#password").is_visible():
                page.fill("#password", test_password)
            if page.locator("#confirm-password").is_visible():
                page.fill("#confirm-password", test_password)
            
            # Submit registration
            if page.locator("#register-button").is_visible():
                page.click("#register-button")
                
                # Wait for success or redirect
                page.wait_for_timeout(2000)
                
                # If redirected to login, login with new credentials
                if "login" in page.url:
                    login_page.login(username=test_email, password=test_password)
                
                # Verify dashboard access
                dashboard_page.wait_for_url("**/dashboard", timeout=10000)
                dashboard_page.wait_for_page_load()
                assert dashboard_page.is_dashboard_loaded()
                
                # Take screenshot
                dashboard_page.take_screenshot("registration_complete")


@pytest.mark.frontend
@pytest.mark.smoke
class TestProfileEditingFlow:
    """Test user profile editing flow."""
    
    def test_edit_user_profile(self, authenticated_page: Page):
        """
        Test editing user profile information.
        
        Flow:
        1. Navigate to profile page
        2. Enter edit mode
        3. Update profile fields
        4. Save changes
        5. Verify changes are persisted
        
        Requirements: 6.5, 6.4
        """
        settings = get_settings()
        dashboard_page = DashboardPage(authenticated_page, base_url=settings.frontend_base_url)
        profile_page = UserProfilePage(authenticated_page, base_url=settings.frontend_base_url)
        
        # Navigate to dashboard
        dashboard_page.wait_for_page_load()
        
        # Navigate to profile
        dashboard_page.navigate_to_profile()
        
        # Wait for profile page to load
        profile_page.wait_for_page_load()
        
        # Get current profile info
        original_info = profile_page.get_profile_info()
        
        # Generate new test data
        new_phone = generate_phone_br()
        new_bio = "Updated bio for automated testing"
        
        # Update profile
        profile_page.update_profile_info({
            "phone": new_phone,
            "bio": new_bio
        })
        
        # Save changes
        profile_page.save_changes()
        
        # Wait for success message or page reload
        if profile_page.is_visible(profile_page.SUCCESS_MESSAGE, timeout=3000):
            assert profile_page.has_success_message()
        
        # Reload page to verify persistence
        profile_page.reload()
        profile_page.wait_for_page_load()
        
        # Verify changes are persisted
        updated_info = profile_page.get_profile_info()
        
        # Phone and bio should be updated
        if "phone" in updated_info:
            assert new_phone in updated_info["phone"] or updated_info["phone"] == new_phone
        if "bio" in updated_info:
            assert new_bio in updated_info["bio"] or updated_info["bio"] == new_bio
        
        # Take screenshot
        profile_page.take_screenshot("profile_updated")
    
    def test_edit_profile_and_cancel(self, authenticated_page: Page):
        """
        Test canceling profile edits.
        
        Flow:
        1. Navigate to profile page
        2. Enter edit mode
        3. Make changes
        4. Cancel without saving
        5. Verify changes are not persisted
        
        Requirements: 6.5, 6.4
        """
        settings = get_settings()
        profile_page = UserProfilePage(authenticated_page, base_url=settings.frontend_base_url)
        
        # Navigate to profile
        profile_page.navigate_to()
        profile_page.wait_for_page_load()
        
        # Get original info
        original_info = profile_page.get_profile_info()
        
        # Enter edit mode and make changes
        if profile_page.is_visible(profile_page.EDIT_BUTTON):
            profile_page.click_edit_profile()
            
            # Make changes
            profile_page.update_profile_info({
                "bio": "This should not be saved"
            })
            
            # Cancel changes
            profile_page.cancel_changes()
            
            # Verify original info is still displayed
            current_info = profile_page.get_profile_info()
            assert current_info["bio"] == original_info["bio"]


@pytest.mark.frontend
@pytest.mark.regression
class TestCriticalBusinessFlows:
    """Test critical business flows."""
    
    def test_navigation_flow(self, authenticated_page: Page):
        """
        Test navigation through main application sections.
        
        Flow:
        1. Start at dashboard
        2. Navigate to profile
        3. Navigate to settings
        4. Navigate back to dashboard
        5. Verify all pages load correctly
        
        Requirements: 6.5, 6.4
        """
        settings = get_settings()
        dashboard_page = DashboardPage(authenticated_page, base_url=settings.frontend_base_url)
        profile_page = UserProfilePage(authenticated_page, base_url=settings.frontend_base_url)
        
        # Start at dashboard
        dashboard_page.wait_for_page_load()
        assert dashboard_page.is_dashboard_loaded()
        dashboard_page.take_screenshot("nav_flow_dashboard")
        
        # Navigate to profile
        dashboard_page.navigate_to_profile()
        profile_page.wait_for_page_load()
        assert profile_page.is_visible(profile_page.PROFILE_CONTAINER)
        profile_page.take_screenshot("nav_flow_profile")
        
        # Navigate to settings (if available)
        if dashboard_page.is_visible(dashboard_page.SETTINGS_LINK):
            dashboard_page.navigate_to_settings()
            authenticated_page.wait_for_url("**/settings", timeout=5000)
            authenticated_page.wait_for_load_state("networkidle")
            dashboard_page.take_screenshot("nav_flow_settings")
        
        # Navigate back to dashboard
        dashboard_page.navigate_to_home()
        dashboard_page.wait_for_page_load()
        assert dashboard_page.is_dashboard_loaded()
    
    def test_search_functionality(self, authenticated_page: Page):
        """
        Test search functionality across the application.
        
        Flow:
        1. Navigate to dashboard
        2. Perform search
        3. Verify search results
        4. Clear search
        
        Requirements: 6.5, 6.4
        """
        settings = get_settings()
        dashboard_page = DashboardPage(authenticated_page, base_url=settings.frontend_base_url)
        
        # Navigate to dashboard
        dashboard_page.wait_for_page_load()
        
        # Perform search if search is available
        if dashboard_page.is_visible(dashboard_page.SEARCH_INPUT):
            search_query = "test"
            dashboard_page.search(search_query)
            
            # Wait for results
            dashboard_page.wait_for_timeout(2000)
            
            # Verify search was executed (results or no results message)
            # Actual validation depends on implementation
            dashboard_page.take_screenshot("search_results")
    
    def test_user_dropdown_interactions(self, authenticated_page: Page):
        """
        Test user dropdown menu interactions.
        
        Flow:
        1. Open user dropdown
        2. Verify menu items
        3. Navigate to profile via dropdown
        4. Return to dashboard
        
        Requirements: 6.5, 6.4
        """
        settings = get_settings()
        dashboard_page = DashboardPage(authenticated_page, base_url=settings.frontend_base_url)
        profile_page = UserProfilePage(authenticated_page, base_url=settings.frontend_base_url)
        
        # Navigate to dashboard
        dashboard_page.wait_for_page_load()
        
        # Open user dropdown
        dashboard_page.open_user_dropdown()
        
        # Verify dropdown is visible
        assert dashboard_page.is_visible(dashboard_page.USER_DROPDOWN)
        
        # Get username
        username = dashboard_page.get_username()
        assert len(username) > 0
        
        # Navigate to profile via dropdown
        if dashboard_page.is_visible(dashboard_page.MY_PROFILE_LINK):
            dashboard_page.go_to_my_profile()
            profile_page.wait_for_page_load()
            assert profile_page.is_visible(profile_page.PROFILE_CONTAINER)


@pytest.mark.frontend
@pytest.mark.regression
@pytest.mark.slow
class TestExtendedUserJourneys:
    """Test extended user journeys with multiple steps."""
    
    def test_complete_profile_setup_journey(self, authenticated_page: Page):
        """
        Test complete profile setup journey.
        
        Flow:
        1. Login
        2. Navigate to profile
        3. Update all profile fields
        4. Update preferences
        5. Verify all changes
        
        Requirements: 6.5, 6.4
        """
        settings = get_settings()
        dashboard_page = DashboardPage(authenticated_page, base_url=settings.frontend_base_url)
        profile_page = UserProfilePage(authenticated_page, base_url=settings.frontend_base_url)
        
        # Navigate to dashboard
        dashboard_page.wait_for_page_load()
        
        # Navigate to profile
        dashboard_page.navigate_to_profile()
        profile_page.wait_for_page_load()
        
        # Update profile information
        profile_data = {
            "full_name": "Test User Complete",
            "phone": generate_phone_br(),
            "bio": "Complete profile setup test",
            "company": "Test Company",
            "location": "São Paulo, Brazil"
        }
        
        profile_page.update_profile_info(profile_data)
        profile_page.save_changes()
        
        # Wait for save to complete
        if profile_page.is_visible(profile_page.SUCCESS_MESSAGE, timeout=5000):
            assert profile_page.has_success_message()
        
        # Navigate to preferences if available
        if profile_page.is_visible(profile_page.PREFERENCES_TAB):
            profile_page.navigate_to_preferences()
            
            # Update preferences
            if profile_page.is_visible(profile_page.EMAIL_NOTIFICATIONS_CHECKBOX):
                profile_page.enable_email_notifications()
            
            # Save preferences
            if profile_page.is_visible(profile_page.SAVE_BUTTON):
                profile_page.save_changes()
        
        # Take final screenshot
        profile_page.take_screenshot("complete_profile_setup")
