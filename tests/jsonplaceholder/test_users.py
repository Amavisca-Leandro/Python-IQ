"""
Tests for JSONPlaceholder Users API endpoints.

This module contains tests for all users-related endpoints including:
- GET /users - List all users
- GET /users/{id} - Get specific user
- POST /users - Create new user
- PUT /users/{id} - Update user
- DELETE /users/{id} - Delete user

Requirements covered:
- 1.3, 1.4: GET operations for users
- 2.4: POST operations for users
- 3.5: PUT operations for users
- 4.3: DELETE operations for users
- 5.1, 5.3, 5.5: Schema and field validation
"""

import pytest
from core.helpers.validators import (
    validate_response_status,
    validate_json_schema,
    validate_required_fields,
    validate_field_types
)
from core.clients.jsonplaceholder_schemas import USER_SCHEMA
from tests.jsonplaceholder.conftest import validate_email_format


# ============================================================================
# GET TESTS
# ============================================================================

@pytest.mark.smoke
def test_get_users_returns_200_and_exactly_10_users(jsonplaceholder_client):
    """
    Test that GET /users returns status 200 and exactly 10 users.
    
    Requirements: 1.3, 5.1
    """
    response = jsonplaceholder_client.get_users()
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Validate response is a list with exactly 10 users
    users = response.json()
    assert isinstance(users, list), "Response should be a list"
    assert len(users) == 10, f"Expected exactly 10 users, got {len(users)}"


@pytest.mark.smoke
def test_get_user_by_id_returns_specific_user(jsonplaceholder_client):
    """
    Test that GET /users/{id} returns a specific user.
    
    Requirements: 1.4, 5.1
    """
    user_id = 1
    response = jsonplaceholder_client.get_user(user_id)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Validate response structure
    user = response.json()
    assert isinstance(user, dict), "Response should be a dictionary"
    
    # Validate the ID matches
    assert user["id"] == user_id, f"User ID should be {user_id}"


@pytest.mark.validation
def test_get_users_validates_required_fields(jsonplaceholder_client):
    """
    Test that GET /users returns users with required fields (name, email, address).
    
    Requirements: 1.4, 5.3
    """
    response = jsonplaceholder_client.get_users()
    validate_response_status(response, 200)
    
    users = response.json()
    assert len(users) > 0, "Should have at least one user"
    
    # Validate required fields for first user
    user = users[0]
    validate_required_fields(user, ["id", "name", "username", "email", "address"])
    
    # Validate address is an object
    assert isinstance(user["address"], dict), "Address should be a dictionary"


@pytest.mark.validation
def test_get_user_by_id_validates_required_fields(jsonplaceholder_client):
    """
    Test that GET /users/{id} returns user with all required fields.
    
    Requirements: 1.4, 5.3
    """
    response = jsonplaceholder_client.get_user(1)
    validate_response_status(response, 200)
    
    user = response.json()
    
    # Validate required fields
    validate_required_fields(user, ["id", "name", "username", "email", "address"])
    
    # Validate nested address fields
    assert "address" in user, "User should have address field"
    assert isinstance(user["address"], dict), "Address should be a dictionary"


@pytest.mark.validation
def test_get_users_validates_email_format(jsonplaceholder_client):
    """
    Test that GET /users returns users with valid email format using regex.
    
    Requirements: 5.3, 5.5
    """
    response = jsonplaceholder_client.get_users()
    validate_response_status(response, 200)
    
    users = response.json()
    assert len(users) > 0, "Should have at least one user"
    
    # Validate email format for all users
    for user in users:
        assert "email" in user, f"User {user.get('id')} should have email field"
        email = user["email"]
        assert validate_email_format(email), f"Invalid email format: {email}"


@pytest.mark.validation
def test_get_user_by_id_validates_email_format(jsonplaceholder_client):
    """
    Test that GET /users/{id} returns user with valid email format.
    
    Requirements: 5.3, 5.5
    """
    response = jsonplaceholder_client.get_user(1)
    validate_response_status(response, 200)
    
    user = response.json()
    
    # Validate email format
    assert "email" in user, "User should have email field"
    email = user["email"]
    assert validate_email_format(email), f"Invalid email format: {email}"


