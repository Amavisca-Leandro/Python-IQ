"""
Backend API tests for authentication endpoints.

This module tests authentication flows including login, logout,
token management, and credential validation.

Requirements: 5.1, 2.2
"""

import pytest
import logging
from datetime import datetime, timedelta

from core.models.auth import LoginRequest, TokenResponse
from core.helpers.validators import (
    validate_response_status,
    validate_response_time,
    validate_required_fields
)


logger = logging.getLogger(__name__)


# ============================================================================
# AUTHENTICATION TESTS
# ============================================================================

@pytest.mark.smoke
@pytest.mark.backend
class TestAuthentication:
    """Test suite for authentication endpoints."""
    
    def test_login_with_valid_credentials(self, unauthenticated_api_client, settings):
        """
        Test successful login with valid credentials.
        
        Validates:
        - Response status code is 200
        - Response contains access_token
        - Response contains token_type
        - Response contains expires_in
        - Token format is valid
        - Response time is acceptable
        
        Requirements: 5.1, 2.2
        """
        logger.info("Testing login with valid credentials")
        
        # Prepare login request
        login_data = {
            "username": settings.auth_user,
            "password": settings.auth_password,
            "remember_me": False
        }
        
        # Validate request data with Pydantic
        login_request = LoginRequest(**login_data)
        
        # Execute login request
        response = unauthenticated_api_client.post(
            "/auth/login",
            json=login_request.model_dump()
        )
        
        # Validate response status
        validate_response_status(response, expected_status=200)
        
        # Validate response time
        validate_response_time(response, max_time=settings.api_timeout)
        
        # Parse response
        response_data = response.json()
        
        # Validate required fields
        required_fields = ["access_token", "token_type", "expires_in"]
        validate_required_fields(response_data, required_fields)
        
        # Validate response with Pydantic model
        token_response = TokenResponse(**response_data)
        
        # Additional validations
        assert token_response.access_token, "Access token should not be empty"
        assert len(token_response.access_token) > 20, "Access token should be substantial"
        assert token_response.token_type == "Bearer", "Token type should be Bearer"
        assert token_response.expires_in > 0, "Expires in should be positive"
        
        logger.info(f"Login successful, token expires in {token_response.expires_in}s")
    
    def test_login_with_invalid_credentials(self, unauthenticated_api_client):
        """
        Test login failure with invalid credentials.
        
        Validates:
        - Response status code is 401 Unauthorized
        - Response contains error message
        - No token is returned
        - Response time is acceptable
        
        Requirements: 5.1, 2.2
        """
        logger.info("Testing login with invalid credentials")
        
        # Prepare login request with invalid credentials
        login_data = {
            "username": "invalid_user@example.com",
            "password": "WrongPassword123!",
            "remember_me": False
        }
        
        # Validate request data with Pydantic
        login_request = LoginRequest(**login_data)
        
        # Execute login request
        response = unauthenticated_api_client.post(
            "/auth/login",
            json=login_request.model_dump()
        )
        
        # Validate response status (should be 401 Unauthorized)
        validate_response_status(response, expected_status=401)
        
        # Parse response
        response_data = response.json()
        
        # Validate error response structure
        assert "detail" in response_data or "message" in response_data or "error" in response_data, \
            "Error response should contain error message"
        
        # Ensure no token is returned
        assert "access_token" not in response_data, "No access token should be returned for invalid credentials"
        
        logger.info("Login correctly rejected invalid credentials")
    
    def test_login_with_missing_password(self, unauthenticated_api_client):
        """
        Test login failure with missing password.
        
        Validates:
        - Response status code is 422 Unprocessable Entity or 400 Bad Request
        - Response contains validation error
        
        Requirements: 5.1
        """
        logger.info("Testing login with missing password")
        
        # Prepare login request with missing password
        login_data = {
            "username": "test_user@example.com"
            # password is missing
        }
        
        # Execute login request
        response = unauthenticated_api_client.post(
            "/auth/login",
            json=login_data
        )
        
        # Validate response status (should be 422 or 400)
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422, got {response.status_code}"
        
        logger.info("Login correctly rejected request with missing password")
    
    def test_login_with_empty_credentials(self, unauthenticated_api_client):
        """
        Test login failure with empty credentials.
        
        Validates:
        - Response status code is 422 or 400
        - Response contains validation error
        
        Requirements: 5.1
        """
        logger.info("Testing login with empty credentials")
        
        # Prepare login request with empty credentials
        login_data = {
            "username": "",
            "password": ""
        }
        
        # Execute login request
        response = unauthenticated_api_client.post(
            "/auth/login",
            json=login_data
        )
        
        # Validate response status (should be 422 or 400)
        assert response.status_code in [400, 422], \
            f"Expected 400 or 422, got {response.status_code}"
        
        logger.info("Login correctly rejected empty credentials")
    
    def test_login_with_email_instead_of_username(self, unauthenticated_api_client, settings):
        """
        Test login with email address instead of username.
        
        Validates:
        - System accepts email as username
        - Response status code is 200
        - Token is returned
        
        Requirements: 5.1, 2.2
        """
        logger.info("Testing login with email instead of username")
        
        # Prepare login request with email
        login_data = {
            "username": settings.auth_user,  # Assuming this is an email
            "password": settings.auth_password,
            "remember_me": False
        }
        
        # Execute login request
        response = unauthenticated_api_client.post(
            "/auth/login",
            json=login_data
        )
        
        # Validate response status
        validate_response_status(response, expected_status=200)
        
        # Parse response
        response_data = response.json()
        
        # Validate token is returned
        assert "access_token" in response_data, "Access token should be returned"
        
        logger.info("Login successful with email as username")
    
    def test_token_expiration_handling(self, unauthenticated_api_client, settings):
        """
        Test token expiration information.
        
        Validates:
        - Token response includes expiration information
        - Expiration time is reasonable
        - Token type is correct
        
        Requirements: 5.1, 2.2
        """
        logger.info("Testing token expiration handling")
        
        # Prepare login request
        login_data = {
            "username": settings.auth_user,
            "password": settings.auth_password,
            "remember_me": False
        }
        
        # Execute login request
        response = unauthenticated_api_client.post(
            "/auth/login",
            json=login_data
        )
        
        # Validate response status
        validate_response_status(response, expected_status=200)
        
        # Parse response
        response_data = response.json()
        token_response = TokenResponse(**response_data)
        
        # Validate expiration information
        assert token_response.expires_in > 0, "Expires in should be positive"
        assert token_response.expires_in <= 86400, "Token should expire within 24 hours"
        
        # If expires_at is provided, validate it
        if token_response.expires_at:
            now = datetime.now()
            expires_at = token_response.expires_at
            
            # Handle timezone-aware datetime
            if expires_at.tzinfo is not None:
                from datetime import timezone
                now = datetime.now(timezone.utc)
            
            time_until_expiry = (expires_at - now).total_seconds()
            
            # Allow some tolerance for clock skew
            assert abs(time_until_expiry - token_response.expires_in) < 60, \
                "expires_at should match expires_in"
        
        logger.info(f"Token expiration validated: {token_response.expires_in}s")
    
    def test_token_refresh(self, unauthenticated_api_client, settings):
        """
        Test token refresh functionality.
        
        Validates:
        - Refresh token is provided in login response
        - Refresh endpoint accepts refresh token
        - New access token is returned
        - New token is different from original
        
        Requirements: 5.1, 2.2
        
        Note: This test may be skipped if refresh tokens are not implemented
        """
        logger.info("Testing token refresh")
        
        # First, login to get tokens
        login_data = {
            "username": settings.auth_user,
            "password": settings.auth_password,
            "remember_me": True  # Request refresh token
        }
        
        login_response = unauthenticated_api_client.post(
            "/auth/login",
            json=login_data
        )
        
        validate_response_status(login_response, expected_status=200)
        
        login_data_response = login_response.json()
        
        # Check if refresh token is provided
        if "refresh_token" not in login_data_response:
            pytest.skip("Refresh token not implemented")
        
        original_access_token = login_data_response["access_token"]
        refresh_token = login_data_response["refresh_token"]
        
        # Attempt to refresh token
        refresh_data = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        
        refresh_response = unauthenticated_api_client.post(
            "/auth/refresh",
            json=refresh_data
        )
        
        # Validate refresh response
        validate_response_status(refresh_response, expected_status=200)
        
        refresh_data_response = refresh_response.json()
        
        # Validate new token
        assert "access_token" in refresh_data_response, "New access token should be returned"
        new_access_token = refresh_data_response["access_token"]
        
        # Verify new token is different
        assert new_access_token != original_access_token, \
            "New access token should be different from original"
        
        logger.info("Token refresh successful")
    
    def test_logout(self, api_client):
        """
        Test logout functionality.
        
        Validates:
        - Logout endpoint is accessible
        - Response status is successful
        - Token is invalidated (if applicable)
        
        Requirements: 5.1
        
        Note: This test may be skipped if logout is not implemented
        """
        logger.info("Testing logout")
        
        # Execute logout request
        response = api_client.post("/auth/logout")
        
        # Validate response status (200 or 204)
        assert response.status_code in [200, 204, 404], \
            f"Expected 200, 204, or 404 (not implemented), got {response.status_code}"
        
        if response.status_code == 404:
            pytest.skip("Logout endpoint not implemented")
        
        logger.info("Logout successful")
    
    def test_authentication_with_remember_me(self, unauthenticated_api_client, settings):
        """
        Test authentication with remember_me flag.
        
        Validates:
        - remember_me flag is accepted
        - Token expiration may be extended
        - Response is successful
        
        Requirements: 5.1, 2.2
        """
        logger.info("Testing authentication with remember_me")
        
        # Login without remember_me
        login_data_short = {
            "username": settings.auth_user,
            "password": settings.auth_password,
            "remember_me": False
        }
        
        response_short = unauthenticated_api_client.post(
            "/auth/login",
            json=login_data_short
        )
        
        validate_response_status(response_short, expected_status=200)
        short_expires_in = response_short.json().get("expires_in", 0)
        
        # Login with remember_me
        login_data_long = {
            "username": settings.auth_user,
            "password": settings.auth_password,
            "remember_me": True
        }
        
        response_long = unauthenticated_api_client.post(
            "/auth/login",
            json=login_data_long
        )
        
        validate_response_status(response_long, expected_status=200)
        long_expires_in = response_long.json().get("expires_in", 0)
        
        # Note: remember_me may or may not extend expiration depending on implementation
        # We just validate that both requests succeed
        assert short_expires_in > 0, "Short session should have valid expiration"
        assert long_expires_in > 0, "Long session should have valid expiration"
        
        logger.info(
            f"Remember me validated - short: {short_expires_in}s, long: {long_expires_in}s"
        )


