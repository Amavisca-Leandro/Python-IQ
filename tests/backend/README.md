# Backend API Tests

This directory contains comprehensive backend API tests for the test automation framework.

## Test Modules

### 1. test_auth.py - Authentication Tests
Tests authentication flows including login, logout, token management, and credential validation.

**Test Classes:**
- `TestAuthentication` - Core authentication functionality
  - `test_login_with_valid_credentials` - Validates successful login with proper credentials
  - `test_login_with_invalid_credentials` - Validates rejection of invalid credentials
  - `test_login_with_missing_password` - Validates validation of missing required fields
  - `test_login_with_empty_credentials` - Validates rejection of empty credentials
  - `test_login_with_email_instead_of_username` - Validates email as username support
  - `test_token_expiration_handling` - Validates token expiration information
  - `test_token_refresh` - Validates token refresh functionality
  - `test_logout` - Validates logout functionality
  - `test_authentication_with_remember_me` - Validates remember me functionality

- `TestAuthenticationState` - Authentication state management
  - `test_authenticated_request` - Validates authenticated requests work
  - `test_unauthenticated_request_to_protected_endpoint` - Validates protection of endpoints
  - `test_invalid_token_request` - Validates rejection of invalid tokens

**Requirements Covered:** 5.1, 2.2

### 2. test_users.py - User CRUD Tests
Tests user management endpoints including create, read, update, delete, and list operations.

**Test Classes:**
- `TestUserCRUD` - User CRUD operations
  - `test_create_user` - Validates user creation with Pydantic validation
  - `test_create_user_with_duplicate_username` - Validates duplicate username rejection
  - `test_create_user_with_duplicate_email` - Validates duplicate email rejection
  - `test_create_user_with_invalid_email` - Validates email format validation
  - `test_create_user_with_weak_password` - Validates password strength requirements
  - `test_get_user_by_id` - Validates user retrieval by ID
  - `test_get_user_by_invalid_id` - Validates 404 for non-existent users
  - `test_update_user` - Validates user data updates
  - `test_update_user_partial` - Validates partial updates
  - `test_delete_user` - Validates user deletion
  - `test_delete_nonexistent_user` - Validates 404 for deleting non-existent users

- `TestUserList` - User listing and pagination
  - `test_list_users` - Validates user listing
  - `test_list_users_pagination` - Validates pagination parameters
  - `test_list_users_with_filters` - Validates filtering capabilities

**Requirements Covered:** 5.2, 5.4, 3.2

### 3. test_user_integration.py - Database Integration Tests
Tests complete end-to-end workflows with database validation using both ORM and raw SQL.

**Test Classes:**
- `TestUserDatabaseIntegration` - End-to-end workflows with database
  - `test_complete_user_workflow` - Complete workflow: create data → API ops → DB validation
  - `test_user_with_profile_workflow` - User with profile relationship testing
  - `test_user_creation_via_api_with_db_validation` - API creation with DB verification
  - `test_user_deletion_cascade` - Validates cascade deletion of related data
  - `test_concurrent_user_operations` - Validates concurrent operations and isolation

**Requirements Covered:** 12.1, 12.2, 12.3

## Test Execution

### Run all backend tests:
```bash
pytest tests/backend/
```

### Run specific test module:
```bash
pytest tests/backend/test_auth.py
pytest tests/backend/test_users.py
pytest tests/backend/test_user_integration.py
```

### Run specific test class:
```bash
pytest tests/backend/test_auth.py::TestAuthentication
pytest tests/backend/test_users.py::TestUserCRUD
```

### Run specific test:
```bash
pytest tests/backend/test_auth.py::TestAuthentication::test_login_with_valid_credentials
```

### Run with markers:
```bash
# Run only smoke tests
pytest tests/backend/ -m smoke

# Run only backend tests
pytest tests/backend/ -m backend

# Run only integration tests
pytest tests/backend/ -m integration

# Run only database tests
pytest tests/backend/ -m database
```

### Run with verbose output:
```bash
pytest tests/backend/ -v
```

### Run with detailed logging:
```bash
pytest tests/backend/ -v --log-cli-level=INFO
```

## Test Features

### Pydantic Validation
All tests use Pydantic models for request/response validation:
- `UserCreate` - User creation schema
- `UserResponse` - User response schema
- `UserUpdate` - User update schema
- `LoginRequest` - Login request schema
- `TokenResponse` - Token response schema

### Automatic Cleanup
Tests use fixtures for automatic cleanup:
- `created_user_ids` - Tracks created users for cleanup
- `test_data_context` - Provides test isolation with automatic cleanup
- Database transactions with rollback support

### Data Generation
Tests use `DataGenerator` for realistic test data:
- Brazilian-specific data (CPF, phone numbers)
- Secure password generation
- Random usernames and emails
- Complete user profiles

### Database Integration
Integration tests validate:
- ORM queries (SQLAlchemy)
- Raw SQL queries
- Relationships and foreign keys
- Cascade operations
- Transaction isolation

## Test Markers

Tests are automatically marked based on:
- **@pytest.mark.smoke** - Critical path tests
- **@pytest.mark.backend** - Backend/API tests
- **@pytest.mark.integration** - Integration tests
- **@pytest.mark.database** - Tests requiring database

## Fixtures Used

### Global Fixtures (from conftest.py)
- `settings` - Configuration settings
- `api_client` - Authenticated API client
- `unauthenticated_api_client` - Unauthenticated API client
- `db_manager` - Database manager with connection pooling
- `db_session` - Database session with automatic rollback
- `test_data_factory` - Test data factory
- `test_data_context` - Test data context with cleanup

### Local Fixtures
- `test_user_data` - Sample user data for testing
- `created_user_ids` - List to track created users

## Best Practices

1. **Test Isolation**: Each test is independent and doesn't rely on other tests
2. **Cleanup**: All created data is automatically cleaned up after tests
3. **Validation**: Use Pydantic models for type-safe validation
4. **Assertions**: Clear, descriptive assertions with helpful error messages
5. **Logging**: Comprehensive logging for debugging
6. **Skip Logic**: Tests skip gracefully if endpoints are not implemented
7. **Error Handling**: Tests validate both success and error scenarios

## Requirements Traceability

| Requirement | Test Coverage |
|-------------|---------------|
| 5.1 - Authentication tests | test_auth.py (12 tests) |
| 5.2 - User CRUD operations | test_users.py (14 tests) |
| 5.4 - Pagination and filtering | test_users.py::TestUserList |
| 3.2 - Pydantic validation | All test modules |
| 2.2 - API client features | test_auth.py |
| 12.1 - Database integration | test_user_integration.py |
| 12.2 - Test data factory | test_user_integration.py |
| 12.3 - ORM and raw SQL | test_user_integration.py |

## Total Test Count

- **Authentication Tests**: 12 tests
- **User CRUD Tests**: 14 tests
- **Integration Tests**: 5 tests
- **Total**: 31 tests

## Notes

- Tests are designed to work with or without a real API backend
- Tests skip gracefully if endpoints are not implemented (404 responses)
- Database tests require a configured database connection
- All tests follow the AAA pattern (Arrange, Act, Assert)
- Tests include comprehensive validation of response structure and data
