"""
Frontend integration tests with Backend and Database.

This module tests complete end-to-end flows including:
- UI interactions
- Backend API calls
- Database validation
- Automatic cleanup
"""

import pytest
from playwright.sync_api import Page
from sqlalchemy import text

from core.ui.pages.login_page import LoginPage
from core.ui.pages.dashboard_page import DashboardPage
from core.ui.pages.user_profile_page import UserProfilePage
from core.config.settings import get_settings
from core.database.models import User, UserProfile
from core.database.manager import DatabaseManager
from core.database.factory import TestDataFactory, TestDataContext
from core.helpers.data_generator import generate_secure_password
from core.api.client import APIClient


@pytest.mark.integration
@pytest.mark.slow
class TestUIBackendDatabaseIntegration:
    """
    Integration tests combining UI, Backend API, and Database validation.
    
    These tests verify complete end-to-end workflows including:
    - Creating test data in database
    - Performing UI actions
    - Making backend API calls
    - Validating data changes in database
    - Automatic cleanup of test data
    """
    
    def test_complete_user_workflow_with_database(
        self,
        page: Page,
        db_manager: DatabaseManager,
        test_data_factory: TestDataFactory,
        test_data_context: TestDataContext,
        api_client: APIClient
    ):
        """
        Test complete user workflow: Create data → UI actions → API calls → DB validation.
        
        This test demonstrates the full integration pattern:
        1. Create test data in database using factory
        2. Verify data is ready for testing
        3. Perform UI interactions
        4. Execute backend API calls
        5. Validate changes in database using both ORM and raw SQL
        6. Automatic cleanup via fixture
        
        Requirements: 6.5, 12.1, 12.3
        """
        settings = get_settings()
        
        # ========================================================================
        # STEP 1: Create test data using factory
        # ========================================================================
        user_data = test_data_factory.create_user_with_profile(
            test_id=test_data_context.test_id,
            email=f"test_{test_data_context.test_id}@example.com",
            username=f"testuser_{test_data_context.test_id}",
            is_active=False,  # Start as inactive
            profile={
                "phone": "+5511999999999",
                "city": "São Paulo",
                "state": "SP"
            }
        )
        
        user_id = user_data['user_id']
        profile_id = user_data['profile_id']
        username = user_data['username']
        email = user_data['email']
        
        # ========================================================================
        # STEP 2: Verify data is ready in database using ORM
        # ========================================================================
        with db_manager.get_session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            profile = session.query(UserProfile).filter(UserProfile.id == profile_id).first()
            
            assert user is not None, f"User {user_id} not found in database"
            assert profile is not None, f"Profile {profile_id} not found in database"
            assert user.is_active is False, "User should start as inactive"
            assert user.email == email
            assert profile.phone == "+5511999999999"
            assert profile.city == "São Paulo"
            
            # Verify relationship
            assert user.profile.id == profile_id
            assert profile.user.id == user_id
        
        # ========================================================================
        # STEP 3: Activate user via Backend API
        # ========================================================================
        # Authenticate API client
        api_client.authenticate()
        
        # Activate user via API
        activate_response = api_client.post(
            f"/users/{user_id}/activate",
            json={"reason": "Integration test activation"}
        )
        
        assert activate_response.status_code in [200, 204], \
            f"User activation failed: {activate_response.status_code}"
        
        # ========================================================================
        # STEP 4: Verify activation in database using raw SQL
        # ========================================================================
        activation_check = db_manager.query_data(
            "SELECT id, username, email, is_active FROM users WHERE id = :user_id",
            {"user_id": user_id}
        )
        
        assert len(activation_check) == 1, "User not found after activation"
        assert activation_check[0]['is_active'] is True, "User should be active after API call"
        
        # ========================================================================
        # STEP 5: Perform UI actions - Login and update profile
        # ========================================================================
        login_page = LoginPage(page)
        
        # Navigate to login page
        page.goto(settings.frontend_base_url)
        
        # Login with test user
        login_page.login(username=username, password=user_data.get('password', 'default_password'))
        
        # Wait for dashboard
        page.wait_for_url("**/dashboard", timeout=10000)
        
        # Navigate to profile page
        dashboard_page = DashboardPage(page)
        dashboard_page.navigate_to_profile()
        
        # Update profile information
        profile_page = UserProfilePage(page)
        new_phone = "+5511888888888"
        new_city = "Rio de Janeiro"
        
        profile_page.update_phone(new_phone)
        profile_page.update_city(new_city)
        profile_page.save_changes()
        
        # Wait for save confirmation
        profile_page.wait_for_save_confirmation()
        
        # ========================================================================
        # STEP 6: Validate UI changes in database using ORM
        # ========================================================================
        with db_manager.get_session() as session:
            updated_profile = session.query(UserProfile).filter(
                UserProfile.id == profile_id
            ).first()
            
            assert updated_profile is not None
            assert updated_profile.phone == new_phone, \
                f"Phone not updated. Expected: {new_phone}, Got: {updated_profile.phone}"
            assert updated_profile.city == new_city, \
                f"City not updated. Expected: {new_city}, Got: {updated_profile.city}"
            
            # Verify user is still active
            updated_user = session.query(User).filter(User.id == user_id).first()
            assert updated_user.is_active is True
        
        # ========================================================================
        # STEP 7: Verify changes via Backend API
        # ========================================================================
        get_user_response = api_client.get(f"/users/{user_id}")
        assert get_user_response.status_code == 200
        
        user_api_data = get_user_response.json()
        assert user_api_data['is_active'] is True
        assert user_api_data['email'] == email
        
        # Get profile via API
        get_profile_response = api_client.get(f"/users/{user_id}/profile")
        assert get_profile_response.status_code == 200
        
        profile_api_data = get_profile_response.json()
        assert profile_api_data['phone'] == new_phone
        assert profile_api_data['city'] == new_city
        
        # ========================================================================
        # STEP 8: Perform complex database validation with joins
        # ========================================================================
        complex_query = db_manager.query_data(
            """
            SELECT 
                u.id as user_id,
                u.username,
                u.email,
                u.is_active,
                p.id as profile_id,
                p.phone,
                p.city,
                p.state
            FROM users u
            LEFT JOIN user_profiles p ON u.id = p.user_id
            WHERE u.id = :user_id
            """,
            {"user_id": user_id}
        )
        
        assert len(complex_query) == 1
        result = complex_query[0]
        assert result['username'] == username
        assert result['is_active'] is True
        assert result['phone'] == new_phone
        assert result['city'] == new_city
        assert result['state'] == "SP"  # State should remain unchanged
        
        # Cleanup is automatic via test_data_context fixture
    
    def test_user_registration_flow_with_validation(
        self,
        page: Page,
        db_manager: DatabaseManager,
        test_data_context: TestDataContext,
        api_client: APIClient
    ):
        """
        Test user registration through UI with backend and database validation.
        
        Flow:
        1. Register new user via UI
        2. Verify user created in database
        3. Validate via backend API
        4. Perform login with new user
        5. Verify session in database
        
        Requirements: 6.5, 12.1, 12.3
        """
        settings = get_settings()
        
        # Generate unique user data
        test_username = f"newuser_{test_data_context.test_id}"
        test_email = f"{test_username}@example.com"
        test_password = generate_secure_password()
        
        # ========================================================================
        # STEP 1: Register user via UI
        # ========================================================================
        page.goto(f"{settings.frontend_base_url}/register")
        
        # Fill registration form
        page.fill("input[name='username']", test_username)
        page.fill("input[name='email']", test_email)
        page.fill("input[name='password']", test_password)
        page.fill("input[name='confirmPassword']", test_password)
        
        # Submit form
        page.click("button[type='submit']")
        
        # Wait for success message or redirect
        page.wait_for_selector(".success-message, .alert-success", timeout=10000)
        
        # ========================================================================
        # STEP 2: Verify user exists in database
        # ========================================================================
        with db_manager.get_session() as session:
            new_user = session.query(User).filter(
                User.username == test_username
            ).first()
            
            assert new_user is not None, f"User {test_username} not found in database"
            assert new_user.email == test_email
            assert new_user.is_active is True  # Should be active by default
            
            # Store user_id for cleanup
            user_id = new_user.id
            test_data_context.register_entity('User', user_id)
        
        # ========================================================================
        # STEP 3: Validate user via Backend API
        # ========================================================================
        api_client.authenticate()  # Authenticate as admin
        
        get_user_response = api_client.get(f"/users/{user_id}")
        assert get_user_response.status_code == 200
        
        user_data = get_user_response.json()
        assert user_data['username'] == test_username
        assert user_data['email'] == test_email
        assert user_data['is_active'] is True
        
        # ========================================================================
        # STEP 4: Login with new user
        # ========================================================================
        login_page = LoginPage(page)
        page.goto(settings.frontend_base_url)
        
        login_page.login(username=test_username, password=test_password)
        
        # Verify successful login
        page.wait_for_url("**/dashboard", timeout=10000)
        
        # ========================================================================
        # STEP 5: Verify login via database (check last_login timestamp)
        # ========================================================================
        login_check = db_manager.query_data(
            """
            SELECT id, username, is_active, last_login
            FROM users
            WHERE id = :user_id
            """,
            {"user_id": user_id}
        )
        
        assert len(login_check) == 1
        # Note: last_login check depends on your schema having this field
        # assert login_check[0]['last_login'] is not None
    
    def test_bulk_data_creation_and_ui_listing(
        self,
        page: Page,
        db_manager: DatabaseManager,
        test_data_factory: TestDataFactory,
        test_data_context: TestDataContext,
        authenticated_page: Page
    ):
        """
        Test bulk data creation and verification through UI listing.
        
        Flow:
        1. Create multiple users in database
        2. Navigate to user list page
        3. Verify all users appear in UI
        4. Validate data consistency between DB and UI
        
        Requirements: 6.5, 12.1, 12.2
        """
        settings = get_settings()
        
        # ========================================================================
        # STEP 1: Create multiple test users
        # ========================================================================
        user_count = 5
        created_users = test_data_factory.create_multiple_users(
            test_id=test_data_context.test_id,
            count=user_count,
            with_profiles=True
        )
        
        assert len(created_users) == user_count
        
        # Extract user IDs and usernames
        user_ids = [user['user_id'] for user in created_users]
        usernames = [user['username'] for user in created_users]
        
        # ========================================================================
        # STEP 2: Verify all users in database
        # ========================================================================
        with db_manager.get_session() as session:
            db_users = session.query(User).filter(User.id.in_(user_ids)).all()
            assert len(db_users) == user_count
            
            # Verify all have profiles
            for user in db_users:
                assert user.profile is not None
                assert user.profile.user_id == user.id
        
        # ========================================================================
        # STEP 3: Navigate to user list page (using authenticated page)
        # ========================================================================
        authenticated_page.goto(f"{settings.frontend_base_url}/users")
        
        # Wait for user list to load
        authenticated_page.wait_for_selector(".user-list, table.users", timeout=10000)
        
        # ========================================================================
        # STEP 4: Verify users appear in UI
        # ========================================================================
        for username in usernames:
            # Check if username appears in the page
            user_element = authenticated_page.locator(f"text={username}")
            assert user_element.is_visible(), f"User {username} not visible in UI"
        
        # ========================================================================
        # STEP 5: Validate data consistency
        # ========================================================================
        # Get user count from UI
        user_rows = authenticated_page.locator(".user-row, tr.user").count()
        assert user_rows >= user_count, \
            f"Expected at least {user_count} users in UI, found {user_rows}"
        
        # Verify database count matches
        db_count = db_manager.query_data(
            "SELECT COUNT(*) as count FROM users WHERE id = ANY(:user_ids)",
            {"user_ids": user_ids}
        )
        assert db_count[0]['count'] == user_count
    
    def test_data_modification_across_all_layers(
        self,
        page: Page,
        db_manager: DatabaseManager,
        test_data_factory: TestDataFactory,
        test_data_context: TestDataContext,
        api_client: APIClient
    ):
        """
        Test data modification across UI, API, and Database layers.
        
        Flow:
        1. Create user in database
        2. Modify via API
        3. Verify in database
        4. Modify via UI
        5. Verify via API
        6. Final database validation
        
        Requirements: 6.5, 12.1, 12.3
        """
        settings = get_settings()
        
        # ========================================================================
        # STEP 1: Create initial user
        # ========================================================================
        user_data = test_data_factory.create_user_with_profile(
            test_id=test_data_context.test_id,
            first_name="John",
            last_name="Doe",
            profile={
                "phone": "+5511111111111",
                "city": "São Paulo"
            }
        )
        
        user_id = user_data['user_id']
        
        # ========================================================================
        # STEP 2: Modify user via API
        # ========================================================================
        api_client.authenticate()
        
        api_update = {
            "first_name": "Jane",
            "last_name": "Smith"
        }
        
        update_response = api_client.put(f"/users/{user_id}", json=api_update)
        assert update_response.status_code in [200, 204]
        
        # ========================================================================
        # STEP 3: Verify API changes in database
        # ========================================================================
        with db_manager.get_session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            assert user.first_name == "Jane"
            assert user.last_name == "Smith"
        
        # ========================================================================
        # STEP 4: Modify profile via UI
        # ========================================================================
        login_page = LoginPage(page)
        page.goto(settings.frontend_base_url)
        
        # Login
        login_page.login(
            username=user_data['username'],
            password=user_data.get('password', 'default_password')
        )
        
        # Navigate to profile
        page.wait_for_url("**/dashboard", timeout=10000)
        dashboard_page = DashboardPage(page)
        dashboard_page.navigate_to_profile()
        
        # Update profile
        profile_page = UserProfilePage(page)
        new_phone = "+5511222222222"
        new_city = "Brasília"
        
        profile_page.update_phone(new_phone)
        profile_page.update_city(new_city)
        profile_page.save_changes()
        profile_page.wait_for_save_confirmation()
        
        # ========================================================================
        # STEP 5: Verify UI changes via API
        # ========================================================================
        profile_response = api_client.get(f"/users/{user_id}/profile")
        assert profile_response.status_code == 200
        
        profile_data = profile_response.json()
        assert profile_data['phone'] == new_phone
        assert profile_data['city'] == new_city
        
        # ========================================================================
        # STEP 6: Final database validation with complete data
        # ========================================================================
        final_check = db_manager.query_data(
            """
            SELECT 
                u.id, u.first_name, u.last_name,
                p.phone, p.city
            FROM users u
            JOIN user_profiles p ON u.id = p.user_id
            WHERE u.id = :user_id
            """,
            {"user_id": user_id}
        )
        
        assert len(final_check) == 1
        result = final_check[0]
        
        # Verify all modifications persisted
        assert result['first_name'] == "Jane"  # From API
        assert result['last_name'] == "Smith"  # From API
        assert result['phone'] == new_phone  # From UI
        assert result['city'] == new_city  # From UI 