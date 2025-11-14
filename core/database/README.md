# Database Integration Framework

This module provides comprehensive database integration for test automation using SQLAlchemy ORM.

## Features

- **Connection Pooling**: Optimized connection management for parallel test execution
- **ORM Models**: SQLAlchemy models with relationships and convenience methods
- **Test Data Factory**: Automated test data creation with tracking and cleanup
- **Transaction Management**: Automatic rollback on failures for test isolation
- **Brazilian Locale**: Faker integration with pt_BR locale for realistic test data

## Components

### 1. DatabaseManager

Manages database connections, sessions, and provides methods for data operations.

```python
from core.database import DatabaseManager

# Initialize (usually done via fixture)
db_manager = DatabaseManager()

# Use context manager for sessions
with db_manager.get_session() as session:
    user = session.query(User).filter(User.id == 1).first()
    print(user.username)

# Create test data using ORM
user = db_manager.create_test_data(
    User,
    {"username": "test", "email": "test@example.com", "password": "pass"}
)

# Execute raw SQL
results = db_manager.query_data(
    "SELECT * FROM users WHERE is_active = :active",
    {"active": True}
)

# Verify data exists
exists = db_manager.verify_data_exists(User, username="test")
```

### 2. SQLAlchemy Models

ORM models with relationships and convenience methods.

```python
from core.database import User, UserProfile

# User model with profile relationship
user = User(
    username="john_doe",
    email="john@example.com",
    password="SecurePass123!",
    first_name="John",
    last_name="Doe"
)

# Convenience methods
user.activate()
user.make_admin()
user_dict = user.to_dict()
full_name = user.full_name  # "John Doe"

# Profile with relationship
profile = UserProfile(
    user_id=user.id,
    full_name="John Doe",
    phone="+5511999999999",
    city="São Paulo"
)

# Access via relationship
print(user.profile.phone)
print(profile.user.email)
```

### 3. TestDataFactory

Factory pattern for creating test data with automatic tracking and cleanup.

```python
from core.database import TestDataFactory, TestDataContext

# Initialize (usually done via fixture)
factory = TestDataFactory(db_manager)

# Create simple user data (dictionary)
user_data = factory.create_user_data(
    test_id="test_123",
    email="custom@example.com"
)

# Create user with profile in database
result = factory.create_user_with_profile(
    test_id="test_123",
    email="withprofile@example.com",
    first_name="Test",
    profile={"phone": "+5511988887777", "city": "Rio de Janeiro"}
)

user = result['user']
profile = result['profile']

# Create multiple users
users = factory.create_multiple_users(
    test_id="test_123",
    count=5,
    with_profiles=True
)

# Automatic cleanup (called by fixture)
factory.cleanup_test_data("test_123")
```

## Usage in Tests

### Basic Test with Database

```python
import pytest
from core.database import User

@pytest.mark.database
def test_user_creation(db_session):
    """Test creating a user."""
    user = User(
        username="test_user",
        email="test@example.com",
        password="password"
    )
    
    db_session.add(user)
    db_session.flush()
    
    assert user.id is not None
    assert user.is_active is True
    # Automatically rolled back after test
```

### Test with Test Data Factory

```python
@pytest.mark.database
def test_with_factory(test_data_factory, test_data_context, db_manager):
    """Test using test data factory."""
    # Create user with profile
    result = test_data_factory.create_user_with_profile(
        test_id=test_data_context.test_id,
        email="factory@example.com"
    )
    
    user_id = result['user_id']
    
    # Verify in database
    assert db_manager.verify_data_exists(User, id=user_id)
    
    # Use in test
    with db_manager.get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        assert user.email == "factory@example.com"
    
    # Cleanup happens automatically via fixture
```

### End-to-End Test with Database Validation

```python
@pytest.mark.integration
def test_complete_workflow(
    api_client,
    test_data_factory,
    test_data_context,
    db_manager
):
    """Test complete workflow with database validation."""
    # 1. Create test data
    result = test_data_factory.create_user_with_profile(
        test_id=test_data_context.test_id,
        email="workflow@example.com",
        is_active=True
    )
    
    user_id = result['user_id']
    
    # 2. Verify data is ready
    with db_manager.get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        assert user is not None
        assert user.is_active is True
    
    # 3. Execute API call
    response = api_client.post(
        f"/users/{user_id}/activate",
        json={"reason": "test activation"}
    )
    assert response.status_code == 200
    
    # 4. Validate changes in database
    with db_manager.get_session() as session:
        updated_user = session.query(User).filter(User.id == user_id).first()
        assert updated_user.is_active is True
    
    # 5. Cleanup happens automatically
```

