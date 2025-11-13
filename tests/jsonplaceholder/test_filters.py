"""
Tests for JSONPlaceholder API Query Parameters and Filters.

This module contains tests for filtering and query parameter functionality
across different JSONPlaceholder API endpoints including:
- GET /posts?userId={id} - Filter posts by user ID
- GET /comments?postId={id} - Filter comments by post ID
- GET /todos?userId={id} - Filter todos by user ID
- GET /albums?userId={id} - Filter albums by user ID

Requirements covered:
- 6.1: Filter posts by userId
- 6.2: Filter comments by postId
- 6.3: Validate filters are applied correctly
"""

import pytest
from core.helpers.validators import validate_response_status


# ============================================================================
# POSTS FILTER TESTS
# ============================================================================

@pytest.mark.filters
@pytest.mark.smoke
def test_filter_posts_by_user_id(jsonplaceholder_client):
    """
    Test that GET /posts?userId=1 filters posts by user ID.
    
    Validates that:
    - Request returns 200 status
    - All returned posts belong to the specified user
    - At least one post is returned
    
    Requirements: 6.1, 6.3
    """
    user_id = 1
    response = jsonplaceholder_client.get_posts(user_id=user_id)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Get posts and validate filtering
    posts = response.json()
    assert isinstance(posts, list), "Response should be a list"
    assert len(posts) > 0, f"Should return at least one post for userId {user_id}"
    
    # Validate all posts belong to the specified user
    for post in posts:
        assert post["userId"] == user_id, \
            f"Post {post['id']} has userId {post['userId']}, expected {user_id}"


@pytest.mark.filters
def test_filter_posts_by_different_user_ids(jsonplaceholder_client):
    """
    Test filtering posts by multiple different user IDs.
    
    Validates that the filter correctly returns different sets of posts
    for different user IDs.
    
    Requirements: 6.1, 6.3
    """
    # Test with user ID 1
    response_user1 = jsonplaceholder_client.get_posts(user_id=1)
    validate_response_status(response_user1, 200)
    posts_user1 = response_user1.json()
    
    # Test with user ID 2
    response_user2 = jsonplaceholder_client.get_posts(user_id=2)
    validate_response_status(response_user2, 200)
    posts_user2 = response_user2.json()
    
    # Validate both return posts
    assert len(posts_user1) > 0, "User 1 should have posts"
    assert len(posts_user2) > 0, "User 2 should have posts"
    
    # Validate all posts belong to correct users
    assert all(p["userId"] == 1 for p in posts_user1), "All posts should belong to user 1"
    assert all(p["userId"] == 2 for p in posts_user2), "All posts should belong to user 2"
    
    # Validate the post sets are different
    post_ids_user1 = {p["id"] for p in posts_user1}
    post_ids_user2 = {p["id"] for p in posts_user2}
    assert post_ids_user1.isdisjoint(post_ids_user2), \
        "Posts from different users should not overlap"


@pytest.mark.filters
def test_filter_posts_returns_subset_of_all_posts(jsonplaceholder_client):
    """
    Test that filtered posts are a subset of all posts.
    
    Validates that filtering by userId returns fewer posts than
    requesting all posts without a filter.
    
    Requirements: 6.1, 6.3
    """
    # Get all posts
    response_all = jsonplaceholder_client.get_posts()
    validate_response_status(response_all, 200)
    all_posts = response_all.json()
    
    # Get filtered posts
    user_id = 1
    response_filtered = jsonplaceholder_client.get_posts(user_id=user_id)
    validate_response_status(response_filtered, 200)
    filtered_posts = response_filtered.json()
    
    # Validate filtered is subset
    assert len(filtered_posts) < len(all_posts), \
        "Filtered posts should be fewer than all posts"
    assert len(filtered_posts) > 0, "Should have at least one filtered post"
    
    # Validate all filtered posts exist in all posts
    all_post_ids = {p["id"] for p in all_posts}
    for post in filtered_posts:
        assert post["id"] in all_post_ids, \
            f"Filtered post {post['id']} should exist in all posts"


