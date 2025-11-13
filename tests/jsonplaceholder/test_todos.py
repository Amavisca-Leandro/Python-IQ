"""
Tests for JSONPlaceholder Todos API endpoints.

This module contains tests for all todos-related endpoints including:
- GET /todos - List all todos
- GET /todos/{id} - Get specific todo
- POST /todos - Create new todo
- PUT /todos/{id} - Update todo (full)

Requirements covered:
- 5.2: Type validation for completed field (boolean)
- 5.5: Schema validation for todos
"""

import pytest
from core.helpers.validators import (
    validate_response_status,
    validate_json_schema,
    validate_required_fields,
    validate_field_types
)
from core.clients.jsonplaceholder_schemas import TODO_SCHEMA


# ============================================================================
# GET TESTS
# ============================================================================

@pytest.mark.smoke
def test_get_todos_returns_200_and_list(jsonplaceholder_client):
    """
    Test that GET /todos returns status 200 and a list of todos.
    
    Requirements: 5.5
    """
    response = jsonplaceholder_client.get_todos()
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Validate response is a list
    todos = response.json()
    assert isinstance(todos, list), "Response should be a list"
    assert len(todos) > 0, "Todos list should not be empty"


@pytest.mark.smoke
@pytest.mark.validation
def test_get_todos_validates_schema(jsonplaceholder_client):
    """
    Test that GET /todos returns todos with valid JSON schema.
    
    Requirements: 5.5
    """
    response = jsonplaceholder_client.get_todos()
    validate_response_status(response, 200)
    
    todos = response.json()
    
    # Validate first todo against schema
    assert len(todos) > 0, "Should have at least one todo"
    validate_json_schema(todos[0], TODO_SCHEMA)


@pytest.mark.validation
def test_get_todos_validates_completed_is_boolean(jsonplaceholder_client):
    """
    Test that GET /todos returns todos with completed field as boolean.
    
    Requirements: 5.2
    """
    response = jsonplaceholder_client.get_todos()
    validate_response_status(response, 200)
    
    todos = response.json()
    assert len(todos) > 0, "Should have at least one todo"
    
    # Validate completed field is boolean for first todo
    todo = todos[0]
    assert "completed" in todo, "Todo should have 'completed' field"
    assert isinstance(todo["completed"], bool), "Completed field should be boolean"


@pytest.mark.smoke
def test_get_todo_by_id_returns_specific_todo(jsonplaceholder_client):
    """
    Test that GET /todos/{id} returns a specific todo with correct fields.
    
    Requirements: 5.5
    """
    todo_id = 1
    response = jsonplaceholder_client.get_todo(todo_id)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Validate response structure
    todo = response.json()
    assert isinstance(todo, dict), "Response should be a dictionary"
    
    # Validate required fields
    validate_required_fields(todo, ["userId", "id", "title", "completed"])
    
    # Validate the ID matches
    assert todo["id"] == todo_id, f"Todo ID should be {todo_id}"


@pytest.mark.validation
def test_get_todo_by_id_validates_schema(jsonplaceholder_client):
    """
    Test that GET /todos/{id} returns todo with valid JSON schema.
    
    Requirements: 5.5
    """
    response = jsonplaceholder_client.get_todo(1)
    validate_response_status(response, 200)
    
    todo = response.json()
    validate_json_schema(todo, TODO_SCHEMA)


@pytest.mark.validation
def test_get_todo_by_id_validates_data_types(jsonplaceholder_client):
    """
    Test that GET /todos/{id} returns todo with correct data types.
    
    Requirements: 5.2, 5.5
    """
    response = jsonplaceholder_client.get_todo(1)
    validate_response_status(response, 200)
    
    todo = response.json()
    validate_field_types(todo, {
        "userId": int,
        "id": int,
        "title": str,
        "completed": bool
    })


# ============================================================================
# POST TESTS
# ============================================================================

