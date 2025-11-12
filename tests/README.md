# Test Fixtures Documentation

This document describes the global pytest fixtures available for test automation.

## Overview

The `conftest.py` file provides a comprehensive set of fixtures for:
- Configuration management
- API client with authentication
- Database connectivity and session management
- Test data factory with automatic cleanup
- Test data context for isolation

## Configuration Fixtures

### `settings`

**Scope:** session

Provides shared settings instance loaded from environment variables and `.env` file.

```python
def test_example(settings):
    assert settings.api_base_url.startswith("http")
    assert settings.env in ["dev", "staging", "prod"]
```

## API Client Fixtures

### `api_client_session`

**Scope:** session

Provides a reusable API client for the entire test session. Connection pooling is enabled for performance.

```python
def test_api_health(api_client_session):
    response = api_client_session.get("/health")
    assert response.status_code == 200
```

### `api_client`

**Scope:** function

Provides an authenticated API client with automatic authentication before each test.

```python
def test_get_user_profile(api_client):
    response = api_client.get("/users/me")
    assert response.status_code == 200
    assert response.json()['email'] is not None
```

### `unauthenticated_api_client`

**Scope:** function

Provides an unauthenticated API client for testing authentication endpoints.

```python
def test_login(unauthenticated_api_client):
    response = unauthenticated_api_client.post(
        "/auth/login",
        json={"username": "test", "password": "pass"}
    )
    assert response.status_code == 200
```

## Database Fixtures

### `db_manager`

**Scope:** session

Provides database manager with connection pooling for the entire test session.

```python
@pytest.mark.database
def test_database_query(db_manager):
    with db_manager.get_session() as session:
        result = session.execute(text("SELECT 1"))
        assert result.scalar() == 1
```

### `db_session`

**Scope:** function

Provides a database session with automatic transaction management. Changes are committed on success and rolled back on failure.

```python
@pytest.mark.database
def test_create_user(db_session):
    user = User(username="test", email="test@example.com")
    db_session.add(user)
    db_session.flush()
    assert user.id is not None
    # Automatically committed or rolled back
```

## Test Data Factory Fixtures

### `test_data_factory`

**Scope:** session

Provides test data factory for creating realistic test data using Faker.

```python
def test_user_data_generation(test_data_factory):
    user_data = test_data_factory.create_user_data(
        test_id="test_123",
        email="custom@example.com"
    )
    assert user_data['email'] == "custom@example.com"
    assert user_data['username'] is not None
```

## Test Data Context Fixtures

### `test_data_context`

**Scope:** function

Provides test data context with unique test_id and automatic cleanup. Ensures test isolation in parallel execution.

```python
def test_with_cleanup(test_data_context, test_data_factory):
    # Create test data
    user_data = test_data_factory.create_user_data(
        test_id=test_data_context.test_id
    )
    
    # Register entities for cleanup
    test_data_context.register_entity('User', user_data['id'])
    
    # Test logic here
    
    # Cleanup happens automatically after test
```

### `isolated_test_data`

**Scope:** function

Combines test data context with database session for tests that need both.

```python
@pytest.mark.database
def test_user_in_database(isolated_test_data):
    context, session = isolated_test_data
    
    # Create user in database
    user = User(
        username=f"test_{context.test_id}",
        email=f"{context.test_id}@example.com"
    )
    session.add(user)
    session.flush()
    
    # Register for cleanup
    context.register_entity('User', user.id)
    
    # Verify user exists
    assert user.id is not None
```

## Pytest Hooks

### Custom Markers

The following markers are automatically registered:

- `@pytest.mark.smoke` - Smoke tests
- `@pytest.mark.regression` - Regression tests
- `@pytest.mark.backend` - Backend/API tests
- `@pytest.mark.frontend` - Frontend/UI tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow running tests
- `@pytest.mark.database` - Tests requiring database

### Auto-marking

Tests are automatically marked based on their location:
- Tests in `tests/backend/` get `@pytest.mark.backend`
- Tests in `tests/frontend/` get `@pytest.mark.frontend`
- Tests in `tests/integration/` get `@pytest.mark.integration`
- Tests using `db_manager` or `db_session` get `@pytest.mark.database`

## Usage Examples

### Simple API Test

```python
def test_api_endpoint(api_client):
    response = api_client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### Test with Database

```python
@pytest.mark.database
def test_user_creation(db_session, test_data_context):
    user = User(
        username=f"test_{test_data_context.test_id}",
        email=f"{test_data_context.test_id}@example.com",
        password="SecurePass123!"
    )
    db_session.add(user)
    db_session.flush()
    
    assert user.id is not None
    assert user.username.startswith("test_")
```

### End-to-End Test

```python
@pytest.mark.integration
def test_complete_user_workflow(
    api_client,
    db_manager,
    test_data_factory,
    test_data_context
):
    # 1. Create test data
    user_data = test_data_factory.create_user_data(
        test_id=test_data_context.test_id
    )
    
    # 2. Create user via API
    response = api_client.post("/users", json=user_data)
    assert response.status_code == 201
    user_id = response.json()['id']
    
    # 3. Verify in database
    with db_manager.get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        assert user is not None
        assert user.email == user_data['email']
    
    # 4. Cleanup happens automatically
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific marker
```bash
pytest -m smoke
pytest -m "backend and not slow"
```

### Run with parallel execution
```bash
pytest -n auto
```

### Run without database tests
```bash
pytest -m "not database"
```

## Best Practices

1. **Use appropriate fixture scope** - Use session scope for expensive setup, function scope for test isolation
2. **Register entities for cleanup** - Always register created entities in test_data_context
3. **Use markers** - Mark tests appropriately for selective execution
4. **Leverage auto-authentication** - Use `api_client` fixture for authenticated requests
5. **Test isolation** - Each test should be independent and not rely on other tests
6. **Cleanup** - Let fixtures handle cleanup automatically via teardown

## Troubleshooting

### Database connection errors
- Ensure database is running and accessible
- Check `.env` file for correct database credentials
- Verify `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`

### Authentication failures
- Check `AUTH_USER` and `AUTH_PASSWORD` in `.env`
- Verify API endpoint is accessible
- Check if authentication endpoint is correct

### Fixture not found
- Ensure `conftest.py` is in the correct location
- Check fixture name spelling
- Verify fixture is not scoped incorrectly
