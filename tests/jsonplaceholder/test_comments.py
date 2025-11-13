"""
Tests for JSONPlaceholder Comments API endpoints.

This module contains tests for all comments-related endpoints including:
- GET /comments - List all comments
- GET /comments/{id} - Get specific comment
- POST /comments - Create new comment

Requirements covered:
- 5.1, 5.5: Schema and validation
- 6.2: Comments filtering by postId
"""

import pytest
from core.helpers.validators import (
    validate_response_status,
    validate_json_schema,
    validate_required_fields,
    validate_field_types
)
from core.clients.jsonplaceholder_schemas import COMMENT_SCHEMA


# ============================================================================
# GET TESTS
# ============================================================================

@pytest.mark.smoke
def test_get_comments_returns_200_and_list(jsonplaceholder_client):
    """
    Test that GET /comments returns status 200 and a list of comments.
    
    Requirements: 5.1
    """
    response = jsonplaceholder_client.get_comments()
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Validate response is a list
    comments = response.json()
    assert isinstance(comments, list), "Response should be a list"
    assert len(comments) > 0, "Comments list should not be empty"


@pytest.mark.smoke
@pytest.mark.validation
def test_get_comments_validates_schema(jsonplaceholder_client):
    """
    Test that GET /comments returns comments with valid JSON schema.
    
    Requirements: 5.1, 5.5
    """
    response = jsonplaceholder_client.get_comments()
    validate_response_status(response, 200)
    
    comments = response.json()
    
    # Validate first comment against schema
    assert len(comments) > 0, "Should have at least one comment"
    validate_json_schema(comments[0], COMMENT_SCHEMA)


@pytest.mark.validation
def test_get_comments_validates_data_types(jsonplaceholder_client):
    """
    Test that GET /comments returns comments with correct data types.
    
    Requirements: 5.5
    """
    response = jsonplaceholder_client.get_comments()
    validate_response_status(response, 200)
    
    comments = response.json()
    assert len(comments) > 0, "Should have at least one comment"
    
    # Validate types for first comment
    comment = comments[0]
    validate_field_types(comment, {
        "postId": int,
        "id": int,
        "name": str,
        "email": str,
        "body": str
    })


@pytest.mark.smoke
def test_get_comment_by_id_returns_specific_comment(jsonplaceholder_client):
    """
    Test that GET /comments/{id} returns a specific comment with correct fields.
    
    Requirements: 5.1, 5.5
    """
    comment_id = 1
    response = jsonplaceholder_client.get_comment(comment_id)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Validate response structure
    comment = response.json()
    assert isinstance(comment, dict), "Response should be a dictionary"
    
    # Validate required fields
    validate_required_fields(comment, ["postId", "id", "name", "email", "body"])
    
    # Validate the ID matches
    assert comment["id"] == comment_id, f"Comment ID should be {comment_id}"


@pytest.mark.validation
def test_get_comment_by_id_validates_schema(jsonplaceholder_client):
    """
    Test that GET /comments/{id} returns comment with valid JSON schema.
    
    Requirements: 5.1, 5.5
    """
    response = jsonplaceholder_client.get_comment(1)
    validate_response_status(response, 200)
    
    comment = response.json()
    validate_json_schema(comment, COMMENT_SCHEMA)


# ============================================================================
# POST TESTS
# ============================================================================

@pytest.mark.crud
def test_create_comment_returns_201(jsonplaceholder_client, sample_comment_data):
    """
    Test that POST /comments with valid data returns 201.
    
    Requirements: 5.1
    """
    response = jsonplaceholder_client.create_comment(sample_comment_data)
    
    # Validate status code
    validate_response_status(response, 201)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")


@pytest.mark.crud
def test_create_comment_returns_generated_id(jsonplaceholder_client, sample_comment_data):
    """
    Test that POST /comments returns a generated ID.
    
    Requirements: 5.1
    """
    response = jsonplaceholder_client.create_comment(sample_comment_data)
    validate_response_status(response, 201)
    
    data = response.json()
    
    # Validate ID is present and is an integer
    assert "id" in data, "Response should contain an 'id' field"
    assert isinstance(data["id"], int), "ID should be an integer"
    assert data["id"] > 0, "ID should be a positive integer"


@pytest.mark.crud
@pytest.mark.validation
def test_create_comment_reflects_sent_data(jsonplaceholder_client, sample_comment_data):
    """
    Test that POST /comments reflects the data sent in the response.
    
    Requirements: 5.1, 5.5
    """
    response = jsonplaceholder_client.create_comment(sample_comment_data)
    validate_response_status(response, 201)
    
    data = response.json()
    
    # Validate that sent data is reflected in response
    assert data["postId"] == sample_comment_data["postId"], "PostId should match sent data"
    assert data["name"] == sample_comment_data["name"], "Name should match sent data"
    assert data["email"] == sample_comment_data["email"], "Email should match sent data"
    assert data["body"] == sample_comment_data["body"], "Body should match sent data"
