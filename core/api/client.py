"""
Robust API client with session management, retry logic, and authentication.

This module provides a comprehensive HTTP client built on top of requests
with automatic retry, exponential backoff, authentication management, and
detailed logging capabilities.
"""

import logging
import time
from typing import Optional, Dict, Any, List, Callable
from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException, Timeout, ConnectionError
from urllib3.util.retry import Retry

from core.config.settings import get_settings


logger = logging.getLogger(__name__)


class APIClient:
    """
    Robust API client with advanced features for test automation.
    
    Features:
    - Automatic retry with configurable backoff strategies
    - Session management with connection pooling
    - Automatic authentication and token management
    - Detailed request/response logging
    - Timeout handling
    - Custom headers and hooks support
    
    Example:
        >>> client = APIClient()
        >>> client.authenticate("user@example.com", "password")
        >>> response = client.get("/users/123")
        >>> assert response.status_code == 200
    """
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        retries: Optional[int] = None,
        verify_ssl: bool = True
    ):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL for API requests (defaults to settings)
            timeout: Request timeout in seconds (defaults to settings)
            retries: Number of retry attempts (defaults to settings)
            verify_ssl: Whether to verify SSL certificates
        """
        self.settings = get_settings()
        self.base_url = base_url or self.settings.api_base_url
        self.timeout = timeout or self.settings.api_timeout
        self.retries = retries or self.settings.api_retries
        self.verify_ssl = verify_ssl
        
        # Authentication state
        self._token: Optional[str] = None
        self._token_type: str = "Bearer"
        self._token_expiry: Optional[datetime] = None
        self._refresh_token: Optional[str] = None
        
        # Session with retry configuration
        self.session = self._create_session_with_retry()
        
        # Request/response hooks
        self._request_hooks: List[Callable] = []
        self._response_hooks: List[Callable] = []
        
        logger.info(
            f"APIClient initialized with base_url={self.base_url}, "
            f"timeout={self.timeout}s, retries={self.retries}"
        )
    
    def _create_session_with_retry(self) -> requests.Session:
        """
        Create a requests session with retry configuration.
        
        Implements retry logic with exponential backoff for transient failures.
        Retries on specific HTTP status codes and connection errors.
        
        Returns:
            requests.Session: Configured session with retry adapter
        """
        session = requests.Session()
        
        # Configure retry strategy based on settings
        retry_strategy = Retry(
            total=self.retries,
            backoff_factor=self.settings.retry_backoff_multiplier,
            status_forcelist=self.settings.retry_status_codes_list,
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"],
            raise_on_status=False,
            respect_retry_after_header=True
        )
        
        # Create adapter with retry strategy
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20,
            pool_block=False
        )
        
        # Mount adapter for both HTTP and HTTPS
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set default headers
        session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"TestAutomation-APIClient/{self.settings.api_version}"
        })
        
        logger.debug("Session created with retry strategy")
        return session
    
    def _build_url(self, endpoint: str) -> str:
        """
        Build full URL from endpoint.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            str: Complete URL
        """
        # Handle absolute URLs
        if endpoint.startswith(("http://", "https://")):
            return endpoint
        
        # Ensure endpoint starts with /
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        
        return urljoin(self.base_url, endpoint)
    
    def _prepare_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Prepare request headers with authentication.
        
        Args:
            headers: Additional headers to include
            
        Returns:
            Dict[str, str]: Complete headers dictionary
        """
        request_headers = {}
        
        # Add authentication header if token exists
        if self._token:
            request_headers["Authorization"] = f"{self._token_type} {self._token}"
        
        # Merge with provided headers
        if headers:
            request_headers.update(headers)
        
        return request_headers
    
    def _log_request(self, method: str, url: str, **kwargs):
        """Log HTTP request details."""
        if self.settings.log_http_requests:
            logger.info(f"→ {method.upper()} {url}")
            if kwargs.get("params"):
                logger.debug(f"  Query params: {kwargs['params']}")
            if kwargs.get("json"):
                logger.debug(f"  Request body: {kwargs['json']}")
            if kwargs.get("headers"):
                # Mask sensitive headers
                safe_headers = {
                    k: "***" if k.lower() in ["authorization", "api-key"] else v
                    for k, v in kwargs["headers"].items()
                }
                logger.debug(f"  Headers: {safe_headers}")
    
    def _log_response(self, response: requests.Response, duration: float):
        """Log HTTP response details."""
        if self.settings.log_http_requests:
            logger.info(
                f"← {response.status_code} {response.reason} "
                f"({duration:.2f}s) {response.request.method} {response.url}"
            )
            logger.debug(f"  Response headers: {dict(response.headers)}")
            
            # Log response body for non-2xx or if debug enabled
            if not response.ok or logger.isEnabledFor(logging.DEBUG):
                try:
                    logger.debug(f"  Response body: {response.json()}")
                except Exception:
                    logger.debug(f"  Response body: {response.text[:500]}")
    
    def _execute_request_hooks(self, method: str, url: str, **kwargs):
        """Execute registered request hooks."""
        for hook in self._request_hooks:
            try:
                hook(method, url, **kwargs)
            except Exception as e:
                logger.warning(f"Request hook failed: {e}")
    
    def _execute_response_hooks(self, response: requests.Response):
        """Execute registered response hooks."""
        for hook in self._response_hooks:
            try:
                hook(response)
            except Exception as e:
                logger.warning(f"Response hook failed: {e}")
    
    def _check_token_expiry(self):
        """Check if token is expired and refresh if needed."""
        if not self._token or not self._token_expiry:
            return
        
        # Check if token will expire soon (within buffer time)
        buffer = timedelta(seconds=self.settings.token_expiration_buffer)
        if datetime.now() + buffer >= self._token_expiry:
            logger.info("Token expiring soon, attempting refresh")
            if self.settings.auto_refresh_token and self._refresh_token:
                try:
                    self.refresh_token()
                except Exception as e:
                    logger.error(f"Token refresh failed: {e}")
                    self._token = None
                    self._token_expiry = None
    
    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
        allow_redirects: bool = True,
        **kwargs
    ) -> requests.Response:
        """
        Execute HTTP request with retry and logging.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json: JSON request body
            data: Form data or raw body
            headers: Additional headers
            timeout: Request timeout (overrides default)
            allow_redirects: Whether to follow redirects
            **kwargs: Additional arguments for requests
            
        Returns:
            requests.Response: Response object
            
        Raises:
            RequestException: On request failure after retries
        """
        # Check token expiry before request
        self._check_token_expiry()
        
        # Build URL and prepare headers
        url = self._build_url(endpoint)
        request_headers = self._prepare_headers(headers)
        request_timeout = timeout or self.timeout
        
        # Execute request hooks
        self._execute_request_hooks(method, url, params=params, json=json, headers=request_headers)
        
        # Log request
        self._log_request(method, url, params=params, json=json, headers=request_headers)
        
        # Execute request with timing
        start_time = time.time()
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                data=data,
                headers=request_headers,
                timeout=request_timeout,
                allow_redirects=allow_redirects,
                verify=self.verify_ssl,
                **kwargs
            )
            duration = time.time() - start_time
            
            # Log response
            self._log_response(response, duration)
            
            # Execute response hooks
            self._execute_response_hooks(response)
            
            return response
            
        except Timeout as e:
            duration = time.time() - start_time
            logger.error(f"Request timeout after {duration:.2f}s: {method} {url}")
            raise
        except ConnectionError as e:
            duration = time.time() - start_time
            logger.error(f"Connection error after {duration:.2f}s: {method} {url} - {e}")
            raise
        except RequestException as e:
            duration = time.time() - start_time
            logger.error(f"Request failed after {duration:.2f}s: {method} {url} - {e}")
            raise
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Execute GET request."""
        return self.request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """Execute POST request."""
        return self.request("POST", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """Execute PUT request."""
        return self.request("PUT", endpoint, **kwargs)
    
    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        """Execute PATCH request."""
        return self.request("PATCH", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Execute DELETE request."""
        return self.request("DELETE", endpoint, **kwargs)
    
    def head(self, endpoint: str, **kwargs) -> requests.Response:
        """Execute HEAD request."""
        return self.request("HEAD", endpoint, **kwargs)
    
    def options(self, endpoint: str, **kwargs) -> requests.Response:
        """Execute OPTIONS request."""
        return self.request("OPTIONS", endpoint, **kwargs)
    
    def add_request_hook(self, hook: Callable):
        """
        Add a request hook function.
        
        Args:
            hook: Callable that receives (method, url, **kwargs)
        """
        self._request_hooks.append(hook)
    
    def add_response_hook(self, hook: Callable):
        """
        Add a response hook function.
        
        Args:
            hook: Callable that receives (response)
        """
        self._response_hooks.append(hook)
    
    def close(self):
        """Close the session and cleanup resources."""
        if self.session:
            self.session.close()
            logger.debug("Session closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    # ============================================================================
    # AUTHENTICATION METHODS
    # ============================================================================
    
    def authenticate(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        auth_endpoint: str = "/auth/login",
        **kwargs
    ) -> str:
        """
        Authenticate with the API and store access token.
        
        Supports multiple authentication types based on settings:
        - Bearer token authentication (default)
        - Basic authentication
        - OAuth2
        - API key authentication
        
        Args:
            username: Username or email (defaults to settings)
            password: Password (defaults to settings)
            auth_endpoint: Authentication endpoint
            **kwargs: Additional authentication parameters
            
        Returns:
            str: Access token
            
        Raises:
            RequestException: On authentication failure
            
        Example:
            >>> client = APIClient()
            >>> token = client.authenticate("user@example.com", "password")
            >>> print(f"Authenticated with token: {token[:10]}...")
        """
        username = username or self.settings.auth_user
        password = password or self.settings.auth_password
        
        logger.info(f"Authenticating user: {username}")
        
        # Prepare authentication request based on auth type
        if self.settings.auth_type == "bearer":
            response = self._authenticate_bearer(username, password, auth_endpoint, **kwargs)
        elif self.settings.auth_type == "basic":
            response = self._authenticate_basic(username, password)
        elif self.settings.auth_type == "oauth2":
            response = self._authenticate_oauth2(username, password, **kwargs)
        elif self.settings.auth_type == "api_key":
            response = self._authenticate_api_key(**kwargs)
        else:
            raise ValueError(f"Unsupported auth type: {self.settings.auth_type}")
        
        # Extract and store token
        self._extract_and_store_token(response)
        
        logger.info(f"Authentication successful for user: {username}")
        return self._token
    
    def _authenticate_bearer(
        self,
        username: str,
        password: str,
        auth_endpoint: str,
        **kwargs
    ) -> requests.Response:
        """
        Authenticate using bearer token (JWT).
        
        Args:
            username: Username or email
            password: Password
            auth_endpoint: Authentication endpoint
            **kwargs: Additional parameters
            
        Returns:
            requests.Response: Authentication response
        """
        payload = {
            "username": username,
            "email": username,  # Support both username and email
            "password": password,
            **kwargs
        }
        
        response = self.post(auth_endpoint, json=payload)
        
        if not response.ok:
            logger.error(f"Authentication failed: {response.status_code} - {response.text}")
            response.raise_for_status()
        
        return response
    
    def _authenticate_basic(self, username: str, password: str) -> requests.Response:
        """
        Authenticate using HTTP Basic Auth.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            requests.Response: Mock response with credentials
        """
        from requests.auth import HTTPBasicAuth
        
        # Store basic auth in session
        self.session.auth = HTTPBasicAuth(username, password)
        
        # Create mock response for consistency
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"message": "Basic auth configured"}'
        
        logger.info("Basic authentication configured")
        return mock_response
    
    def _authenticate_oauth2(
        self,
        username: str,
        password: str,
        **kwargs
    ) -> requests.Response:
        """
        Authenticate using OAuth2 password grant.
        
        Args:
            username: Username
            password: Password
            **kwargs: Additional OAuth2 parameters
            
        Returns:
            requests.Response: Token response
        """
        if not self.settings.oauth2_token_url:
            raise ValueError("OAuth2 token URL not configured")
        
        payload = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": self.settings.oauth2_client_id,
            "client_secret": self.settings.oauth2_client_secret,
            "scope": self.settings.oauth2_scope,
            **kwargs
        }
        
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        response = self.post(self.settings.oauth2_token_url, data=payload)
        
        if not response.ok:
            logger.error(f"OAuth2 authentication failed: {response.status_code}")
            response.raise_for_status()
        
        return response
    
    def _authenticate_api_key(self, **kwargs) -> requests.Response:
        """
        Authenticate using API key.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            requests.Response: Mock response
        """
        api_key = kwargs.get("api_key") or self.settings.api_key
        
        if not api_key:
            raise ValueError("API key not provided")
        
        # Store API key in session headers
        self.session.headers["X-API-Key"] = api_key
        
        # Create mock response
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'{"message": "API key configured"}'
        
        logger.info("API key authentication configured")
        return mock_response
    
    def _extract_and_store_token(self, response: requests.Response):
        """
        Extract token from authentication response and store it.
        
        Args:
            response: Authentication response
        """
        try:
            data = response.json()
        except Exception:
            logger.warning("Could not parse authentication response as JSON")
            return
        
        # Try common token field names
        token_fields = ["access_token", "token", "accessToken", "jwt", "bearer"]
        for field in token_fields:
            if field in data:
                self._token = data[field]
                break
        
        # Extract refresh token if available
        refresh_fields = ["refresh_token", "refreshToken"]
        for field in refresh_fields:
            if field in data:
                self._refresh_token = data[field]
                break
        
        # Extract token type
        if "token_type" in data:
            self._token_type = data["token_type"]
        elif "tokenType" in data:
            self._token_type = data["tokenType"]
        
        # Calculate token expiry
        if "expires_in" in data:
            expires_in = int(data["expires_in"])
            self._token_expiry = datetime.now() + timedelta(seconds=expires_in)
            logger.debug(f"Token expires at: {self._token_expiry}")
        elif "expiresIn" in data:
            expires_in = int(data["expiresIn"])
            self._token_expiry = datetime.now() + timedelta(seconds=expires_in)
            logger.debug(f"Token expires at: {self._token_expiry}")
        
        if not self._token:
            logger.warning("Could not extract access token from response")
    
    def refresh_token(self, refresh_endpoint: Optional[str] = None) -> str:
        """
        Refresh the access token using refresh token.
        
        Args:
            refresh_endpoint: Token refresh endpoint (defaults to settings)
            
        Returns:
            str: New access token
            
        Raises:
            ValueError: If refresh token is not available
            RequestException: On refresh failure
            
        Example:
            >>> client = APIClient()
            >>> client.authenticate("user@example.com", "password")
            >>> # ... time passes ...
            >>> new_token = client.refresh_token()
        """
        if not self._refresh_token:
            raise ValueError("No refresh token available")
        
        refresh_endpoint = refresh_endpoint or self.settings.token_refresh_endpoint
        
        logger.info("Refreshing access token")
        
        payload = {
            "refresh_token": self._refresh_token,
            "grant_type": "refresh_token"
        }
        
        # Temporarily remove token to avoid using expired token
        old_token = self._token
        self._token = None
        
        try:
            response = self.post(refresh_endpoint, json=payload)
            
            if not response.ok:
                logger.error(f"Token refresh failed: {response.status_code}")
                response.raise_for_status()
            
            # Extract and store new token
            self._extract_and_store_token(response)
            
            logger.info("Token refreshed successfully")
            return self._token
            
        except Exception as e:
            # Restore old token on failure
            self._token = old_token
            logger.error(f"Token refresh failed: {e}")
            raise
    
    def set_token(self, token: str, token_type: str = "Bearer"):
        """
        Manually set authentication token.
        
        Useful when token is obtained externally or for testing.
        
        Args:
            token: Access token
            token_type: Token type (Bearer, JWT, etc.)
            
        Example:
            >>> client = APIClient()
            >>> client.set_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        """
        self._token = token
        self._token_type = token_type
        logger.info(f"Token set manually (type: {token_type})")
    
    def clear_authentication(self):
        """
        Clear all authentication data.
        
        Removes tokens and authentication headers from the session.
        """
        self._token = None
        self._token_type = "Bearer"
        self._token_expiry = None
        self._refresh_token = None
        
        # Remove auth headers
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
        if "X-API-Key" in self.session.headers:
            del self.session.headers["X-API-Key"]
        
        # Remove basic auth
        self.session.auth = None
        
        logger.info("Authentication cleared")
    
    def is_authenticated(self) -> bool:
        """
        Check if client is currently authenticated.
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        return self._token is not None or self.session.auth is not None
    
    def get_token(self) -> Optional[str]:
        """
        Get current access token.
        
        Returns:
            Optional[str]: Current access token or None
        """
        return self._token
    
    def validate_credentials(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> bool:
        """
        Validate credentials without storing authentication.
        
        Args:
            username: Username to validate
            password: Password to validate
            
        Returns:
            bool: True if credentials are valid, False otherwise
            
        Example:
            >>> client = APIClient()
            >>> is_valid = client.validate_credentials("user@example.com", "password")
            >>> print(f"Credentials valid: {is_valid}")
        """
        username = username or self.settings.auth_user
        password = password or self.settings.auth_password
        
        logger.info(f"Validating credentials for user: {username}")
        
        try:
            # Save current auth state
            old_token = self._token
            old_token_type = self._token_type
            old_token_expiry = self._token_expiry
            old_refresh_token = self._refresh_token
            
            # Try to authenticate
            self.authenticate(username, password)
            
            # Restore old auth state
            self._token = old_token
            self._token_type = old_token_type
            self._token_expiry = old_token_expiry
            self._refresh_token = old_refresh_token
            
            logger.info(f"Credentials valid for user: {username}")
            return True
            
        except Exception as e:
            logger.warning(f"Credentials invalid for user {username}: {e}")
            return False