## Configuration

Database settings are managed via environment variables:

```bash
# Database Connection
DB_HOST=localhost
DB_PORT=5432
DB_NAME=test_database
DB_USER=test_user
DB_PASSWORD=test_password
DB_DRIVER=postgresql

# Connection Pool
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_PRE_PING=true
DB_POOL_RECYCLE=3600

# Test Data
FAKER_LOCALE=pt_BR
AUTO_CLEANUP_TEST_DATA=true
TEST_DATA_PREFIX=test_
ENABLE_DATA_FACTORY_TRACKING=true
```

## Available Fixtures

### Session-scoped Fixtures

- `db_manager`: DatabaseManager instance (reused across all tests)
- `test_data_factory`: TestDataFactory instance (reused across all tests)

### Function-scoped Fixtures

- `db_session`: Database session with automatic rollback
- `test_data_context`: Test data context with unique test_id and automatic cleanup
- `isolated_test_data`: Combination of test_data_context and db_session

## Best Practices

### 1. Use Test Data Context

Always use `test_data_context` fixture to ensure proper cleanup:

```python
def test_example(test_data_factory, test_data_context):
    result = test_data_factory.create_user_with_profile(
        test_id=test_data_context.test_id  # Always use context.test_id
    )
```

### 2. Verify Data Before Testing

Always verify test data is ready before executing tests:

```python
def test_with_verification(test_data_factory, test_data_context, db_manager):
    result = test_data_factory.create_user_with_profile(
        test_id=test_data_context.test_id
    )
    
    # Verify data exists
    assert db_manager.verify_data_exists(User, id=result['user_id'])
    
    # Now proceed with test
```

### 3. Use Relationships

Leverage SQLAlchemy relationships for cleaner code:

```python
# Instead of manual joins
user = session.query(User).filter(User.id == user_id).first()
profile = session.query(UserProfile).filter(UserProfile.user_id == user_id).first()

# Use relationships
user = session.query(User).filter(User.id == user_id).first()
profile = user.profile  # Cleaner!
```

### 4. Parallel Test Safety

The framework is designed for parallel execution:

- Each test gets a unique `test_id`
- Connection pooling handles concurrent connections
- Cleanup is isolated per test
- No shared state between tests

### 5. Transaction Isolation

Use `db_session` fixture for automatic rollback:

```python
def test_with_rollback(db_session):
    # Create data
    user = User(username="temp", email="temp@example.com", password="pass")
    db_session.add(user)
    db_session.flush()
    
    # Test with data
    assert user.id is not None
    
    # Automatically rolled back - no cleanup needed!
```

## Troubleshooting

### Connection Pool Exhausted

If you see "QueuePool limit exceeded", increase pool size:

```bash
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=40
```

### Foreign Key Constraint Errors

Cleanup happens in reverse order. If you add new models, update cleanup order in `TestDataFactory._cleanup_database_entities()`.

### Data Not Cleaned Up

Ensure `AUTO_CLEANUP_TEST_DATA=true` and `ENABLE_DATA_FACTORY_TRACKING=true` in your environment.

### Session Errors

Always use context managers or fixtures for sessions:

```python
# Good
with db_manager.get_session() as session:
    user = session.query(User).first()

# Good
def test_example(db_session):
    user = db_session.query(User).first()

# Bad - manual session management
session = db_manager.session_factory()
user = session.query(User).first()
session.close()  # Easy to forget!
```

## Requirements Mapping

This implementation satisfies the following requirements:

- **12.1**: Complete database integration with SQLAlchemy ORM
- **12.2**: Test data factory with mass data creation
- **12.3**: Models with relationships and validations
- **12.4**: Automatic tracking and cleanup
- **12.5**: Transaction isolation and parallel execution safety
- **12.6**: Connection pooling for performance
- **12.7**: Support for both ORM and raw SQL queries

## Examples

See `tests/integration/test_database_integration.py` for comprehensive examples.