# ============================================================================
# COMMENTS FILTER TESTS
# ============================================================================

@pytest.mark.filters
@pytest.mark.smoke
def test_filter_comments_by_post_id(jsonplaceholder_client):
    """
    Test that GET /comments?postId=1 filters comments by post ID.
    
    Validates that:
    - Request returns 200 status
    - All returned comments belong to the specified post
    - At least one comment is returned
    
    Requirements: 6.2, 6.3
    """
    post_id = 1
    response = jsonplaceholder_client.get_comments(post_id=post_id)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Get comments and validate filtering
    comments = response.json()
    assert isinstance(comments, list), "Response should be a list"
    assert len(comments) > 0, f"Should return at least one comment for postId {post_id}"
    
    # Validate all comments belong to the specified post
    for comment in comments:
        assert comment["postId"] == post_id, \
            f"Comment {comment['id']} has postId {comment['postId']}, expected {post_id}"


@pytest.mark.filters
def test_filter_comments_by_different_post_ids(jsonplaceholder_client):
    """
    Test filtering comments by multiple different post IDs.
    
    Validates that the filter correctly returns different sets of comments
    for different post IDs.
    
    Requirements: 6.2, 6.3
    """
    # Test with post ID 1
    response_post1 = jsonplaceholder_client.get_comments(post_id=1)
    validate_response_status(response_post1, 200)
    comments_post1 = response_post1.json()
    
    # Test with post ID 2
    response_post2 = jsonplaceholder_client.get_comments(post_id=2)
    validate_response_status(response_post2, 200)
    comments_post2 = response_post2.json()
    
    # Validate both return comments
    assert len(comments_post1) > 0, "Post 1 should have comments"
    assert len(comments_post2) > 0, "Post 2 should have comments"
    
    # Validate all comments belong to correct posts
    assert all(c["postId"] == 1 for c in comments_post1), \
        "All comments should belong to post 1"
    assert all(c["postId"] == 2 for c in comments_post2), \
        "All comments should belong to post 2"
    
    # Validate the comment sets are different
    comment_ids_post1 = {c["id"] for c in comments_post1}
    comment_ids_post2 = {c["id"] for c in comments_post2}
    assert comment_ids_post1.isdisjoint(comment_ids_post2), \
        "Comments from different posts should not overlap"


@pytest.mark.filters
def test_filter_comments_returns_subset_of_all_comments(jsonplaceholder_client):
    """
    Test that filtered comments are a subset of all comments.
    
    Validates that filtering by postId returns fewer comments than
    requesting all comments without a filter.
    
    Requirements: 6.2, 6.3
    """
    # Get all comments
    response_all = jsonplaceholder_client.get_comments()
    validate_response_status(response_all, 200)
    all_comments = response_all.json()
    
    # Get filtered comments
    post_id = 1
    response_filtered = jsonplaceholder_client.get_comments(post_id=post_id)
    validate_response_status(response_filtered, 200)
    filtered_comments = response_filtered.json()
    
    # Validate filtered is subset
    assert len(filtered_comments) < len(all_comments), \
        "Filtered comments should be fewer than all comments"
    assert len(filtered_comments) > 0, "Should have at least one filtered comment"
    
    # Validate all filtered comments exist in all comments
    all_comment_ids = {c["id"] for c in all_comments}
    for comment in filtered_comments:
        assert comment["id"] in all_comment_ids, \
            f"Filtered comment {comment['id']} should exist in all comments"


# ============================================================================
# TODOS FILTER TESTS
# ============================================================================

