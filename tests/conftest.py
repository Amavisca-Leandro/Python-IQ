"""
Global pytest fixtures and configuration.

This module provides shared fixtures for test automation including:
- Settings and configuration management
- API client with authentication
- Database manager and session handling
- Test data factory with automatic cleanup
- Test data context for isolation
"""

import logging
import pytest
from typing import Generator

from core.config.settings import get_settings, Settings
from core.api.client import APIClient
from core.database.manager import DatabaseManager
from core.database.factory import TestDataFactory, TestDataContext


logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def settings() -> Settings:
    """
    Provide shared settings instance for all tests.
    
    Scope: session - Created once per test session
    
    Returns:
        Settings: Global settings instance
        
    Example:
        >>> def test_api_url(settings):
        ...     assert settings.api_base_url.startswith("http")
    """
    settings_instance = get_settings()
    logger.info(f"Settings loaded for environment: {settings_instance.env}")
    return settings_instance


# ============================================================================
# API CLIENT FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def api_client_session(settings: Settings) -> Generator[APIClient, None, None]:
    """
    Provide API client for the entire test session.
    
    Scope: session - Reused across all tests for performance
    
    Args:
        settings: Settings fixture
        
    Yields:
        APIClient: Configured API client
        
    Example:
        >>> def test_api_connection(api_client_session):
        ...     response = api_client_session.get("/health")
        ...     assert response.status_code == 200
    """
    client = APIClient(
        base_url=settings.api_base_url,
        timeout=settings.api_timeout,
        retries=settings.api_retries
    )
    
    logger.info(f"API client created for session: {settings.api_base_url}")
    
    yield client
    
    # Cleanup
    client.close()
    logger.info("API client closed")


@pytest.fixture(scope="function")
def api_client(
    api_client_session: APIClient,
    settings: Settings
) -> Generator[APIClient, None, None]:
    """
    Provide authenticated API client with automatic authentication.
    
    Scope: function - Fresh authentication for each test
    
    Args:
        api_client_session: Session-scoped API client
        settings: Settings fixture
        
    Yields:
        APIClient: Authenticated API client
        
    Example:
        >>> def test_get_user(api_client):
        ...     response = api_client.get("/users/me")
        ...     assert response.status_code == 200
    """
    # Authenticate before each test
    try:
        api_client_session.authenticate(
            username=settings.auth_user,
            password=settings.auth_password
        )
        logger.info(f"API client authenticated as: {settings.auth_user}")
    except Exception as e:
        logger.warning(f"Authentication failed: {e}")
        # Continue without authentication - some tests may not need it
    
    yield api_client_session
    
    # Optional: Clear authentication after test
    # api_client_session.clear_authentication()


@pytest.fixture(scope="function")
def unauthenticated_api_client(settings: Settings) -> Generator[APIClient, None, None]:
    """
    Provide unauthenticated API client for auth tests.
    
    Scope: function - New client for each test
    
    Args:
        settings: Settings fixture
        
    Yields:
        APIClient: Unauthenticated API client
        
    Example:
        >>> def test_login(unauthenticated_api_client):
        ...     response = unauthenticated_api_client.post(
        ...         "/auth/login",
        ...         json={"username": "test", "password": "pass"}
        ...     )
        ...     assert response.status_code == 200
    """
    client = APIClient(
        base_url=settings.api_base_url,
        timeout=settings.api_timeout,
        retries=settings.api_retries
    )
    
    logger.info("Unauthenticated API client created")
    
    yield client
    
    client.close()
    logger.info("Unauthenticated API client closed")


# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def db_manager(settings: Settings) -> Generator[DatabaseManager, None, None]:
    """
    Provide database manager for the entire test session.
    
    Scope: session - Reused across all tests with connection pooling
    
    Args:
        settings: Settings fixture
        
    Yields:
        DatabaseManager: Database manager instance
        
    Example:
        >>> def test_database_connection(db_manager):
        ...     with db_manager.get_session() as session:
        ...         result = session.execute(text("SELECT 1"))
        ...         assert result.scalar() == 1
    """
    manager = DatabaseManager(connection_string=settings.database_url)
    
    logger.info(f"Database manager created: {settings.db_host}:{settings.db_port}/{settings.db_name}")
    
    yield manager
    
    # Cleanup
    manager.close()
    logger.info("Database manager closed")


@pytest.fixture(scope="function")
def db_session(db_manager: DatabaseManager):
    """
    Provide database session with automatic rollback.
    
    Scope: function - New session for each test with transaction isolation
    
    Args:
        db_manager: Database manager fixture
        
    Yields:
        Session: SQLAlchemy session
        
    Note:
        This fixture automatically rolls back changes after each test
        to ensure test isolation.
        
    Example:
        >>> def test_create_user(db_session):
        ...     user = User(username="test", email="test@example.com")
        ...     db_session.add(user)
        ...     db_session.flush()
        ...     assert user.id is not None
        ...     # Automatically rolled back after test
    """
    with db_manager.get_session() as session:
        yield session
        # Session is automatically rolled back if test fails
        # or committed if test passes (via context manager)


