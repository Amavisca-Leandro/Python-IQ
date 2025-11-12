"""
Test script to validate Pydantic models.

This script performs basic validation of user and auth models to ensure
they work correctly with proper validation rules.
"""

from datetime import datetime
from core.models import (
    UserCreate, UserResponse, UserUpdate, UserList,
    LoginRequest, TokenResponse, RefreshTokenRequest,
    PasswordResetConfirm, PasswordChangeRequest, AuthStatus
)


def test_user_models():
    """Test user management models."""
    print("Testing User Models...")
    
    # Test UserCreate with valid data
    try:
        user_create = UserCreate(
            username="test_user",
            email="test@example.com",
            password="SecurePass123!",
            full_name="Test User",
            phone="(11) 98765-4321"
        )
        print("✓ UserCreate with valid data: PASSED")
    except Exception as e:
        print(f"✗ UserCreate with valid data: FAILED - {e}")
    
    # Test UserCreate with invalid password
    try:
        user_create = UserCreate(
            username="test_user",
            email="test@example.com",
            password="weak",  # Should fail
            full_name="Test User"
        )
        print("✗ UserCreate with weak password: FAILED - Should have raised error")
    except ValueError as e:
        print(f"✓ UserCreate with weak password: PASSED - Correctly rejected")
    
    # Test UserCreate with invalid email
    try:
        user_create = UserCreate(
            username="test_user",
            email="invalid-email",  # Should fail
            password="SecurePass123!"
        )
        print("✗ UserCreate with invalid email: FAILED - Should have raised error")
    except Exception as e:
        print(f"✓ UserCreate with invalid email: PASSED - Correctly rejected")
    
    # Test UserCreate with invalid username
    try:
        user_create = UserCreate(
            username="_invalid_",  # Should fail - starts with underscore
            email="test@example.com",
            password="SecurePass123!"
        )
        print("✗ UserCreate with invalid username: FAILED - Should have raised error")
    except ValueError as e:
        print(f"✓ UserCreate with invalid username: PASSED - Correctly rejected")
    
    # Test UserResponse
    try:
        user_response = UserResponse(
            id=1,
            username="test_user",
            email="test@example.com",
            full_name="Test User",
            phone="(11) 98765-4321",
            is_active=True,
            created_at=datetime.now()
        )
        print("✓ UserResponse: PASSED")
    except Exception as e:
        print(f"✗ UserResponse: FAILED - {e}")
    
    # Test UserUpdate with partial data
    try:
        user_update = UserUpdate(
            full_name="Updated Name",
            phone="(11) 91234-5678"
        )
        print("✓ UserUpdate with partial data: PASSED")
    except Exception as e:
        print(f"✗ UserUpdate with partial data: FAILED - {e}")
    
    # Test UserList
    try:
        user_list = UserList(
            users=[user_response],
            total=1,
            page=1,
            page_size=10,
            total_pages=1
        )
        print("✓ UserList: PASSED")
    except Exception as e:
        print(f"✗ UserList: FAILED - {e}")
    
    print()


def test_auth_models():
    """Test authentication models."""
    print("Testing Auth Models...")
    
    # Test LoginRequest with username
    try:
        login_request = LoginRequest(
            username="test_user",
            password="SecurePass123!",
            remember_me=False
        )
        print("✓ LoginRequest with username: PASSED")
    except Exception as e:
        print(f"✗ LoginRequest with username: FAILED - {e}")
    
    # Test LoginRequest with email
    try:
        login_request = LoginRequest(
            username="test@example.com",
            password="SecurePass123!",
            remember_me=True
        )
        print("✓ LoginRequest with email: PASSED")
    except Exception as e:
        print(f"✗ LoginRequest with email: FAILED - {e}")
    
    # Test TokenResponse
    try:
        token_response = TokenResponse(
            access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test",
            refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.refresh",
            token_type="Bearer",
            expires_in=3600,
            expires_at=datetime.now()
        )
        print("✓ TokenResponse: PASSED")
    except Exception as e:
        print(f"✗ TokenResponse: FAILED - {e}")
    
    # Test RefreshTokenRequest
    try:
        refresh_request = RefreshTokenRequest(
            refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.refresh"
        )
        print("✓ RefreshTokenRequest: PASSED")
    except Exception as e:
        print(f"✗ RefreshTokenRequest: FAILED - {e}")
    
    # Test PasswordResetConfirm with matching passwords
    try:
        reset_confirm = PasswordResetConfirm(
            token="reset_token_123",
            new_password="NewSecurePass123!",
            confirm_password="NewSecurePass123!"
        )
        print("✓ PasswordResetConfirm with matching passwords: PASSED")
    except Exception as e:
        print(f"✗ PasswordResetConfirm with matching passwords: FAILED - {e}")
    
    # Test PasswordResetConfirm with non-matching passwords
    try:
        reset_confirm = PasswordResetConfirm(
            token="reset_token_123",
            new_password="NewSecurePass123!",
            confirm_password="DifferentPass123!"  # Should fail
        )
        print("✗ PasswordResetConfirm with non-matching passwords: FAILED - Should have raised error")
    except ValueError as e:
        print(f"✓ PasswordResetConfirm with non-matching passwords: PASSED - Correctly rejected")
    
    # Test PasswordChangeRequest
    try:
        password_change = PasswordChangeRequest(
            current_password="OldSecurePass123!",
            new_password="NewSecurePass123!",
            confirm_password="NewSecurePass123!"
        )
        print("✓ PasswordChangeRequest: PASSED")
    except Exception as e:
        print(f"✗ PasswordChangeRequest: FAILED - {e}")
    
    # Test AuthStatus
    try:
        auth_status = AuthStatus(
            authenticated=True,
            user_id=1,
            username="test_user",
            token_expires_at=datetime.now(),
            permissions=["read", "write"]
        )
        print("✓ AuthStatus: PASSED")
    except Exception as e:
        print(f"✗ AuthStatus: FAILED - {e}")
    
    print()


def test_serialization():
    """Test model serialization and deserialization."""
    print("Testing Serialization...")
    
    # Test JSON serialization
    try:
        user_create = UserCreate(
            username="test_user",
            email="test@example.com",
            password="SecurePass123!",
            full_name="Test User"
        )
        
        # Serialize to dict
        user_dict = user_create.model_dump()
        assert isinstance(user_dict, dict)
        assert user_dict["username"] == "test_user"
        
        # Serialize to JSON
        user_json = user_create.model_dump_json()
        assert isinstance(user_json, str)
        
        print("✓ Model serialization: PASSED")
    except Exception as e:
        print(f"✗ Model serialization: FAILED - {e}")
    
    # Test JSON deserialization
    try:
        user_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "SecurePass123!",
            "full_name": "Test User"
        }
        user_create = UserCreate(**user_data)
        assert user_create.username == "test_user"
        
        print("✓ Model deserialization: PASSED")
    except Exception as e:
        print(f"✗ Model deserialization: FAILED - {e}")
    
    print()


def main():
    """Run all model tests."""
    print("=" * 60)
    print("Pydantic Models Validation Test")
    print("=" * 60)
    print()
    
    test_user_models()
    test_auth_models()
    test_serialization()
    
    print("=" * 60)
    print("Test completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