@pytest.mark.crud
def test_create_todo_returns_201(jsonplaceholder_client, sample_todo_data):
    """
    Test that POST /todos with valid data returns 201.
    
    Requirements: 5.5
    """
    response = jsonplaceholder_client.create_todo(sample_todo_data)
    
    # Validate status code
    validate_response_status(response, 201)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")


@pytest.mark.crud
def test_create_todo_returns_generated_id(jsonplaceholder_client, sample_todo_data):
    """
    Test that POST /todos returns a generated ID.
    
    Requirements: 5.5
    """
    response = jsonplaceholder_client.create_todo(sample_todo_data)
    validate_response_status(response, 201)
    
    data = response.json()
    
    # Validate ID is present and is an integer
    assert "id" in data, "Response should contain an 'id' field"
    assert isinstance(data["id"], int), "ID should be an integer"
    assert data["id"] > 0, "ID should be a positive integer"


@pytest.mark.crud
@pytest.mark.validation
def test_create_todo_reflects_sent_data(jsonplaceholder_client, sample_todo_data):
    """
    Test that POST /todos reflects the data sent in the response.
    
    Requirements: 5.5
    """
    response = jsonplaceholder_client.create_todo(sample_todo_data)
    validate_response_status(response, 201)
    
    data = response.json()
    
    # Validate that sent data is reflected in response
    assert data["title"] == sample_todo_data["title"], "Title should match sent data"
    assert data["completed"] == sample_todo_data["completed"], "Completed should match sent data"
    assert data["userId"] == sample_todo_data["userId"], "UserId should match sent data"


@pytest.mark.crud
@pytest.mark.validation
def test_create_todo_validates_completed_is_boolean(jsonplaceholder_client, sample_todo_data):
    """
    Test that POST /todos returns todo with completed field as boolean.
    
    Requirements: 5.2
    """
    response = jsonplaceholder_client.create_todo(sample_todo_data)
    validate_response_status(response, 201)
    
    data = response.json()
    
    # Validate completed field is boolean
    assert "completed" in data, "Response should have 'completed' field"
    assert isinstance(data["completed"], bool), "Completed field should be boolean"


# ============================================================================
# PUT TESTS
# ============================================================================

@pytest.mark.crud
def test_update_todo_with_put_returns_200(jsonplaceholder_client, sample_todo_data):
    """
    Test that PUT /todos/{id} with complete data returns 200.
    
    Requirements: 5.5
    """
    todo_id = 1
    response = jsonplaceholder_client.update_todo(todo_id, sample_todo_data)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")


@pytest.mark.crud
@pytest.mark.validation
def test_update_todo_with_put_updates_all_fields(jsonplaceholder_client):
    """
    Test that PUT /todos/{id} updates all fields in the response.
    
    Requirements: 5.5
    """
    todo_id = 1
    updated_data = {
        "userId": 1,
        "title": "Updated Todo via PUT",
        "completed": True
    }
    
    response = jsonplaceholder_client.update_todo(todo_id, updated_data)
    validate_response_status(response, 200)
    
    data = response.json()
    
    # Validate all fields are updated
    assert data["title"] == updated_data["title"], "Title should be updated"
    assert data["completed"] == updated_data["completed"], "Completed should be updated"
    assert data["userId"] == updated_data["userId"], "UserId should be updated"
    assert data["id"] == todo_id, "ID should remain the same"


@pytest.mark.crud
@pytest.mark.validation
def test_update_todo_validates_completed_is_boolean(jsonplaceholder_client):
    """
    Test that PUT /todos/{id} returns todo with completed field as boolean.
    
    Requirements: 5.2
    """
    todo_id = 1
    updated_data = {
        "userId": 1,
        "title": "Updated Todo",
        "completed": True
    }
    
    response = jsonplaceholder_client.update_todo(todo_id, updated_data)
    validate_response_status(response, 200)
    
    data = response.json()
    
    # Validate completed field is boolean
    assert "completed" in data, "Response should have 'completed' field"
    assert isinstance(data["completed"], bool), "Completed field should be boolean"