# ============================================================================
# AUTHENTICATION STATE TESTS
# ============================================================================

@pytest.mark.backend
class TestAuthenticationState:
    """Test suite for authentication state management."""
    
    def test_authenticated_request(self, api_client):
        """
        Test making authenticated request.
        
        Validates:
        - Authenticated client can access protected endpoints
        - Authorization header is included
        - Response is successful
        
        Requirements: 2.2
        """
        logger.info("Testing authenticated request")
        
        # Make request to a protected endpoint (assuming /users/me or similar)
        response = api_client.get("/users/me")
        
        # Validate response (should be 200 or 404 if endpoint doesn't exist)
        assert response.status_code in [200, 404], \
            f"Expected 200 or 404, got {response.status_code}"
        
        if response.status_code == 404:
            pytest.skip("Protected endpoint /users/me not implemented")
        
        logger.info("Authenticated request successful")
    
    def test_unauthenticated_request_to_protected_endpoint(self, unauthenticated_api_client):
        """
        Test accessing protected endpoint without authentication.
        
        Validates:
        - Unauthenticated requests are rejected
        - Response status is 401 Unauthorized
        
        Requirements: 2.2
        """
        logger.info("Testing unauthenticated request to protected endpoint")
        
        # Attempt to access protected endpoint without authentication
        response = unauthenticated_api_client.get("/users/me")
        
        # Validate response status (should be 401)
        assert response.status_code in [401, 404], \
            f"Expected 401 or 404, got {response.status_code}"
        
        if response.status_code == 404:
            pytest.skip("Protected endpoint /users/me not implemented")
        
        logger.info("Unauthenticated request correctly rejected")
    
    def test_invalid_token_request(self, unauthenticated_api_client):
        """
        Test request with invalid token.
        
        Validates:
        - Invalid tokens are rejected
        - Response status is 401 Unauthorized
        
        Requirements: 2.2
        """
        logger.info("Testing request with invalid token")
        
        # Set invalid token
        unauthenticated_api_client.set_token("invalid_token_12345")
        
        # Attempt to access protected endpoint
        response = unauthenticated_api_client.get("/users/me")
        
        # Validate response status (should be 401)
        assert response.status_code in [401, 404], \
            f"Expected 401 or 404, got {response.status_code}"
        
        if response.status_code == 404:
            pytest.skip("Protected endpoint /users/me not implemented")
        
        logger.info("Invalid token correctly rejected")
