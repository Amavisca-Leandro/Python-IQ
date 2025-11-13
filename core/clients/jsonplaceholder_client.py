"""
JSONPlaceholder API Client.

This module provides a specialized client for interacting with the JSONPlaceholder
API (https://jsonplaceholder.typicode.com/), a free fake REST API for testing and prototyping.

The client wraps the core APIClient with JSONPlaceholder-specific methods for
resources like posts, users, comments, todos, and albums.
"""

import logging
from typing import Optional, Dict, Any

import requests

from core.api.client import APIClient


logger = logging.getLogger(__name__)


class JSONPlaceholderClient:
    """
    Client for interacting with the JSONPlaceholder API.
    
    This client provides convenient methods for all JSONPlaceholder endpoints,
    including posts, users, comments, todos, and albums. It handles request
    construction, parameter validation, and response handling.
    
    Features:
    - Full CRUD operations for posts, users, comments, todos, and albums
    - Query parameter support for filtering
    - Built on robust APIClient with retry and logging
    - Type hints for better IDE support
    
    Example:
        >>> client = JSONPlaceholderClient()
        >>> response = client.get_posts()
        >>> assert response.status_code == 200
        >>> posts = response.json()
        >>> client.close()
        
        # Or use as context manager
        >>> with JSONPlaceholderClient() as client:
        ...     response = client.get_post(1)
        ...     post = response.json()
    """
    
    def __init__(
        self,
        base_url: str = "https://jsonplaceholder.typicode.com",
        timeout: int = 10,
        retries: int = 2
    ):
        """
        Initialize the JSONPlaceholder client.
        
        Args:
            base_url: Base URL for the JSONPlaceholder API
                     (default: https://jsonplaceholder.typicode.com)
            timeout: Request timeout in seconds (default: 10)
            retries: Number of retry attempts for failed requests (default: 2)
        """
        self.client = APIClient(
            base_url=base_url,
            timeout=timeout,
            retries=retries
        )
        logger.info(f"JSONPlaceholderClient initialized with base_url={base_url}")
    
    def close(self):
        """
        Close the HTTP session and cleanup resources.
        
        Should be called when done using the client to properly release
        connection pool resources.
        
        Example:
            >>> client = JSONPlaceholderClient()
            >>> try:
            ...     response = client.get_posts()
            ... finally:
            ...     client.close()
        """
        self.client.close()
        logger.debug("JSONPlaceholderClient session closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    # ============================================================================
    # POSTS ENDPOINTS
    # ============================================================================
    
    def get_posts(self, user_id: Optional[int] = None) -> requests.Response:
        """
        Get all posts or filter by user ID.
        
        Args:
            user_id: Optional user ID to filter posts
            
        Returns:
            requests.Response: Response containing list of posts
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> response = client.get_posts()
            >>> all_posts = response.json()
            >>> 
            >>> response = client.get_posts(user_id=1)
            >>> user_posts = response.json()
        """
        params = {"userId": user_id} if user_id is not None else None
        return self.client.get("/posts", params=params)
    
    def get_post(self, post_id: int) -> requests.Response:
        """
        Get a specific post by ID.
        
        Args:
            post_id: ID of the post to retrieve
            
        Returns:
            requests.Response: Response containing the post data
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> response = client.get_post(1)
            >>> post = response.json()
            >>> assert post["id"] == 1
        """
        return self.client.get(f"/posts/{post_id}")
    
    def create_post(self, data: Dict[str, Any]) -> requests.Response:
        """
        Create a new post.
        
        Args:
            data: Post data dictionary containing userId, title, and body
            
        Returns:
            requests.Response: Response containing the created post with ID
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> post_data = {
            ...     "userId": 1,
            ...     "title": "My Post",
            ...     "body": "Post content"
            ... }
            >>> response = client.create_post(post_data)
            >>> assert response.status_code == 201
            >>> created_post = response.json()
        """
        return self.client.post("/posts", json=data)
    
    def update_post(self, post_id: int, data: Dict[str, Any]) -> requests.Response:
        """
        Update a post completely (PUT - replaces all fields).
        
        Args:
            post_id: ID of the post to update
            data: Complete post data dictionary
            
        Returns:
            requests.Response: Response containing the updated post
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> updated_data = {
            ...     "userId": 1,
            ...     "title": "Updated Title",
            ...     "body": "Updated content"
            ... }
            >>> response = client.update_post(1, updated_data)
            >>> assert response.status_code == 200
        """
        return self.client.put(f"/posts/{post_id}", json=data)
    
    def patch_post(self, post_id: int, data: Dict[str, Any]) -> requests.Response:
        """
        Partially update a post (PATCH - updates only specified fields).
        
        Args:
            post_id: ID of the post to update
            data: Partial post data dictionary with fields to update
            
        Returns:
            requests.Response: Response containing the updated post
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> partial_data = {"title": "New Title"}
            >>> response = client.patch_post(1, partial_data)
            >>> assert response.status_code == 200
        """
        return self.client.patch(f"/posts/{post_id}", json=data)
    
    def delete_post(self, post_id: int) -> requests.Response:
        """
        Delete a post.
        
        Args:
            post_id: ID of the post to delete
            
        Returns:
            requests.Response: Response confirming deletion
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> response = client.delete_post(1)
            >>> assert response.status_code == 200
        """
        return self.client.delete(f"/posts/{post_id}")

    # ============================================================================
    # USERS ENDPOINTS
    # ============================================================================
    
    def get_users(self) -> requests.Response:
        """
        Get all users.
        
        Returns:
            requests.Response: Response containing list of all users
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> response = client.get_users()
            >>> users = response.json()
            >>> assert len(users) == 10
        """
        return self.client.get("/users")
    
    def get_user(self, user_id: int) -> requests.Response:
        """
        Get a specific user by ID.
        
        Args:
            user_id: ID of the user to retrieve
            
        Returns:
            requests.Response: Response containing the user data
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> response = client.get_user(1)
            >>> user = response.json()
            >>> assert user["id"] == 1
        """
        return self.client.get(f"/users/{user_id}")
    
    def create_user(self, data: Dict[str, Any]) -> requests.Response:
        """
        Create a new user.
        
        Args:
            data: User data dictionary containing name, username, email, etc.
            
        Returns:
            requests.Response: Response containing the created user with ID
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> user_data = {
            ...     "name": "John Doe",
            ...     "username": "johndoe",
            ...     "email": "john@example.com"
            ... }
            >>> response = client.create_user(user_data)
            >>> assert response.status_code == 201
        """
        return self.client.post("/users", json=data)
    
    def update_user(self, user_id: int, data: Dict[str, Any]) -> requests.Response:
        """
        Update a user completely (PUT - replaces all fields).
        
        Args:
            user_id: ID of the user to update
            data: Complete user data dictionary
            
        Returns:
            requests.Response: Response containing the updated user
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> updated_data = {
            ...     "name": "Jane Doe",
            ...     "username": "janedoe",
            ...     "email": "jane@example.com"
            ... }
            >>> response = client.update_user(1, updated_data)
            >>> assert response.status_code == 200
        """
        return self.client.put(f"/users/{user_id}", json=data)
    
    def delete_user(self, user_id: int) -> requests.Response:
        """
        Delete a user.
        
        Args:
            user_id: ID of the user to delete
            
        Returns:
            requests.Response: Response confirming deletion
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> response = client.delete_user(1)
            >>> assert response.status_code == 200
        """
        return self.client.delete(f"/users/{user_id}")

    # ============================================================================
    # COMMENTS ENDPOINTS
    # ============================================================================
    
    def get_comments(self, post_id: Optional[int] = None) -> requests.Response:
        """
        Get all comments or filter by post ID.
        
        Args:
            post_id: Optional post ID to filter comments
            
        Returns:
            requests.Response: Response containing list of comments
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> response = client.get_comments()
            >>> all_comments = response.json()
            >>> 
            >>> response = client.get_comments(post_id=1)
            >>> post_comments = response.json()
        """
        params = {"postId": post_id} if post_id is not None else None
        return self.client.get("/comments", params=params)
    
    def get_comment(self, comment_id: int) -> requests.Response:
        """
        Get a specific comment by ID.
        
        Args:
            comment_id: ID of the comment to retrieve
            
        Returns:
            requests.Response: Response containing the comment data
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> response = client.get_comment(1)
            >>> comment = response.json()
            >>> assert comment["id"] == 1
        """
        return self.client.get(f"/comments/{comment_id}")
    
    def create_comment(self, data: Dict[str, Any]) -> requests.Response:
        """
        Create a new comment.
        
        Args:
            data: Comment data dictionary containing postId, name, email, and body
            
        Returns:
            requests.Response: Response containing the created comment with ID
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> comment_data = {
            ...     "postId": 1,
            ...     "name": "My Comment",
            ...     "email": "user@example.com",
            ...     "body": "Comment content"
            ... }
            >>> response = client.create_comment(comment_data)
            >>> assert response.status_code == 201
        """
        return self.client.post("/comments", json=data)

    # ============================================================================
    # TODOS ENDPOINTS
    # ============================================================================
    
    def get_todos(self, user_id: Optional[int] = None) -> requests.Response:
        """
        Get all todos or filter by user ID.
        
        Args:
            user_id: Optional user ID to filter todos
            
        Returns:
            requests.Response: Response containing list of todos
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> response = client.get_todos()
            >>> all_todos = response.json()
            >>> 
            >>> response = client.get_todos(user_id=1)
            >>> user_todos = response.json()
        """
        params = {"userId": user_id} if user_id is not None else None
        return self.client.get("/todos", params=params)
    
    def get_todo(self, todo_id: int) -> requests.Response:
        """
        Get a specific todo by ID.
        
        Args:
            todo_id: ID of the todo to retrieve
            
        Returns:
            requests.Response: Response containing the todo data
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> response = client.get_todo(1)
            >>> todo = response.json()
            >>> assert todo["id"] == 1
        """
        return self.client.get(f"/todos/{todo_id}")
    
    def create_todo(self, data: Dict[str, Any]) -> requests.Response:
        """
        Create a new todo.
        
        Args:
            data: Todo data dictionary containing userId, title, and completed
            
        Returns:
            requests.Response: Response containing the created todo with ID
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> todo_data = {
            ...     "userId": 1,
            ...     "title": "My Todo",
            ...     "completed": False
            ... }
            >>> response = client.create_todo(todo_data)
            >>> assert response.status_code == 201
        """
        return self.client.post("/todos", json=data)
    
    def update_todo(self, todo_id: int, data: Dict[str, Any]) -> requests.Response:
        """
        Update a todo completely (PUT - replaces all fields).
        
        Args:
            todo_id: ID of the todo to update
            data: Complete todo data dictionary
            
        Returns:
            requests.Response: Response containing the updated todo
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> updated_data = {
            ...     "userId": 1,
            ...     "title": "Updated Todo",
            ...     "completed": True
            ... }
            >>> response = client.update_todo(1, updated_data)
            >>> assert response.status_code == 200
        """
        return self.client.put(f"/todos/{todo_id}", json=data)

    # ============================================================================
    # ALBUMS ENDPOINTS
    # ============================================================================
    
    def get_albums(self, user_id: Optional[int] = None) -> requests.Response:
        """
        Get all albums or filter by user ID.
        
        Args:
            user_id: Optional user ID to filter albums
            
        Returns:
            requests.Response: Response containing list of albums
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> response = client.get_albums()
            >>> all_albums = response.json()
            >>> 
            >>> response = client.get_albums(user_id=1)
            >>> user_albums = response.json()
        """
        params = {"userId": user_id} if user_id is not None else None
        return self.client.get("/albums", params=params)
    
    def get_album(self, album_id: int) -> requests.Response:
        """
        Get a specific album by ID.
        
        Args:
            album_id: ID of the album to retrieve
            
        Returns:
            requests.Response: Response containing the album data
            
        Example:
            >>> client = JSONPlaceholderClient()
            >>> response = client.get_album(1)
            >>> album = response.json()
            >>> assert album["id"] == 1
        """
        return self.client.get(f"/albums/{album_id}")
