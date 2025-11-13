"""
JSONPlaceholder API Test Fixtures.

This module provides pytest fixtures specifically for testing the JSONPlaceholder API.
It includes fixtures for the API client, sample test data, and helper functions for
validation.

Fixtures:
- jsonplaceholder_client: Session-scoped client for JSONPlaceholder API
- sample_post_data: Sample data for creating posts
- sample_user_data: Sample data for creating users
- sample_comment_data: Sample data for creating comments
- sample_todo_data: Sample data for creating todos

Helper Functions:
- validate_email_format: Validates email format using regex
"""

import re
import logging
import pytest
from typing import Dict, Any

from core.clients.jsonplaceholder_client import JSONPlaceholderClient

logger = logging.getLogger(__name__)


# ============================================================================
# JSONPLACEHOLDER CLIENT FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def jsonplaceholder_client():
    """
    Provide JSONPlaceholder API client for the entire test session.
    
    Scope: session - Reused across all tests for performance
    
    This fixture creates a single JSONPlaceholderClient instance that is shared
    across all tests in the session. The client is automatically closed after
    all tests complete.
    
    Yields:
        JSONPlaceholderClient: Configured client for JSONPlaceholder API
        
    Example:
        >>> def test_get_posts(jsonplaceholder_client):
        ...     response = jsonplaceholder_client.get_posts()
        ...     assert response.status_code == 200
    """
    client = JSONPlaceholderClient()
    
    logger.info("JSONPlaceholder client created for test session")
    
    yield client
    
    # Cleanup
    client.close()
    logger.info("JSONPlaceholder client closed")


# ============================================================================
# SAMPLE DATA FIXTURES
# ============================================================================

@pytest.fixture
def sample_post_data() -> Dict[str, Any]:
    """
    Provide sample data for creating a post.
    
    Scope: function - New data for each test
    
    Returns:
        Dict[str, Any]: Dictionary containing post data with userId, title, and body
        
    Example:
        >>> def test_create_post(jsonplaceholder_client, sample_post_data):
        ...     response = jsonplaceholder_client.create_post(sample_post_data)
        ...     assert response.status_code == 201
        ...     data = response.json()
        ...     assert data["title"] == sample_post_data["title"]
    """
    return {
        "userId": 1,
        "title": "Test Post Title",
        "body": "Test post body content"
    }


@pytest.fixture
def sample_user_data() -> Dict[str, Any]:
    """
    Provide sample data for creating a user.
    
    Scope: function - New data for each test
    
    Returns:
        Dict[str, Any]: Dictionary containing user data with name, username, email, and address
        
    Example:
        >>> def test_create_user(jsonplaceholder_client, sample_user_data):
        ...     response = jsonplaceholder_client.create_user(sample_user_data)
        ...     assert response.status_code == 201
        ...     data = response.json()
        ...     assert data["email"] == sample_user_data["email"]
    """
    return {
        "name": "Test User",
        "username": "testuser",
        "email": "test@example.com",
        "address": {
            "street": "Test Street",
            "suite": "Apt. 123",
            "city": "Test City",
            "zipcode": "12345",
            "geo": {
                "lat": "0.0000",
                "lng": "0.0000"
            }
        },
        "phone": "1-555-123-4567",
        "website": "test.example.com",
        "company": {
            "name": "Test Company",
            "catchPhrase": "Testing is our business",
            "bs": "test automation solutions"
        }
    }


@pytest.fixture
def sample_comment_data() -> Dict[str, Any]:
    """
    Provide sample data for creating a comment.
    
    Scope: function - New data for each test
    
    Returns:
        Dict[str, Any]: Dictionary containing comment data with postId, name, email, and body
        
    Example:
        >>> def test_create_comment(jsonplaceholder_client, sample_comment_data):
        ...     response = jsonplaceholder_client.create_comment(sample_comment_data)
        ...     assert response.status_code == 201
        ...     data = response.json()
        ...     assert data["email"] == sample_comment_data["email"]
    """
    return {
        "postId": 1,
        "name": "Test Comment",
        "email": "test@example.com",
        "body": "Test comment body content"
    }


@pytest.fixture
def sample_todo_data() -> Dict[str, Any]:
    """
    Provide sample data for creating a todo.
    
    Scope: function - New data for each test
    
    Returns:
        Dict[str, Any]: Dictionary containing todo data with userId, title, and completed
        
    Example:
        >>> def test_create_todo(jsonplaceholder_client, sample_todo_data):
        ...     response = jsonplaceholder_client.create_todo(sample_todo_data)
        ...     assert response.status_code == 201
        ...     data = response.json()
        ...     assert data["title"] == sample_todo_data["title"]
    """
    return {
        "userId": 1,
        "title": "Test Todo",
        "completed": False
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_email_format(email: str) -> bool:
    """
    Validate email format using regex pattern.
    
    This function checks if an email address follows a valid format according
    to a standard email regex pattern. It validates:
    - Local part (before @): alphanumeric, dots, underscores, percent, plus, hyphen
    - Domain part (after @): alphanumeric, dots, hyphen
    - TLD: at least 2 characters
    
    Args:
        email: Email address string to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
        
    Example:
        >>> validate_email_format("user@example.com")
        True
        >>> validate_email_format("invalid.email")
        False
        >>> validate_email_format("user@domain.co.uk")
        True
        >>> validate_email_format("user+tag@example.com")
        True
    """
    # Standard email regex pattern
    # Matches: local-part@domain.tld
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return re.match(pattern, email) is not None
