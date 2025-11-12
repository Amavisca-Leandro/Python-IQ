"""
Pydantic data models.

This package provides comprehensive data models for the test automation framework
including user management, authentication, and validation schemas.
"""

from core.models.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserList,
)

from core.models.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    LogoutRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    PasswordChangeRequest,
    AuthStatus,
)

__all__ = [
    # User models
    "UserCreate",
    "UserResponse",
    "UserUpdate",
    "UserList",
    # Auth models
    "LoginRequest",
    "TokenResponse",
    "RefreshTokenRequest",
    "LogoutRequest",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    "PasswordChangeRequest",
    "AuthStatus",
]
