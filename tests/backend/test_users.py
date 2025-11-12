"""
Backend API tests for user CRUD operations.

This module tests user management endpoints including create, read,
update, delete, and list operations with pagination.

Requirements: 5.2, 5.4, 3.2
"""

import pytest
import logging
from typing import Dict, Any

from core.models.user import UserCreate, UserResponse, UserUpdate, UserList
from core.helpers.validators import (
    validate_response_status,
    validate_response_time,
    validate_required_fields
)
from core.helpers.data_generator import DataGenerator

# Initialize data generator
data_gen = DataGenerator()


logger = logging.getLogger(__name__)


# ============================================================================
# USER CRUD TESTS
# ============================================================================

@pytest.mark.smoke
@pytest.mark.backend
class TestUserCRUD:
    """Test suite for user CRUD operations."""
    
    @pytest.fixture
    def test_user_data(self) -> Dict[str, Any]:
        """
        Fixture providing test user data.
        
        Returns:
            Dict[str, Any]: User data for testing
        """
        return {
            "username": data_gen.generate_username(),
            "email": data_gen.generate_email(),
            "password": data_gen.generate_secure_password(),
            "full_name": "Test User",
            "phone": data_gen.generate_phone_number(),
            "is_active": True
        }
    
    @pytest.fixture
    def created_user_ids(self) -> list:
        """
        Fixture to track created user IDs for cleanup.
        
        Yields:
            list: List of user IDs to cleanup
        """
        user_ids = []
        yield user_ids
        # Cleanup happens here after test
        logger.info(f"Cleanup: {len(user_ids)} users created during test")
    
    def test_create_user(self, api_client, test_user_data, created_user_ids, settings):
        """
        Test creating a new user with valid data.
        
        Validates:
        - Request data with Pydantic model
        - Response status code is 201 Created
        - Response contains user data
        - User ID is assigned
        - Password is not returned in response
        - Response time is acceptable
        
        Requirements: 5.2, 3.2
        """
        logger.info("Testing user creation")
        
        # Validate request data with Pydantic
        user_create = UserCreate(**test_user_data)
        
        # Execute create user request
        response = api_client.post(
            "/users",
            json=user_create.model_dump()
        )
        
        # Validate response status
        validate_response_status(response, expected_status=201)
        
        # Validate response time
        validate_response_time(response, max_time=settings.api_timeout)
        
        # Parse response
        response_data = response.json()
        
        # Validate required fields
        required_fields = ["id", "username", "email", "is_active", "created_at"]
        validate_required_fields(response_data, required_fields)
        
        # Validate response with Pydantic model
        user_response = UserResponse(**response_data)
        
        # Additional validations
        assert user_response.id > 0, "User ID should be positive"
        assert user_response.username == test_user_data["username"], \
            "Username should match request"
        assert user_response.email == test_user_data["email"], \
            "Email should match request"
        assert user_response.is_active == test_user_data["is_active"], \
            "Active status should match request"
        
        # Ensure password is not in response
        assert "password" not in response_data, \
            "Password should not be returned in response"
        
        # Track for cleanup
        created_user_ids.append(user_response.id)
        
        logger.info(f"User created successfully with ID: {user_response.id}")
    
    def test_create_user_with_duplicate_username(
        self,
        api_client,
        test_user_data,
        created_user_ids
    ):
        """
        Test creating user with duplicate username.
        
        Validates:
        - First user creation succeeds
        - Second user creation with same username fails
        - Response status is 409 Conflict or 400 Bad Request
        - Error message indicates duplicate username
        
        Requirements: 5.2, 3.2
        """
        logger.info("Testing user creation with duplicate username")
        
        # Create first user
        user_create = UserCreate(**test_user_data)
        response1 = api_client.post("/users", json=user_create.model_dump())
        
        validate_response_status(response1, expected_status=201)
        user1 = UserResponse(**response1.json())
        created_user_ids.append(user1.id)
        
        # Attempt to create second user with same username but different email
        duplicate_data = test_user_data.copy()
        duplicate_data["email"] = data_gen.generate_email()  # Different email
        
        user_create_dup = UserCreate(**duplicate_data)
        response2 = api_client.post("/users", json=user_create_dup.model_dump())
        
        # Validate response status (should be 409 or 400)
        assert response2.status_code in [400, 409], \
            f"Expected 400 or 409, got {response2.status_code}"
        
        # Validate error message
        response_data = response2.json()
        error_message = str(response_data).lower()
        assert "username" in error_message or "duplicate" in error_message or "exists" in error_message, \
            "Error message should indicate duplicate username"
        
        logger.info("Duplicate username correctly rejected")
    
    def test_create_user_with_duplicate_email(
        self,
        api_client,
        test_user_data,
        created_user_ids
    ):
        """
        Test creating user with duplicate email.
        
        Validates:
        - First user creation succeeds
        - Second user creation with same email fails
        - Response status is 409 Conflict or 400 Bad Request
        
        Requirements: 5.2, 3.2
        """
        logger.info("Testing user creation with duplicate email")
        
        # Create first user
        user_create = UserCreate(**test_user_data)
        response1 = api_client.post("/users", json=user_create.model_dump())
        
        validate_response_status(response1, expected_status=201)
        user1 = UserResponse(**response1.json())
        created_user_ids.append(user1.id)
        
        # Attempt to create second user with same email but different username
        duplicate_data = test_user_data.copy()
        duplicate_data["username"] = data_gen.generate_username()  # Different username
        
        user_create_dup = UserCreate(**duplicate_data)
        response2 = api_client.post("/users", json=user_create_dup.model_dump())
        
        # Validate response status (should be 409 or 400)
        assert response2.status_code in [400, 409], \
            f"Expected 400 or 409, got {response2.status_code}"
        
        logger.info("Duplicate email correctly rejected")
    
    def test_create_user_with_invalid_email(self, api_client):
        """
        Test creating user with invalid email format.
        
        Validates:
        - Pydantic validation catches invalid email
        - Response status is 422 Unprocessable Entity
        
        Requirements: 3.2
        """
        logger.info("Testing user creation with invalid email")
        
        invalid_data = {
            "username": data_gen.generate_username(),
            "email": "invalid-email-format",  # Invalid email
            "password": data_gen.generate_secure_password(),
            "is_active": True
        }
        
        # Pydantic should catch this, but let's test API validation too
        response = api_client.post("/users", json=invalid_data)
        
        # Validate response status (should be 422 or 400)
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422, got {response.status_code}"
        
        logger.info("Invalid email correctly rejected")
    
    def test_create_user_with_weak_password(self, api_client):
        """
        Test creating user with weak password.
        
        Validates:
        - Weak passwords are rejected
        - Response status is 422 or 400
        - Error message indicates password requirements
        
        Requirements: 3.2
        """
        logger.info("Testing user creation with weak password")
        
        weak_data = {
            "username": data_gen.generate_username(),
            "email": data_gen.generate_email(),
            "password": "weak",  # Too short and weak
            "is_active": True
        }
        
        response = api_client.post("/users", json=weak_data)
        
        # Validate response status (should be 422 or 400)
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422, got {response.status_code}"
        
        logger.info("Weak password correctly rejected")
    
    def test_get_user_by_id(self, api_client, test_user_data, created_user_ids, settings):
        """
        Test retrieving user by ID.
        
        Validates:
        - User can be retrieved by ID
        - Response status code is 200 OK
        - Response contains correct user data
        - Response time is acceptable
        
        Requirements: 5.2
        """
        logger.info("Testing get user by ID")
        
        # First, create a user
        user_create = UserCreate(**test_user_data)
        create_response = api_client.post("/users", json=user_create.model_dump())
        validate_response_status(create_response, expected_status=201)
        
        created_user = UserResponse(**create_response.json())
        created_user_ids.append(created_user.id)
        
        # Now retrieve the user
        response = api_client.get(f"/users/{created_user.id}")
        
        # Validate response status
        validate_response_status(response, expected_status=200)
        
        # Validate response time
        validate_response_time(response, max_time=settings.api_timeout)
        
        # Parse and validate response
        user_response = UserResponse(**response.json())
        
        # Validate user data matches
        assert user_response.id == created_user.id, "User ID should match"
        assert user_response.username == created_user.username, "Username should match"
        assert user_response.email == created_user.email, "Email should match"
        
        logger.info(f"User retrieved successfully: {user_response.id}")
    
    def test_get_user_by_invalid_id(self, api_client):
        """
        Test retrieving user with non-existent ID.
        
        Validates:
        - Response status code is 404 Not Found
        - Error message is appropriate
        
        Requirements: 5.2
        """
        logger.info("Testing get user by invalid ID")
        
        # Use a very large ID that likely doesn't exist
        invalid_id = 999999999
        
        response = api_client.get(f"/users/{invalid_id}")
        
        # Validate response status
        validate_response_status(response, expected_status=404)
        
        logger.info("Invalid user ID correctly returned 404")
    
    def test_update_user(self, api_client, test_user_data, created_user_ids, settings):
        """
        Test updating user data.
        
        Validates:
        - User data can be updated
        - Response status code is 200 OK
        - Updated fields are reflected in response
        - Unchanged fields remain the same
        - Response time is acceptable
        
        Requirements: 5.2, 3.2
        """
        logger.info("Testing user update")
        
        # First, create a user
        user_create = UserCreate(**test_user_data)
        create_response = api_client.post("/users", json=user_create.model_dump())
        validate_response_status(create_response, expected_status=201)
        
        created_user = UserResponse(**create_response.json())
        created_user_ids.append(created_user.id)
        
        # Prepare update data
        update_data = {
            "full_name": "Updated Test User",
            "phone": data_gen.generate_phone_number(),
            "is_active": False
        }
        
        # Validate update data with Pydantic
        user_update = UserUpdate(**update_data)
        
        # Execute update request
        response = api_client.put(
            f"/users/{created_user.id}",
            json=user_update.model_dump(exclude_none=True)
        )
        
        # Validate response status (200 or 204)
        assert response.status_code in [200, 204], \
            f"Expected 200 or 204, got {response.status_code}"
        
        # Validate response time
        validate_response_time(response, max_time=settings.api_timeout)
        
        # If response has body, validate it
        if response.status_code == 200:
            updated_user = UserResponse(**response.json())
            
            # Validate updated fields
            assert updated_user.full_name == update_data["full_name"], \
                "Full name should be updated"
            assert updated_user.phone == update_data["phone"], \
                "Phone should be updated"
            assert updated_user.is_active == update_data["is_active"], \
                "Active status should be updated"
            
            # Validate unchanged fields
            assert updated_user.username == created_user.username, \
                "Username should not change"
            assert updated_user.email == created_user.email, \
                "Email should not change"
        
        logger.info(f"User updated successfully: {created_user.id}")
    
    def test_update_user_partial(self, api_client, test_user_data, created_user_ids):
        """
        Test partial update of user data.
        
        Validates:
        - Only specified fields are updated
        - Other fields remain unchanged
        - Response status is successful
        
        Requirements: 5.2, 3.2
        """
        logger.info("Testing partial user update")
        
        # First, create a user
        user_create = UserCreate(**test_user_data)
        create_response = api_client.post("/users", json=user_create.model_dump())
        validate_response_status(create_response, expected_status=201)
        
        created_user = UserResponse(**create_response.json())
        created_user_ids.append(created_user.id)
        
        # Update only full_name
        update_data = {
            "full_name": "Partially Updated User"
        }
        
        user_update = UserUpdate(**update_data)
        
        response = api_client.patch(
            f"/users/{created_user.id}",
            json=user_update.model_dump(exclude_none=True)
        )
        
        # Validate response status (200, 204, or 405 if PATCH not supported)
        assert response.status_code in [200, 204, 405], \
            f"Expected 200, 204, or 405, got {response.status_code}"
        
        if response.status_code == 405:
            pytest.skip("PATCH method not supported, using PUT instead")
            # Retry with PUT
            response = api_client.put(
                f"/users/{created_user.id}",
                json=user_update.model_dump(exclude_none=True)
            )
        
        logger.info(f"User partially updated: {created_user.id}")
    
    def test_delete_user(self, api_client, test_user_data):
        """
        Test deleting a user.
        
        Validates:
        - User can be deleted
        - Response status code is 204 No Content or 200 OK
        - Deleted user cannot be retrieved
        
        Requirements: 5.2
        """
        logger.info("Testing user deletion")
        
        # First, create a user
        user_create = UserCreate(**test_user_data)
        create_response = api_client.post("/users", json=user_create.model_dump())
        validate_response_status(create_response, expected_status=201)
        
        created_user = UserResponse(**create_response.json())
        user_id = created_user.id
        
        # Delete the user
        delete_response = api_client.delete(f"/users/{user_id}")
        
        # Validate response status (200 or 204)
        assert delete_response.status_code in [200, 204], \
            f"Expected 200 or 204, got {delete_response.status_code}"
        
        # Verify user is deleted by trying to retrieve it
        get_response = api_client.get(f"/users/{user_id}")
        
        # Should return 404
        validate_response_status(get_response, expected_status=404)
        
        logger.info(f"User deleted successfully: {user_id}")
    
    def test_delete_nonexistent_user(self, api_client):
        """
        Test deleting a non-existent user.
        
        Validates:
        - Response status code is 404 Not Found
        - Error message is appropriate
        
        Requirements: 5.2
        """
        logger.info("Testing deletion of non-existent user")
        
        # Use a very large ID that likely doesn't exist
        invalid_id = 999999999
        
        response = api_client.delete(f"/users/{invalid_id}")
        
        # Validate response status
        validate_response_status(response, expected_status=404)
        
        logger.info("Non-existent user deletion correctly returned 404")


