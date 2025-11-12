"""
Environment-specific configuration management.

This module provides environment-specific configurations that override
base settings for different deployment environments (dev, staging, prod).
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import os


@dataclass
class Environment:
    """
    Environment-specific configuration container.
    
    Attributes:
        name: Environment name (dev, staging, prod)
        api_base_url: API base URL for this environment
        frontend_base_url: Frontend base URL for this environment
        db_host: Database host for this environment
        db_port: Database port for this environment
        db_name: Database name for this environment
        overrides: Additional environment-specific overrides
    """
    
    name: str
    api_base_url: str
    frontend_base_url: str
    db_host: str
    db_port: int = 5432
    db_name: str = "test_database"
    overrides: Dict[str, Any] = field(default_factory=dict)
    
    def get_override(self, key: str, default: Any = None) -> Any:
        """
        Get an environment-specific override value.
        
        Args:
            key: Configuration key to retrieve
            default: Default value if key not found
            
        Returns:
            Override value or default
        """
        return self.overrides.get(key, default)
    
    def apply_overrides(self, settings: Any) -> None:
        """
        Apply environment-specific overrides to settings object.
        
        Args:
            settings: Settings object to apply overrides to
        """
        # Apply base environment overrides
        settings.api_base_url = self.api_base_url
        settings.frontend_base_url = self.frontend_base_url
        settings.db_host = self.db_host
        settings.db_port = self.db_port
        settings.db_name = self.db_name
        
        # Apply additional overrides
        for key, value in self.overrides.items():
            if hasattr(settings, key):
                setattr(settings, key, value)


# ============================================================================
# ENVIRONMENT DEFINITIONS
# ============================================================================

DEV_ENVIRONMENT = Environment(
    name="dev",
    api_base_url="http://localhost:8000",
    frontend_base_url="http://localhost:3000",
    db_host="localhost",
    db_port=5432,
    db_name="test_database_dev",
    overrides={
        "headless": False,  # Show browser in dev
        "log_level": "DEBUG",  # More verbose logging
        "db_echo": True,  # Show SQL queries
        "enable_tracing": True,  # Enable Playwright tracing
        "slow_mo": 100,  # Slow down browser for debugging
        "screenshot_on_failure": True,
        "video_recording": False,
        "pytest_workers": "2",  # Limit workers for easier debugging
        "auto_refresh_token": True,
        "enable_performance_metrics": True,
        "log_http_requests": True,
        "log_db_queries": True,
        "capture_console_logs": True,
        "wait_for_network_idle": True,
        "enable_test_isolation": True,
        "use_db_transactions": True,
        "cleanup_strategy": "immediate",
        "auto_cleanup_test_data": True,
        "test_data_retention_hours": 0,
        "zephyr_sync_enabled": False,  # Disable integrations in dev
        "slack_notifications_enabled": False,
        "jira_auto_create_defects": False,
    }
)

STAGING_ENVIRONMENT = Environment(
    name="staging",
    api_base_url="https://staging-api.example.com",
    frontend_base_url="https://staging.example.com",
    db_host="staging-db.example.com",
    db_port=5432,
    db_name="test_database_staging",
    overrides={
        "headless": True,  # Headless in staging
        "log_level": "INFO",
        "db_echo": False,
        "enable_tracing": False,
        "slow_mo": 0,
        "screenshot_on_failure": True,
        "video_recording": True,  # Record videos in staging
        "pytest_workers": "auto",  # Use all available cores
        "auto_refresh_token": True,
        "enable_performance_metrics": True,
        "log_http_requests": True,
        "log_db_queries": False,
        "capture_console_logs": True,
        "wait_for_network_idle": True,
        "enable_test_isolation": True,
        "use_db_transactions": True,
        "cleanup_strategy": "immediate",
        "auto_cleanup_test_data": True,
        "test_data_retention_hours": 1,  # Keep data for 1 hour for debugging
        "zephyr_sync_enabled": True,  # Enable Zephyr sync
        "slack_notifications_enabled": True,  # Enable Slack notifications
        "slack_notify_on_failure_only": True,
        "jira_auto_create_defects": False,  # Manual defect creation
        "detect_flaky_tests": True,
        "pytest_rerun_failures": 2,  # Retry flaky tests
    }
)

PROD_ENVIRONMENT = Environment(
    name="prod",
    api_base_url="https://api.example.com",
    frontend_base_url="https://app.example.com",
    db_host="prod-db.example.com",
    db_port=5432,
    db_name="test_database_prod",
    overrides={
        "headless": True,
        "log_level": "WARNING",  # Less verbose in prod
        "db_echo": False,
        "enable_tracing": False,
        "slow_mo": 0,
        "screenshot_on_failure": True,
        "video_recording": True,
        "pytest_workers": "auto",
        "auto_refresh_token": True,
        "enable_performance_metrics": True,
        "log_http_requests": False,  # Reduce logging in prod
        "log_db_queries": False,
        "capture_console_logs": False,
        "wait_for_network_idle": True,
        "enable_test_isolation": True,
        "use_db_transactions": True,
        "cleanup_strategy": "immediate",
        "auto_cleanup_test_data": True,
        "test_data_retention_hours": 0,  # Immediate cleanup in prod
        "zephyr_sync_enabled": True,
        "slack_notifications_enabled": True,
        "slack_notify_on_failure_only": False,  # Notify on all results
        "jira_auto_create_defects": True,  # Auto-create defects in prod
        "detect_flaky_tests": True,
        "pytest_rerun_failures": 1,  # Minimal retries in prod
        "max_failures": 10,  # Stop after more failures in prod
    }
)


# Environment registry
ENVIRONMENTS: Dict[str, Environment] = {
    "dev": DEV_ENVIRONMENT,
    "staging": STAGING_ENVIRONMENT,
    "prod": PROD_ENVIRONMENT,
}


def get_environment(env_name: Optional[str] = None) -> Environment:
    """
    Get environment configuration by name.
    
    Automatically detects environment from ENV environment variable
    if env_name is not provided.
    
    Args:
        env_name: Environment name (dev, staging, prod). 
                 If None, reads from ENV environment variable.
    
    Returns:
        Environment: Environment configuration object
        
    Raises:
        ValueError: If environment name is invalid
        
    Examples:
        >>> env = get_environment("dev")
        >>> env = get_environment()  # Auto-detect from ENV variable
    """
    if env_name is None:
        env_name = os.getenv("ENV", "dev").lower()
    
    env_name = env_name.lower()
    
    if env_name not in ENVIRONMENTS:
        raise ValueError(
            f"Invalid environment: {env_name}. "
            f"Valid options: {', '.join(ENVIRONMENTS.keys())}"
        )
    
    return ENVIRONMENTS[env_name]


def get_current_environment() -> Environment:
    """
    Get the current environment based on ENV environment variable.
    
    Returns:
        Environment: Current environment configuration
        
    Examples:
        >>> env = get_current_environment()
        >>> print(env.name)
        'dev'
    """
    return get_environment()


def apply_environment_overrides(settings: Any, env_name: Optional[str] = None) -> None:
    """
    Apply environment-specific overrides to a settings object.
    
    This function modifies the settings object in-place by applying
    environment-specific configuration overrides.
    
    Args:
        settings: Settings object to modify
        env_name: Environment name. If None, auto-detects from ENV variable.
        
    Examples:
        >>> from core.config.settings import get_settings
        >>> settings = get_settings()
        >>> apply_environment_overrides(settings, "staging")
    """
    environment = get_environment(env_name)
    environment.apply_overrides(settings)


def list_environments() -> list[str]:
    """
    List all available environment names.
    
    Returns:
        list[str]: List of environment names
        
    Examples:
        >>> envs = list_environments()
        >>> print(envs)
        ['dev', 'staging', 'prod']
    """
    return list(ENVIRONMENTS.keys())


def get_environment_info(env_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get detailed information about an environment.
    
    Args:
        env_name: Environment name. If None, uses current environment.
        
    Returns:
        Dict[str, Any]: Environment information dictionary
        
    Examples:
        >>> info = get_environment_info("staging")
        >>> print(info["api_base_url"])
        'https://staging-api.example.com'
    """
    environment = get_environment(env_name)
    
    return {
        "name": environment.name,
        "api_base_url": environment.api_base_url,
        "frontend_base_url": environment.frontend_base_url,
        "db_host": environment.db_host,
        "db_port": environment.db_port,
        "db_name": environment.db_name,
        "overrides": environment.overrides,
    }


def is_production() -> bool:
    """
    Check if current environment is production.
    
    Returns:
        bool: True if current environment is production
        
    Examples:
        >>> if is_production():
        ...     print("Running in production!")
    """
    return get_current_environment().name == "prod"


def is_development() -> bool:
    """
    Check if current environment is development.
    
    Returns:
        bool: True if current environment is development
        
    Examples:
        >>> if is_development():
        ...     print("Running in development mode")
    """
    return get_current_environment().name == "dev"


def is_staging() -> bool:
    """
    Check if current environment is staging.
    
    Returns:
        bool: True if current environment is staging
        
    Examples:
        >>> if is_staging():
        ...     print("Running in staging")
    """
    return get_current_environment().name == "staging"