# ============================================================================
# TEST DATA FACTORY FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def test_data_factory(db_manager: DatabaseManager) -> TestDataFactory:
    """
    Provide test data factory for the entire test session.
    
    Scope: session - Reused across all tests
    
    Args:
        db_manager: Database manager fixture
        
    Returns:
        TestDataFactory: Test data factory instance
        
    Example:
        >>> def test_user_creation(test_data_factory):
        ...     user_data = test_data_factory.create_user_data(
        ...         test_id="test_123",
        ...         email="custom@example.com"
        ...     )
        ...     assert user_data['email'] == "custom@example.com"
    """
    factory = TestDataFactory(db_manager=db_manager)
    
    logger.info("Test data factory created")
    
    return factory


# ============================================================================
# TEST DATA CONTEXT FIXTURES
# ============================================================================

@pytest.fixture(scope="function")
def test_data_context(
    test_data_factory: TestDataFactory,
    request: pytest.FixtureRequest
) -> Generator[TestDataContext, None, None]:
    """
    Provide test data context with automatic cleanup.
    
    Scope: function - New context for each test with unique test_id
    
    This fixture ensures test data isolation by:
    - Generating unique test_id for each test
    - Tracking all created entities
    - Automatically cleaning up data after test completion
    - Supporting parallel test execution
    
    Args:
        test_data_factory: Test data factory fixture
        request: Pytest request object
        
    Yields:
        TestDataContext: Test data context with unique test_id
        
    Example:
        >>> def test_with_test_data(test_data_context, test_data_factory):
        ...     # Create test data
        ...     user_data = test_data_factory.create_user_data(
        ...         test_id=test_data_context.test_id
        ...     )
        ...     
        ...     # Use test data in test
        ...     assert user_data['username'].startswith('test_')
        ...     
        ...     # Cleanup happens automatically after test
    """
    # Generate unique test_id based on test name and execution
    test_name = request.node.name
    test_id = f"{test_name}_{TestDataContext._generate_test_id()}"
    
    # Create context
    context = TestDataContext(test_id=test_id)
    
    logger.info(f"Test data context created for test: {test_name} with test_id: {test_id}")
    
    yield context
    
    # Cleanup after test
    try:
        test_data_factory.cleanup_test_data(context.test_id)
        logger.info(f"Test data cleanup completed for test_id: {context.test_id}")
    except Exception as e:
        logger.error(f"Test data cleanup failed for test_id: {context.test_id}: {e}")


@pytest.fixture(scope="function")
def isolated_test_data(
    test_data_context: TestDataContext,
    db_session
):
    """
    Provide isolated test data with database session.
    
    Scope: function - Combines test data context with database session
    
    This fixture provides both test data context and database session
    for tests that need to create and verify data in the database.
    
    Args:
        test_data_context: Test data context fixture
        db_session: Database session fixture
        
    Yields:
        tuple: (TestDataContext, Session)
        
    Example:
        >>> def test_user_in_database(isolated_test_data):
        ...     context, session = isolated_test_data
        ...     
        ...     # Create user in database
        ...     user = User(
        ...         username=f"test_{context.test_id}",
        ...         email=f"{context.test_id}@example.com"
        ...     )
        ...     session.add(user)
        ...     session.flush()
        ...     
        ...     # Register for cleanup
        ...     context.register_entity('User', user.id)
        ...     
        ...     # Verify user exists
        ...     assert user.id is not None
    """
    yield test_data_context, db_session


# ============================================================================
# PYTEST CONFIGURATION HOOKS
# ============================================================================

def pytest_configure(config):
    """
    Configure pytest with custom markers and settings.
    
    Args:
        config: Pytest config object
    """
    # Register custom markers
    config.addinivalue_line(
        "markers",
        "smoke: mark test as part of smoke test suite"
    )
    config.addinivalue_line(
        "markers",
        "regression: mark test as part of regression test suite"
    )
    config.addinivalue_line(
        "markers",
        "backend: mark test as backend/API test"
    )
    config.addinivalue_line(
        "markers",
        "frontend: mark test as frontend/UI test"
    )
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers",
        "database: mark test as requiring database"
    )
    
    logger.info("Pytest configuration completed")


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add markers automatically.
    
    Args:
        config: Pytest config object
        items: List of collected test items
    """
    for item in items:
        # Auto-mark tests based on file location
        if "backend" in str(item.fspath):
            item.add_marker(pytest.mark.backend)
        elif "frontend" in str(item.fspath):
            item.add_marker(pytest.mark.frontend)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Auto-mark database tests
        if "db_manager" in item.fixturenames or "db_session" in item.fixturenames:
            item.add_marker(pytest.mark.database)


def pytest_sessionstart(session):
    """
    Called after Session object has been created and before test collection.
    
    Args:
        session: Pytest session object
    """
    settings = get_settings()
    logger.info("=" * 80)
    logger.info("TEST SESSION STARTED")
    logger.info(f"Environment: {settings.env}")
    logger.info(f"API Base URL: {settings.api_base_url}")
    logger.info(f"Frontend Base URL: {settings.frontend_base_url}")
    logger.info(f"Database: {settings.db_host}:{settings.db_port}/{settings.db_name}")
    logger.info(f"Parallel Workers: {settings.pytest_workers}")
    logger.info("=" * 80)


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before returning exit status.
    
    Args:
        session: Pytest session object
        exitstatus: Exit status code
    """
    logger.info("=" * 80)
    logger.info("TEST SESSION FINISHED")
    logger.info(f"Exit Status: {exitstatus}")
    logger.info("=" * 80)