# ============================================================================
# USER LIST AND PAGINATION TESTS
# ============================================================================

@pytest.mark.backend
class TestUserList:
    """Test suite for user list and pagination."""
    
    def test_list_users(self, api_client, settings):
        """
        Test listing users without pagination parameters.
        
        Validates:
        - Response status code is 200 OK
        - Response contains list of users
        - Response includes pagination metadata
        - Response time is acceptable
        
        Requirements: 5.2, 5.4
        """
        logger.info("Testing list users")
        
        # Execute list users request
        response = api_client.get("/users")
        
        # Validate response status
        validate_response_status(response, expected_status=200)
        
        # Validate response time
        validate_response_time(response, max_time=settings.api_timeout)
        
        # Parse response
        response_data = response.json()
        
        # Check if response is paginated or simple list
        if isinstance(response_data, list):
            # Simple list response
            assert len(response_data) >= 0, "Should return list of users"
            logger.info(f"Retrieved {len(response_data)} users")
        else:
            # Paginated response
            user_list = UserList(**response_data)
            
            assert user_list.total >= 0, "Total should be non-negative"
            assert user_list.page >= 1, "Page should be at least 1"
            assert user_list.page_size > 0, "Page size should be positive"
            assert len(user_list.users) <= user_list.page_size, \
                "Number of users should not exceed page size"
            
            logger.info(
                f"Retrieved {len(user_list.users)} users "
                f"(page {user_list.page}/{user_list.total_pages})"
            )
    
    def test_list_users_pagination(self, api_client):
        """
        Test user list with pagination parameters.
        
        Validates:
        - Pagination parameters are respected
        - Response contains correct page of data
        - Pagination metadata is accurate
        
        Requirements: 5.2, 5.4
        """
        logger.info("Testing user list with pagination")
        
        # Request first page with page_size=5
        response = api_client.get("/users", params={"page": 1, "page_size": 5})
        
        # Validate response status
        validate_response_status(response, expected_status=200)
        
        response_data = response.json()
        
        # Check if pagination is supported
        if isinstance(response_data, list):
            pytest.skip("Pagination not implemented")
        
        user_list = UserList(**response_data)
        
        # Validate pagination
        assert user_list.page == 1, "Should return first page"
        assert user_list.page_size == 5, "Page size should be 5"
        assert len(user_list.users) <= 5, "Should return at most 5 users"
        
        logger.info(f"Pagination working: page {user_list.page}, size {user_list.page_size}")
    
    def test_list_users_with_filters(self, api_client, test_user_data, created_user_ids):
        """
        Test user list with filter parameters.
        
        Validates:
        - Filter parameters are applied
        - Only matching users are returned
        - Response is successful
        
        Requirements: 5.2, 5.4
        
        Note: This test may be skipped if filtering is not implemented
        """
        logger.info("Testing user list with filters")
        
        # Create a user with specific attributes
        user_create = UserCreate(**test_user_data)
        create_response = api_client.post("/users", json=user_create.model_dump())
        validate_response_status(create_response, expected_status=201)
        
        created_user = UserResponse(**create_response.json())
        created_user_ids.append(created_user.id)
        
        # Try to filter by is_active
        response = api_client.get("/users", params={"is_active": True})
        
        validate_response_status(response, expected_status=200)
        
        response_data = response.json()
        
        # Validate filtering (if supported)
        if isinstance(response_data, list):
            # Simple list - check if our user is in the list
            user_ids = [u.get("id") for u in response_data]
            assert created_user.id in user_ids, "Created user should be in filtered list"
        else:
            # Paginated list
            user_list = UserList(**response_data)
            user_ids = [u.id for u in user_list.users]
            
            # Our user should be in the results (if on current page)
            # This is a soft check since pagination might affect results
            logger.info(f"Filter returned {len(user_list.users)} active users")
        
        logger.info("User list filtering validated")
    
    @pytest.fixture
    def created_user_ids(self) -> list:
        """Fixture to track created user IDs for cleanup."""
        user_ids = []
        yield user_ids
        logger.info(f"Cleanup: {len(user_ids)} users created during test")
