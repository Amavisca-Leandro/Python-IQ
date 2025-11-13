"""
Tests for JSONPlaceholder API performance validation.

This module contains performance tests to validate response times
for all API endpoints meet acceptable thresholds.

Performance Thresholds:
- GET requests: < 500ms
- POST/PUT/PATCH requests: < 1000ms
- DELETE requests: < 500ms
- List endpoints: < 1000ms

Requirements covered:
- 7.2: Response time validation
"""

import pytest
from core.helpers.validators import (
    validate_response_status,
    validate_response_time
)


# ============================================================================
# POSTS PERFORMANCE TESTS
# ============================================================================

@pytest.mark.performance
def test_get_posts_performance(jsonplaceholder_client):
    """
    Test that GET /posts responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.get_posts()
    validate_response_status(response, 200)
    validate_response_time(response, 1000)


@pytest.mark.performance
def test_get_post_by_id_performance(jsonplaceholder_client):
    """
    Test that GET /posts/{id} responds within 500ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.get_post(1)
    validate_response_status(response, 200)
    validate_response_time(response, 500)


@pytest.mark.performance
def test_create_post_performance(jsonplaceholder_client, sample_post_data):
    """
    Test that POST /posts responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.create_post(sample_post_data)
    validate_response_status(response, 201)
    validate_response_time(response, 1000)


@pytest.mark.performance
def test_update_post_performance(jsonplaceholder_client, sample_post_data):
    """
    Test that PUT /posts/{id} responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.update_post(1, sample_post_data)
    validate_response_status(response, 200)
    validate_response_time(response, 1000)


@pytest.mark.performance
def test_patch_post_performance(jsonplaceholder_client):
    """
    Test that PATCH /posts/{id} responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    partial_data = {"title": "Performance Test"}
    response = jsonplaceholder_client.patch_post(1, partial_data)
    validate_response_status(response, 200)
    validate_response_time(response, 1000)


@pytest.mark.performance
def test_delete_post_performance(jsonplaceholder_client):
    """
    Test that DELETE /posts/{id} responds within 500ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.delete_post(1)
    validate_response_status(response, 200)
    validate_response_time(response, 500)


# ============================================================================
# USERS PERFORMANCE TESTS
# ============================================================================

@pytest.mark.performance
def test_get_users_performance(jsonplaceholder_client):
    """
    Test that GET /users responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.get_users()
    validate_response_status(response, 200)
    validate_response_time(response, 1000)


@pytest.mark.performance
def test_get_user_by_id_performance(jsonplaceholder_client):
    """
    Test that GET /users/{id} responds within 500ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.get_user(1)
    validate_response_status(response, 200)
    validate_response_time(response, 500)


@pytest.mark.performance
def test_create_user_performance(jsonplaceholder_client, sample_user_data):
    """
    Test that POST /users responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.create_user(sample_user_data)
    validate_response_status(response, 201)
    validate_response_time(response, 1000)


@pytest.mark.performance
def test_update_user_performance(jsonplaceholder_client, sample_user_data):
    """
    Test that PUT /users/{id} responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.update_user(1, sample_user_data)
    validate_response_status(response, 200)
    validate_response_time(response, 1000)


@pytest.mark.performance
def test_delete_user_performance(jsonplaceholder_client):
    """
    Test that DELETE /users/{id} responds within 500ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.delete_user(1)
    validate_response_status(response, 200)
    validate_response_time(response, 500)


# ============================================================================
# COMMENTS PERFORMANCE TESTS
# ============================================================================

@pytest.mark.performance
def test_get_comments_performance(jsonplaceholder_client):
    """
    Test that GET /comments responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.get_comments()
    validate_response_status(response, 200)
    validate_response_time(response, 1000)


@pytest.mark.performance
def test_get_comment_by_id_performance(jsonplaceholder_client):
    """
    Test that GET /comments/{id} responds within 500ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.get_comment(1)
    validate_response_status(response, 200)
    validate_response_time(response, 500)


@pytest.mark.performance
def test_create_comment_performance(jsonplaceholder_client, sample_comment_data):
    """
    Test that POST /comments responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.create_comment(sample_comment_data)
    validate_response_status(response, 201)
    validate_response_time(response, 1000)


# ============================================================================
# TODOS PERFORMANCE TESTS
# ============================================================================

@pytest.mark.performance
def test_get_todos_performance(jsonplaceholder_client):
    """
    Test that GET /todos responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.get_todos()
    validate_response_status(response, 200)
    validate_response_time(response, 1000)


@pytest.mark.performance
def test_get_todo_by_id_performance(jsonplaceholder_client):
    """
    Test that GET /todos/{id} responds within 500ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.get_todo(1)
    validate_response_status(response, 200)
    validate_response_time(response, 500)


@pytest.mark.performance
def test_create_todo_performance(jsonplaceholder_client, sample_todo_data):
    """
    Test that POST /todos responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.create_todo(sample_todo_data)
    validate_response_status(response, 201)
    validate_response_time(response, 1000)


@pytest.mark.performance
def test_update_todo_performance(jsonplaceholder_client, sample_todo_data):
    """
    Test that PUT /todos/{id} responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.update_todo(1, sample_todo_data)
    validate_response_status(response, 200)
    validate_response_time(response, 1000)


# ============================================================================
# ALBUMS PERFORMANCE TESTS
# ============================================================================

@pytest.mark.performance
def test_get_albums_performance(jsonplaceholder_client):
    """
    Test that GET /albums responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.get_albums()
    validate_response_status(response, 200)
    validate_response_time(response, 1000)


@pytest.mark.performance
def test_get_album_by_id_performance(jsonplaceholder_client):
    """
    Test that GET /albums/{id} responds within 500ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.get_album(1)
    validate_response_status(response, 200)
    validate_response_time(response, 500)


# ============================================================================
# FILTER PERFORMANCE TESTS
# ============================================================================

@pytest.mark.performance
@pytest.mark.filters
def test_filter_posts_by_user_performance(jsonplaceholder_client):
    """
    Test that GET /posts?userId=1 responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.get_posts(user_id=1)
    validate_response_status(response, 200)
    validate_response_time(response, 1000)


@pytest.mark.performance
@pytest.mark.filters
def test_filter_comments_by_post_performance(jsonplaceholder_client):
    """
    Test that GET /comments?postId=1 responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.get_comments(post_id=1)
    validate_response_status(response, 200)
    validate_response_time(response, 1000)


@pytest.mark.performance
@pytest.mark.filters
def test_filter_todos_by_user_performance(jsonplaceholder_client):
    """
    Test that GET /todos?userId=1 responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.get_todos(user_id=1)
    validate_response_status(response, 200)
    validate_response_time(response, 1000)


@pytest.mark.performance
@pytest.mark.filters
def test_filter_albums_by_user_performance(jsonplaceholder_client):
    """
    Test that GET /albums?userId=1 responds within 1000ms threshold.
    
    Requirements: 7.2
    """
    response = jsonplaceholder_client.get_albums(user_id=1)
    validate_response_status(response, 200)
    validate_response_time(response, 1000)
