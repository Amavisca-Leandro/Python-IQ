"""
User management Pydantic models.

This module provides data models for user-related operations including
creation, updates, and responses with comprehensive validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    
    Validates all required fields including email format and password strength.
    """
    
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username for the user"
    )
    email: EmailStr = Field(
        ...,
        description="Valid email address"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password with minimum 8 characters"
    )
    full_name: Optional[str] = Field(
        None,
        max_length=100,
        description="User's full name"
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="User's phone number"
    )
    is_active: bool = Field(
        default=True,
        description="Whether the user account is active"
    )
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """
        Validate username format.
        
        Rules:
        - Must contain only alphanumeric characters, underscores, and hyphens
        - Cannot start or end with special characters
        
        Args:
            v: Username to validate
            
        Returns:
            str: Validated username
            
        Raises:
            ValueError: If username format is invalid
        """
        if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_-]*[a-zA-Z0-9]$', v) and len(v) > 1:
            raise ValueError(
                "Username must contain only alphanumeric characters, underscores, "
                "and hyphens, and cannot start or end with special characters"
            )
        if len(v) == 1 and not v.isalnum():
            raise ValueError("Single character username must be alphanumeric")
        return v
    
    @field_validator("password")
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
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate phone number format (Brazilian format).
        
        Accepts formats:
        - (11) 98765-4321
        - 11987654321
        - +5511987654321
        
        Args:
            v: Phone number to validate
            
        Returns:
            Optional[str]: Validated phone number
            
        Raises:
            ValueError: If phone format is invalid
        """
        if v is None:
            return v
        
        # Remove common formatting characters
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        
        # Check if it matches Brazilian phone patterns
        if not re.match(r'^(\+55)?[1-9]{2}9?\d{8}$', cleaned):
            raise ValueError(
                "Phone must be a valid Brazilian phone number "
                "(e.g., (11) 98765-4321 or +5511987654321)"
            )
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "john_doe",
                    "email": "john.doe@example.com",
                    "password": "SecurePass123!",
                    "full_name": "John Doe",
                    "phone": "(11) 98765-4321",
                    "is_active": True
                }
            ]
        }
    }


class UserResponse(BaseModel):
    """
    Schema for user response data.
    
    Represents user data returned from API endpoints.
    Does not include sensitive information like passwords.
    """
    
    id: int = Field(
        ...,
        description="Unique user identifier"
    )
    username: str = Field(
        ...,
        description="Username"
    )
    email: EmailStr = Field(
        ...,
        description="Email address"
    )
    full_name: Optional[str] = Field(
        None,
        description="User's full name"
    )
    phone: Optional[str] = Field(
        None,
        description="User's phone number"
    )
    is_active: bool = Field(
        default=True,
        description="Whether the user account is active"
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when user was created"
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Timestamp when user was last updated"
    )
    
    model_config = {
        "from_attributes": True,  # Enable ORM mode for SQLAlchemy compatibility
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "username": "john_doe",
                    "email": "john.doe@example.com",
                    "full_name": "John Doe",
                    "phone": "(11) 98765-4321",
                    "is_active": True,
                    "created_at": "2024-01-15T10:30:00Z",
                    "updated_at": "2024-01-20T14:45:00Z"
                }
            ]
        }
    }


class UserUpdate(BaseModel):
    """
    Schema for updating user data.
    
    All fields are optional to support partial updates.
    """
    
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        description="Updated username"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Updated email address"
    )
    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=128,
        description="Updated password"
    )
    full_name: Optional[str] = Field(
        None,
        max_length=100,
        description="Updated full name"
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Updated phone number"
    )
    is_active: Optional[bool] = Field(
        None,
        description="Updated active status"
    )
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        """Validate username format if provided."""
        if v is None:
            return v
        
        if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_-]*[a-zA-Z0-9]$', v) and len(v) > 1:
            raise ValueError(
                "Username must contain only alphanumeric characters, underscores, "
                "and hyphens, and cannot start or end with special characters"
            )
        if len(v) == 1 and not v.isalnum():
            raise ValueError("Single character username must be alphanumeric")
        return v
    
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: Optional[str]) -> Optional[str]:
        """Validate password strength if provided."""
        if v is None:
            return v
        
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character")
        return v
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format if provided."""
        if v is None:
            return v
        
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        
        if not re.match(r'^(\+55)?[1-9]{2}9?\d{8}$', cleaned):
            raise ValueError(
                "Phone must be a valid Brazilian phone number "
                "(e.g., (11) 98765-4321 or +5511987654321)"
            )
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "full_name": "John Updated Doe",
                    "phone": "(11) 91234-5678",
                    "is_active": False
                }
            ]
        }
    }


class UserList(BaseModel):
    """
    Schema for paginated user list response.
    
    Provides pagination metadata along with user data.
    """
    
    users: list[UserResponse] = Field(
        ...,
        description="List of users"
    )
    total: int = Field(
        ...,
        ge=0,
        description="Total number of users"
    )
    page: int = Field(
        default=1,
        ge=1,
        description="Current page number"
    )
    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of items per page"
    )
    total_pages: int = Field(
        ...,
        ge=0,
        description="Total number of pages"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "users": [
                        {
                            "id": 1,
                            "username": "john_doe",
                            "email": "john.doe@example.com",
                            "full_name": "John Doe",
                            "phone": "(11) 98765-4321",
                            "is_active": True,
                            "created_at": "2024-01-15T10:30:00Z",
                            "updated_at": None
                        }
                    ],
                    "total": 1,
                    "page": 1,
                    "page_size": 10,
                    "total_pages": 1
                }
            ]
        }
    }
