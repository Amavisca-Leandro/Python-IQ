# Pydantic Data Models

This package provides comprehensive Pydantic data models for the test automation framework, including user management and authentication schemas with built-in validation.

## Overview

The models are organized into two main modules:
- `user.py` - User management models (create, update, response, list)
- `auth.py` - Authentication models (login, tokens, password management)

## Features

- **Type Safety**: Full type hints and runtime validation
- **Comprehensive Validation**: Email, password strength, phone numbers (Brazilian format)
- **Serialization**: JSON serialization/deserialization support
- **ORM Compatibility**: Compatible with SQLAlchemy models via `from_attributes=True`
- **Documentation**: Rich examples and field descriptions

## User Models

### UserCreate

Schema for creating new users with comprehensive validation.

```python
from core.models import UserCreate

user = UserCreate(
    username="john_doe",
    email="john.doe@example.com",
    password="SecurePass123!",
    full_name="John Doe",
    phone="(11) 98765-4321",
    is_active=True
)
```

**Validations:**
- Username: 3-50 chars, alphanumeric with underscores/hyphens
- Email: Valid email format
- Password: Min 8 chars, must contain uppercase, lowercase, digit, and special character
- Phone: Brazilian phone format (optional)

### UserResponse

Schema for user data returned from API endpoints (excludes sensitive data).

```python
from core.models import UserResponse
from datetime import datetime

user_response = UserResponse(
    id=1,
    username="john_doe",
    email="john.doe@example.com",
    full_name="John Doe",
    phone="(11) 98765-4321",
    is_active=True,
    created_at=datetime.now(),
    updated_at=None
)
```

### UserUpdate

Schema for partial user updates (all fields optional).

```python
from core.models import UserUpdate

user_update = UserUpdate(
    full_name="John Updated Doe",
    phone="(11) 91234-5678"
)
```

### UserList

Schema for paginated user list responses.

```python
from core.models import UserList, UserResponse

user_list = UserList(
    users=[user_response],
    total=100,
    page=1,
    page_size=10,
    total_pages=10
)
```

## Authentication Models

### LoginRequest

Schema for user login with username/email and password.

```python
from core.models import LoginRequest

# Login with username
login = LoginRequest(
    username="john_doe",
    password="SecurePass123!",
    remember_me=False
)

# Login with email
login = LoginRequest(
    username="john.doe@example.com",
    password="SecurePass123!",
    remember_me=True
)
```

### TokenResponse

Schema for authentication token responses.

```python
from core.models import TokenResponse
from datetime import datetime

token = TokenResponse(
    access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    token_type="Bearer",
    expires_in=3600,
    expires_at=datetime.now(),
    scope="read write"
)
```

### RefreshTokenRequest

Schema for refreshing access tokens.

```python
from core.models import RefreshTokenRequest

refresh = RefreshTokenRequest(
    refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
)
```

### PasswordResetConfirm

Schema for confirming password reset with token.

```python
from core.models import PasswordResetConfirm

reset = PasswordResetConfirm(
    token="reset_token_123",
    new_password="NewSecurePass123!",
    confirm_password="NewSecurePass123!"
)
```

**Validations:**
- Passwords must match
- Password strength requirements enforced

### PasswordChangeRequest

Schema for authenticated users changing their password.

```python
from core.models import PasswordChangeRequest

change = PasswordChangeRequest(
    current_password="OldSecurePass123!",
    new_password="NewSecurePass123!",
    confirm_password="NewSecurePass123!"
)
```

**Validations:**
- Passwords must match
- New password must differ from current
- Password strength requirements enforced

### AuthStatus

Schema for authentication status responses.

```python
from core.models import AuthStatus
from datetime import datetime

status = AuthStatus(
    authenticated=True,
    user_id=1,
    username="john_doe",
    token_expires_at=datetime.now(),
    permissions=["read", "write", "delete"]
)
```

## Usage in Tests

### API Testing

```python
from core.models import UserCreate, UserResponse
import requests

# Create user via API
user_data = UserCreate(
    username="test_user",
    email="test@example.com",
    password="SecurePass123!"
)

response = requests.post(
    "https://api.example.com/users",
    json=user_data.model_dump()
)

# Validate response
user_response = UserResponse(**response.json())
assert user_response.username == "test_user"
```

### Data Validation

```python
from core.models import UserCreate
from pydantic import ValidationError

try:
    # This will fail validation
    user = UserCreate(
        username="test",
        email="invalid-email",
        password="weak"
    )
except ValidationError as e:
    print(e.errors())
    # [
    #   {'loc': ('email',), 'msg': 'value is not a valid email address', ...},
    #   {'loc': ('password',), 'msg': 'Password must contain...', ...}
    # ]
```

### Serialization

```python
from core.models import UserCreate

user = UserCreate(
    username="test_user",
    email="test@example.com",
    password="SecurePass123!"
)

# To dict
user_dict = user.model_dump()

# To JSON string
user_json = user.model_dump_json()

# From dict
user_from_dict = UserCreate(**user_dict)

# From JSON string
import json
user_from_json = UserCreate(**json.loads(user_json))
```

## Validation Rules

### Username
- Length: 3-50 characters
- Format: Alphanumeric with underscores and hyphens
- Cannot start or end with special characters

### Email
- Must be valid email format
- Uses `EmailStr` from Pydantic for validation

### Password
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character (!@#$%^&*(),.?":{}|<>)

### Phone (Brazilian Format)
- Accepts: (11) 98765-4321, 11987654321, +5511987654321
- Validates Brazilian phone number patterns

## Testing

Run the validation test script:

```bash
python scripts/test_models.py
```

This will validate:
- All model creation with valid data
- Validation rejection of invalid data
- Serialization/deserialization
- Field validators

## Integration with SQLAlchemy

Models are compatible with SQLAlchemy ORM via `from_attributes=True`:

```python
from core.models import UserResponse
from core.database.models import User  # SQLAlchemy model

# Convert SQLAlchemy model to Pydantic
db_user = session.query(User).first()
user_response = UserResponse.from_orm(db_user)
```

## Best Practices

1. **Always validate input data** using these models before API calls
2. **Use UserResponse** for API responses to exclude sensitive data
3. **Use UserUpdate** for partial updates to avoid requiring all fields
4. **Handle ValidationError** appropriately in tests
5. **Leverage type hints** for better IDE support and type checking

## Requirements

- Python 3.11+
- pydantic >= 2.5.3
- pydantic-settings >= 2.1.0
- email-validator >= 2.1.0

## Related Documentation

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [API Client](../api/README.md)
- [Database Models](../database/README.md)
