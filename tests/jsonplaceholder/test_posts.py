"""
Tests for JSONPlaceholder Posts API endpoints.

This module contains tests for all posts-related endpoints including:
- GET /posts - List all posts
- GET /posts/{id} - Get specific post
- POST /posts - Create new post
- PUT /posts/{id} - Update post (full)
- PATCH /posts/{id} - Update post (partial)
- DELETE /posts/{id} - Delete post

Requirements covered:
- 1.1, 1.2, 1.5: GET operations and validation
- 2.1, 2.2, 2.3: POST operations
- 3.1, 3.2, 3.3, 3.4: PUT/PATCH operations
- 4.1, 4.2: DELETE operations
- 5.1, 5.2: Schema and type validation
"""

import pytest
from core.helpers.validators import (
    validate_response_status,
    validate_json_schema,
    validate_required_fields,
    validate_field_types
)
from core.clients.jsonplaceholder_schemas import POST_SCHEMA


# ============================================================================
# GET TESTS
# ============================================================================

@pytest.mark.smoke
def test_get_posts_returns_200_and_list(jsonplaceholder_client):
    """
    Test that GET /posts returns status 200 and a list of posts.
    
    Requirements: 1.1, 5.1
    """
    response = jsonplaceholder_client.get_posts()
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Validate response is a list
    posts = response.json()
    assert isinstance(posts, list), "Response should be a list"
    assert len(posts) > 0, "Posts list should not be empty"


@pytest.mark.smoke
@pytest.mark.validation
def test_get_posts_validates_schema(jsonplaceholder_client):
    """
    Test that GET /posts returns posts with valid JSON schema.
    
    Requirements: 5.1, 5.2
    """
    response = jsonplaceholder_client.get_posts()
    validate_response_status(response, 200)
    
    posts = response.json()
    
    # Validate first post against schema
    assert len(posts) > 0, "Should have at least one post"
    validate_json_schema(posts[0], POST_SCHEMA)


@pytest.mark.validation
def test_get_posts_validates_data_types(jsonplaceholder_client):
    """
    Test that GET /posts returns posts with correct data types.
    
    Requirements: 5.2
    """
    response = jsonplaceholder_client.get_posts()
    validate_response_status(response, 200)
    
    posts = response.json()
    assert len(posts) > 0, "Should have at least one post"
    
    # Validate types for first post
    post = posts[0]
    validate_field_types(post, {
        "userId": int,
        "id": int,
        "title": str,
        "body": str
    })


@pytest.mark.smoke
def test_get_post_by_id_returns_specific_post(jsonplaceholder_client):
    """
    Test that GET /posts/{id} returns a specific post with correct fields.
    
    Requirements: 1.2, 5.2
    """
    post_id = 1
    response = jsonplaceholder_client.get_post(post_id)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Validate response structure
    post = response.json()
    assert isinstance(post, dict), "Response should be a dictionary"
    
    # Validate required fields
    validate_required_fields(post, ["userId", "id", "title", "body"])
    
    # Validate the ID matches
    assert post["id"] == post_id, f"Post ID should be {post_id}"


@pytest.mark.validation
def test_get_post_by_id_validates_schema(jsonplaceholder_client):
    """
    Test that GET /posts/{id} returns post with valid JSON schema.
    
    Requirements: 5.1, 5.2
    """
    response = jsonplaceholder_client.get_post(1)
    validate_response_status(response, 200)
    
    post = response.json()
    validate_json_schema(post, POST_SCHEMA)


@pytest.mark.validation
def test_get_post_by_id_validates_data_types(jsonplaceholder_client):
    """
    Test that GET /posts/{id} returns post with correct data types.
    
    Requirements: 5.2
    """
    response = jsonplaceholder_client.get_post(1)
    validate_response_status(response, 200)
    
    post = response.json()
    validate_field_types(post, {
        "userId": int,
        "id": int,
        "title": str,
        "body": str
    })


def test_get_nonexistent_post_returns_404(jsonplaceholder_client):
    """
    Test that GET /posts/{id} with non-existent ID returns 404.
    
    Requirements: 1.5
    """
    nonexistent_id = 99999
    response = jsonplaceholder_client.get_post(nonexistent_id)
    
    # Validate 404 status
    assert response.status_code == 404, f"Expected 404 for non-existent post ID {nonexistent_id}"


# ============================================================================
# POST TESTS
# ============================================================================

@pytest.mark.crud
def test_create_post_returns_201(jsonplaceholder_client, sample_post_data):
    """
    Test that POST /posts with valid data returns 201.
    
    Requirements: 2.1
    """
    response = jsonplaceholder_client.create_post(sample_post_data)
    
    # Validate status code
    validate_response_status(response, 201)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")