@pytest.mark.filters
@pytest.mark.smoke
def test_filter_todos_by_user_id(jsonplaceholder_client):
    """
    Test that GET /todos?userId=1 filters todos by user ID.
    
    Validates that:
    - Request returns 200 status
    - All returned todos belong to the specified user
    - At least one todo is returned
    
    Requirements: 6.1, 6.3
    """
    user_id = 1
    response = jsonplaceholder_client.get_todos(user_id=user_id)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Get todos and validate filtering
    todos = response.json()
    assert isinstance(todos, list), "Response should be a list"
    assert len(todos) > 0, f"Should return at least one todo for userId {user_id}"
    
    # Validate all todos belong to the specified user
    for todo in todos:
        assert todo["userId"] == user_id, \
            f"Todo {todo['id']} has userId {todo['userId']}, expected {user_id}"


@pytest.mark.filters
def test_filter_todos_by_different_user_ids(jsonplaceholder_client):
    """
    Test filtering todos by multiple different user IDs.
    
    Validates that the filter correctly returns different sets of todos
    for different user IDs.
    
    Requirements: 6.1, 6.3
    """
    # Test with user ID 1
    response_user1 = jsonplaceholder_client.get_todos(user_id=1)
    validate_response_status(response_user1, 200)
    todos_user1 = response_user1.json()
    
    # Test with user ID 2
    response_user2 = jsonplaceholder_client.get_todos(user_id=2)
    validate_response_status(response_user2, 200)
    todos_user2 = response_user2.json()
    
    # Validate both return todos
    assert len(todos_user1) > 0, "User 1 should have todos"
    assert len(todos_user2) > 0, "User 2 should have todos"
    
    # Validate all todos belong to correct users
    assert all(t["userId"] == 1 for t in todos_user1), "All todos should belong to user 1"
    assert all(t["userId"] == 2 for t in todos_user2), "All todos should belong to user 2"
    
    # Validate the todo sets are different
    todo_ids_user1 = {t["id"] for t in todos_user1}
    todo_ids_user2 = {t["id"] for t in todos_user2}
    assert todo_ids_user1.isdisjoint(todo_ids_user2), \
        "Todos from different users should not overlap"


@pytest.mark.filters
def test_filter_todos_returns_subset_of_all_todos(jsonplaceholder_client):
    """
    Test that filtered todos are a subset of all todos.
    
    Validates that filtering by userId returns fewer todos than
    requesting all todos without a filter.
    
    Requirements: 6.1, 6.3
    """
    # Get all todos
    response_all = jsonplaceholder_client.get_todos()
    validate_response_status(response_all, 200)
    all_todos = response_all.json()
    
    # Get filtered todos
    user_id = 1
    response_filtered = jsonplaceholder_client.get_todos(user_id=user_id)
    validate_response_status(response_filtered, 200)
    filtered_todos = response_filtered.json()
    
    # Validate filtered is subset
    assert len(filtered_todos) < len(all_todos), \
        "Filtered todos should be fewer than all todos"
    assert len(filtered_todos) > 0, "Should have at least one filtered todo"
    
    # Validate all filtered todos exist in all todos
    all_todo_ids = {t["id"] for t in all_todos}
    for todo in filtered_todos:
        assert todo["id"] in all_todo_ids, \
            f"Filtered todo {todo['id']} should exist in all todos"


# ============================================================================
# ALBUMS FILTER TESTS
# ============================================================================

@pytest.mark.filters
@pytest.mark.smoke
def test_filter_albums_by_user_id(jsonplaceholder_client):
    """
    Test that GET /albums?userId=1 filters albums by user ID.
    
    Validates that:
    - Request returns 200 status
    - All returned albums belong to the specified user
    - At least one album is returned
    
    Requirements: 6.1, 6.3
    """
    user_id = 1
    response = jsonplaceholder_client.get_albums(user_id=user_id)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Get albums and validate filtering
    albums = response.json()
    assert isinstance(albums, list), "Response should be a list"
    assert len(albums) > 0, f"Should return at least one album for userId {user_id}"
    
    # Validate all albums belong to the specified user
    for album in albums:
        assert album["userId"] == user_id, \
            f"Album {album['id']} has userId {album['userId']}, expected {user_id}"


