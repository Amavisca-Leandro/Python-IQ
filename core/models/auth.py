"""
Authentication Pydantic models.

This module provides data models for authentication operations including
login, token management, and refresh flows with comprehensive validation.
"""

from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class LoginRequest(BaseModel):
    """
    Schema for user login request.
    
    Supports both username/email and password authentication.
    """
    
    username: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Username or email address"
    )
    password: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="User password"
    )
    remember_me: bool = Field(
        default=False,
        description="Whether to extend token expiration"
    )
    
    @field_validator("username")
    @classmethod
    def validate_username_or_email(cls, v: str) -> str:
        """
        Validate that username is either a valid username or email format.
        
        Args:
            v: Username or email to validate
            
        Returns:
            str: Validated username/email
            
        Raises:
            ValueError: If format is invalid
        """
        # Check if it's an email
        if '@' in v:
            # Basic email validation
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
                raise ValueError("Invalid email format")
        else:
            # Username validation
            if not re.match(r'^[a-zA-Z0-9_-]+$', v):
                raise ValueError(
                    "Username must contain only alphanumeric characters, "
                    "underscores, and hyphens"
                )
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "john_doe",
                    "password": "SecurePass123!",
                    "remember_me": False
                },
                {
                    "username": "john.doe@example.com",
                    "password": "SecurePass123!",
                    "remember_me": True
                }
            ]
        }
    }


class TokenResponse(BaseModel):
    """
    Schema for authentication token response.
    
    Contains access token, refresh token, and metadata.
    """
    
    access_token: str = Field(
        ...,
        description="JWT access token for API authentication"
    )
    refresh_token: Optional[str] = Field(
        None,
        description="JWT refresh token for obtaining new access tokens"
    )
    token_type: str = Field(
        default="Bearer",
        description="Token type (typically 'Bearer')"
    )
    expires_in: int = Field(
        ...,
        gt=0,
        description="Token expiration time in seconds"
    )
    expires_at: Optional[datetime] = Field(
        None,
        description="Absolute token expiration timestamp"
    )
    scope: Optional[str] = Field(
        None,
        description="Token scope/permissions"
    )
    
    @field_validator("token_type")
    @classmethod
    def validate_token_type(cls, v: str) -> str:
        """
        Validate and normalize token type.
        
        Args:
            v: Token type to validate
            
        Returns:
            str: Normalized token type
        """
        # Normalize to title case
        normalized = v.strip().title()
        
        # Validate against common token types
        valid_types = ["Bearer", "Basic", "Digest", "OAuth"]
        if normalized not in valid_types:
            # Allow custom types but warn via validation
            pass
        
        return normalized
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "Bearer",
                    "expires_in": 3600,
                    "expires_at": "2024-01-15T11:30:00Z",
                    "scope": "read write"
                }
            ]
        }
    }


class RefreshTokenRequest(BaseModel):
    """
    Schema for token refresh request.
    
    Used to obtain a new access token using a refresh token.
    """
    
    refresh_token: str = Field(
        ...,
        min_length=10,
        description="Valid refresh token"
    )
    grant_type: Literal["refresh_token"] = Field(
        default="refresh_token",
        description="OAuth2 grant type"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "grant_type": "refresh_token"
                }
            ]
        }
    }


class LogoutRequest(BaseModel):
    """
    Schema for user logout request.
    
    Optionally includes token to invalidate.
    """
    
    token: Optional[str] = Field(
        None,
        description="Token to invalidate (optional)"
    )
    revoke_all_tokens: bool = Field(
        default=False,
        description="Whether to revoke all user tokens"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "revoke_all_tokens": False
                }
            ]
        }
    }


class PasswordResetRequest(BaseModel):
    """
    Schema for password reset request.
    
    Initiates password reset flow by email.
    """
    
    email: EmailStr = Field(
        ...,
        description="Email address for password reset"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "john.doe@example.com"
                }
            ]
        }
    }


class PasswordResetConfirm(BaseModel):
    """
    Schema for confirming password reset.
    
    Completes password reset with token and new password.
    """
    
    token: str = Field(
        ...,
        min_length=10,
        description="Password reset token from email"
    )
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="New password"
    )
    confirm_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password confirmation"
    )
    
    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password strength.
        
        Rules:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        
        Args:
            v: Password to validate
            
        Returns:
            str: Validated password
            
        Raises:
            ValueError: If password doesn't meet strength requirements
        """
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character")
        return v
    
    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        """
        Validate that password confirmation matches new password.
        
        Args:
            v: Confirmation password
            info: Validation info containing other fields
            
        Returns:
            str: Validated confirmation password
            
        Raises:
            ValueError: If passwords don't match
        """
        if 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError("Passwords do not match")
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "token": "abc123def456ghi789",
                    "new_password": "NewSecurePass123!",
                    "confirm_password": "NewSecurePass123!"
                }
            ]
        }
    }


class PasswordChangeRequest(BaseModel):
    """
    Schema for changing password (authenticated user).
    
    Requires current password for security.
    """
    
    current_password: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="Current password for verification"
    )
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="New password"
    )
    confirm_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password confirmation"
    )
    
    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character")
        return v
    
    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        """Validate that passwords match."""
        if 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError("Passwords do not match")
        return v
    
    @field_validator("new_password")
    @classmethod
    def password_not_same_as_current(cls, v: str, info) -> str:
        """Validate that new password is different from current."""
        if 'current_password' in info.data and v == info.data['current_password']:
            raise ValueError("New password must be different from current password")
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "current_password": "OldSecurePass123!",
                    "new_password": "NewSecurePass123!",
                    "confirm_password": "NewSecurePass123!"
                }
            ]
        }
    }


class AuthStatus(BaseModel):
    """
    Schema for authentication status response.
    
    Provides information about current authentication state.
    """
    
    authenticated: bool = Field(
        ...,
        description="Whether user is authenticated"
    )
    user_id: Optional[int] = Field(
        None,
        description="Authenticated user ID"
    )
    username: Optional[str] = Field(
        None,
        description="Authenticated username"
    )
    token_expires_at: Optional[datetime] = Field(
        None,
        description="Token expiration timestamp"
    )
    permissions: Optional[list[str]] = Field(
        None,
        description="User permissions/scopes"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "authenticated": True,
                    "user_id": 1,
                    "username": "john_doe",
                    "token_expires_at": "2024-01-15T11:30:00Z",
                    "permissions": ["read", "write", "delete"]
                }
            ]
        }
    }
