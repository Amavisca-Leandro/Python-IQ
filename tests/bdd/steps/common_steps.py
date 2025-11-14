"""
Common step definitions for BDD tests.

This module provides reusable step definitions for common test setup and
configuration steps that are used across multiple feature files.

Steps:
- Given the API client is configured
- Given I am authenticated
- Given the database is connected and ready
"""

import allure
import logging
from pytest_bdd import given
from sqlalchemy import text

logger = logging.getLogger(__name__)

# Allure feature and story decorators for this module
allure.feature("Test Setup and Configuration")
allure.story("Common Test Preconditions")


@given("the API client is configured")
@allure.story("API Client Setup")
def api_client_configured(jsonplaceholder_client, settings):
    """
    Ensure API client is available and properly configured.
    
    This step verifies that the JSONPlaceholder API client is initialized
    and ready to use. It attaches configuration details to the Allure report
    for debugging and documentation purposes.
    
    Args:
        jsonplaceholder_client: JSONPlaceholder API client fixture
        settings: Settings fixture with configuration
        
    Raises:
        AssertionError: If the API client is not properly configured
        
    Example in feature file:
        Given the API client is configured
    """
    with allure.step("Verify API client is configured"):
        assert jsonplaceholder_client is not None, "API client should be initialized"
        assert jsonplaceholder_client.client is not None, "Inner API client should be initialized"
        
        # Get base URL from the inner APIClient
        base_url = jsonplaceholder_client.client.base_url
        timeout = jsonplaceholder_client.client.timeout
        
        # Attach configuration details to Allure report
        allure.attach(
            base_url,
            name="API Base URL",
            attachment_type=allure.attachment_type.TEXT
        )
        
        allure.attach(
            str(timeout),
            name="API Timeout (seconds)",
            attachment_type=allure.attachment_type.TEXT
        )
        
        allure.attach(
            settings.env,
            name="Environment",
            attachment_type=allure.attachment_type.TEXT
        )
        
        logger.info(f"API client configured for {base_url}")


@given("I am authenticated")
@allure.story("Authentication Setup")
def authenticated(api_client, settings):
    """
    Verify authentication is configured for the API client.
    
    This step ensures that authentication credentials are available and
    the API client is ready to make authenticated requests. It attaches
    authentication status to the Allure report.
    
    Note:
        For JSONPlaceholder API, authentication is not required, but this
        step demonstrates the pattern for APIs that require authentication.
        The step checks if authentication is configured in settings.
    
    Args:
        api_client: API client fixture (with authentication support)
        settings: Settings fixture with authentication credentials
        
    Example in feature file:
        Given I am authenticated
    """
    with allure.step("Verify authentication is configured"):
        # For JSONPlaceholder, authentication is not required
        # This step demonstrates the pattern for authenticated APIs
        
        # Check if authentication credentials are configured
        auth_configured = bool(settings.auth_user and settings.auth_password)
        
        # Attach authentication status to Allure report
        auth_status = "Configured" if auth_configured else "Not Required"
        allure.attach(
            auth_status,
            name="Authentication Status",
            attachment_type=allure.attachment_type.TEXT
        )
        
        if auth_configured:
            allure.attach(
                settings.auth_user,
                name="Auth User",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                settings.auth_type,
                name="Auth Type",
                attachment_type=allure.attachment_type.TEXT
            )
            
            logger.info(f"Authentication configured for user: {settings.auth_user}")
        else:
            logger.info("Authentication not required for this API")


@given("the database is connected and ready")
@allure.story("Database Setup")
def database_connected(db_manager, settings):
    """
    Ensure database connection is available and ready for operations.
    
    This step verifies that the database manager is initialized and
    the database connection is working properly. It attaches database
    configuration details to the Allure report.
    
    Args:
        db_manager: Database manager fixture
        settings: Settings fixture with database configuration
        
    Raises:
        AssertionError: If the database is not properly connected
        
    Example in feature file:
        Given the database is connected and ready
    """
    with allure.step("Verify database connection is ready"):
        assert db_manager is not None, "Database manager should be initialized"
        
        # Test database connection
        try:
            with db_manager.get_session() as session:
                # Execute a simple query to verify connection
                session.execute(text("SELECT 1"))
                
            connection_status = "Connected"
            logger.info("Database connection verified successfully")
            
        except Exception as e:
            connection_status = f"Connection Failed: {str(e)}"
            logger.error(f"Database connection failed: {e}")
            raise AssertionError(f"Database connection failed: {e}")
        
        # Attach database configuration to Allure report
        allure.attach(
            connection_status,
            name="Database Connection Status",
            attachment_type=allure.attachment_type.TEXT
        )
        
        allure.attach(
            f"{settings.db_host}:{settings.db_port}/{settings.db_name}",
            name="Database Connection",
            attachment_type=allure.attachment_type.TEXT
        )
        
        allure.attach(
            settings.env,
            name="Environment",
            attachment_type=allure.attachment_type.TEXT
        )