@pytest.mark.validation
def test_get_users_validates_schema(jsonplaceholder_client):
    """
    Test that GET /users returns users with valid JSON schema.
    
    Requirements: 5.1, 5.5
    """
    response = jsonplaceholder_client.get_users()
    validate_response_status(response, 200)
    
    users = response.json()
    
    # Validate first user against schema
    assert len(users) > 0, "Should have at least one user"
    validate_json_schema(users[0], USER_SCHEMA)


@pytest.mark.validation
def test_get_user_by_id_validates_schema(jsonplaceholder_client):
    """
    Test that GET /users/{id} returns user with valid JSON schema.
    
    Requirements: 5.1, 5.5
    """
    response = jsonplaceholder_client.get_user(1)
    validate_response_status(response, 200)
    
    user = response.json()
    validate_json_schema(user, USER_SCHEMA)


@pytest.mark.validation
def test_get_users_validates_data_types(jsonplaceholder_client):
    """
    Test that GET /users returns users with correct data types.
    
    Requirements: 5.5
    """
    response = jsonplaceholder_client.get_users()
    validate_response_status(response, 200)
    
    users = response.json()
    assert len(users) > 0, "Should have at least one user"
    
    # Validate types for first user
    user = users[0]
    validate_field_types(user, {
        "id": int,
        "name": str,
        "username": str,
        "email": str
    })


def test_get_nonexistent_user_returns_404(jsonplaceholder_client):
    """
    Test that GET /users/{id} with non-existent ID returns 404.
    
    Requirements: 1.4
    """
    nonexistent_id = 99999
    response = jsonplaceholder_client.get_user(nonexistent_id)
    
    # Validate 404 status
    assert response.status_code == 404, f"Expected 404 for non-existent user ID {nonexistent_id}"


# ============================================================================
# CRUD TESTS (POST, PUT, DELETE)
# ============================================================================

@pytest.mark.crud
def test_create_user_with_complete_data_returns_201(jsonplaceholder_client, sample_user_data):
    """
    Test that POST /users with complete data returns 201 and creates user.
    
    Requirements: 2.4
    """
    response = jsonplaceholder_client.create_user(sample_user_data)
    
    # Validate status code
    validate_response_status(response, 201)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Validate response contains created user data
    user = response.json()
    assert isinstance(user, dict), "Response should be a dictionary"
    
    # Validate ID was generated
    assert "id" in user, "Response should contain generated ID"
    assert isinstance(user["id"], int), "ID should be an integer"
    
    # Validate sent data is reflected in response
    assert user["name"] == sample_user_data["name"]
    assert user["username"] == sample_user_data["username"]
    assert user["email"] == sample_user_data["email"]


@pytest.mark.crud
def test_update_user_with_put_returns_200(jsonplaceholder_client, sample_user_data):
    """
    Test that PUT /users/{id} updates user and returns 200.
    
    Requirements: 3.5
    """
    user_id = 1
    response = jsonplaceholder_client.update_user(user_id, sample_user_data)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Validate response contains updated user data
    user = response.json()
    assert isinstance(user, dict), "Response should be a dictionary"
    
    # Validate ID matches
    assert user["id"] == user_id, f"User ID should be {user_id}"
    
    # Validate updated data is reflected in response
    assert user["name"] == sample_user_data["name"]
    assert user["username"] == sample_user_data["username"]
    assert user["email"] == sample_user_data["email"]


@pytest.mark.crud
def test_delete_user_returns_200(jsonplaceholder_client):
    """
    Test that DELETE /users/{id} removes user and returns 200.
    
    Requirements: 4.3
    """
    user_id = 1
    response = jsonplaceholder_client.delete_user(user_id)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Validate response (JSONPlaceholder returns empty object on delete)
    data = response.json()
    assert isinstance(data, dict), "Response should be a dictionary"