@pytest.mark.filters
def test_filter_albums_by_different_user_ids(jsonplaceholder_client):
    """
    Test filtering albums by multiple different user IDs.
    
    Validates that the filter correctly returns different sets of albums
    for different user IDs.
    
    Requirements: 6.1, 6.3
    """
    # Test with user ID 1
    response_user1 = jsonplaceholder_client.get_albums(user_id=1)
    validate_response_status(response_user1, 200)
    albums_user1 = response_user1.json()
    
    # Test with user ID 2
    response_user2 = jsonplaceholder_client.get_albums(user_id=2)
    validate_response_status(response_user2, 200)
    albums_user2 = response_user2.json()
    
    # Validate both return albums
    assert len(albums_user1) > 0, "User 1 should have albums"
    assert len(albums_user2) > 0, "User 2 should have albums"
    
    # Validate all albums belong to correct users
    assert all(a["userId"] == 1 for a in albums_user1), "All albums should belong to user 1"
    assert all(a["userId"] == 2 for a in albums_user2), "All albums should belong to user 2"
    
    # Validate the album sets are different
    album_ids_user1 = {a["id"] for a in albums_user1}
    album_ids_user2 = {a["id"] for a in albums_user2}
    assert album_ids_user1.isdisjoint(album_ids_user2), \
        "Albums from different users should not overlap"


@pytest.mark.filters
def test_filter_albums_returns_subset_of_all_albums(jsonplaceholder_client):
    """
    Test that filtered albums are a subset of all albums.
    
    Validates that filtering by userId returns fewer albums than
    requesting all albums without a filter.
    
    Requirements: 6.1, 6.3
    """
    # Get all albums
    response_all = jsonplaceholder_client.get_albums()
    validate_response_status(response_all, 200)
    all_albums = response_all.json()
    
    # Get filtered albums
    user_id = 1
    response_filtered = jsonplaceholder_client.get_albums(user_id=user_id)
    validate_response_status(response_filtered, 200)
    filtered_albums = response_filtered.json()
    
    # Validate filtered is subset
    assert len(filtered_albums) < len(all_albums), \
        "Filtered albums should be fewer than all albums"
    assert len(filtered_albums) > 0, "Should have at least one filtered album"
    
    # Validate all filtered albums exist in all albums
    all_album_ids = {a["id"] for a in all_albums}
    for album in filtered_albums:
        assert album["id"] in all_album_ids, \
            f"Filtered album {album['id']} should exist in all albums"


# ============================================================================
# CROSS-RESOURCE FILTER TESTS
# ============================================================================

@pytest.mark.filters
def test_filter_consistency_across_resources(jsonplaceholder_client):
    """
    Test that filtering works consistently across different resources.
    
    Validates that the same user ID returns data from posts, todos, and albums
    for that user, demonstrating consistent filter behavior.
    
    Requirements: 6.1, 6.3
    """
    user_id = 1
    
    # Get filtered data from multiple resources
    posts_response = jsonplaceholder_client.get_posts(user_id=user_id)
    todos_response = jsonplaceholder_client.get_todos(user_id=user_id)
    albums_response = jsonplaceholder_client.get_albums(user_id=user_id)
    
    # Validate all requests succeed
    validate_response_status(posts_response, 200)
    validate_response_status(todos_response, 200)
    validate_response_status(albums_response, 200)
    
    # Get data
    posts = posts_response.json()
    todos = todos_response.json()
    albums = albums_response.json()
    
    # Validate all return data
    assert len(posts) > 0, f"User {user_id} should have posts"
    assert len(todos) > 0, f"User {user_id} should have todos"
    assert len(albums) > 0, f"User {user_id} should have albums"
    
    # Validate all belong to the same user
    assert all(p["userId"] == user_id for p in posts), "All posts should belong to user"
    assert all(t["userId"] == user_id for t in todos), "All todos should belong to user"
    assert all(a["userId"] == user_id for a in albums), "All albums should belong to user"