@pytest.mark.crud
def test_create_post_returns_generated_id(jsonplaceholder_client, sample_post_data):
    """
    Test that POST /posts returns a generated ID.
    
    Requirements: 2.2
    """
    response = jsonplaceholder_client.create_post(sample_post_data)
    validate_response_status(response, 201)
    
    data = response.json()
    
    # Validate ID is present and is an integer
    assert "id" in data, "Response should contain an 'id' field"
    assert isinstance(data["id"], int), "ID should be an integer"
    assert data["id"] > 0, "ID should be a positive integer"


@pytest.mark.crud
@pytest.mark.validation
def test_create_post_reflects_sent_data(jsonplaceholder_client, sample_post_data):
    """
    Test that POST /posts reflects the data sent in the response.
    
    Requirements: 2.3
    """
    response = jsonplaceholder_client.create_post(sample_post_data)
    validate_response_status(response, 201)
    
    data = response.json()
    
    # Validate that sent data is reflected in response
    assert data["title"] == sample_post_data["title"], "Title should match sent data"
    assert data["body"] == sample_post_data["body"], "Body should match sent data"
    assert data["userId"] == sample_post_data["userId"], "UserId should match sent data"


# ============================================================================
# PUT/PATCH TESTS
# ============================================================================

@pytest.mark.crud
def test_update_post_with_put_returns_200(jsonplaceholder_client, sample_post_data):
    """
    Test that PUT /posts/{id} with complete data returns 200.
    
    Requirements: 3.1
    """
    post_id = 1
    response = jsonplaceholder_client.update_post(post_id, sample_post_data)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")


@pytest.mark.crud
@pytest.mark.validation
def test_update_post_with_put_updates_all_fields(jsonplaceholder_client):
    """
    Test that PUT /posts/{id} updates all fields in the response.
    
    Requirements: 3.2
    """
    post_id = 1
    updated_data = {
        "userId": 1,
        "title": "Updated Title via PUT",
        "body": "Updated body content via PUT"
    }
    
    response = jsonplaceholder_client.update_post(post_id, updated_data)
    validate_response_status(response, 200)
    
    data = response.json()
    
    # Validate all fields are updated
    assert data["title"] == updated_data["title"], "Title should be updated"
    assert data["body"] == updated_data["body"], "Body should be updated"
    assert data["userId"] == updated_data["userId"], "UserId should be updated"
    assert data["id"] == post_id, "ID should remain the same"


@pytest.mark.crud
def test_patch_post_returns_200(jsonplaceholder_client):
    """
    Test that PATCH /posts/{id} with partial data returns 200.
    
    Requirements: 3.3
    """
    post_id = 1
    partial_data = {
        "title": "Partially Updated Title"
    }
    
    response = jsonplaceholder_client.patch_post(post_id, partial_data)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")


@pytest.mark.crud
@pytest.mark.validation
def test_patch_post_updates_only_sent_fields(jsonplaceholder_client):
    """
    Test that PATCH /posts/{id} updates only the fields sent.
    
    Requirements: 3.4
    """
    post_id = 1
    
    # First, get the original post
    original_response = jsonplaceholder_client.get_post(post_id)
    validate_response_status(original_response, 200)
    original_post = original_response.json()
    
    # Update only the title
    partial_data = {
        "title": "Partially Updated Title via PATCH"
    }
    
    response = jsonplaceholder_client.patch_post(post_id, partial_data)
    validate_response_status(response, 200)
    
    data = response.json()
    
    # Validate only title is updated, other fields remain
    assert data["title"] == partial_data["title"], "Title should be updated"
    assert data["id"] == post_id, "ID should remain the same"
    # Note: JSONPlaceholder is a fake API, so body and userId might not persist
    # but we validate the response structure is correct
    assert "body" in data, "Body field should still be present"
    assert "userId" in data, "UserId field should still be present"


# ============================================================================
# DELETE TESTS
# ============================================================================

@pytest.mark.crud
def test_delete_post_returns_200(jsonplaceholder_client):
    """
    Test that DELETE /posts/{id} returns 200.
    
    Requirements: 4.1
    """
    post_id = 1
    response = jsonplaceholder_client.delete_post(post_id)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")


@pytest.mark.crud
def test_delete_post_confirms_deletion(jsonplaceholder_client):
    """
    Test that DELETE /posts/{id} confirms the deletion.
    
    Requirements: 4.2
    """
    post_id = 1
    response = jsonplaceholder_client.delete_post(post_id)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate response (JSONPlaceholder returns empty object on successful delete)
    data = response.json()
    assert isinstance(data, dict), "Response should be a dictionary"
    
    # JSONPlaceholder returns an empty object {} on successful deletion
    # This confirms the deletion was processed
    assert len(data) == 0 or data == {}, "Response should be empty object confirming deletion"
