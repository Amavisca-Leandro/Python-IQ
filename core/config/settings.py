"""
Centralized configuration management using Pydantic BaseSettings.

This module provides a Settings class that loads and validates all configuration
from environment variables with support for multiple environments (dev, staging, prod).
"""

from typing import Literal, Optional, List
from pydantic import Field, field_validator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized settings management with environment variable validation.
    
    Supports multiple environments (dev, staging, prod) with automatic
    configuration loading from .env files and environment variables.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # ============================================================================
    # ENVIRONMENT
    # ============================================================================
    env: Literal["dev", "staging", "prod"] = Field(
        default="dev",
        description="Current environment"
    )
    
    # ============================================================================
    # API CONFIGURATION
    # ============================================================================
    api_base_url: str = Field(
        default="https://api.example.com",
        description="Base URL for the API under test"
    )
    api_timeout: int = Field(
        default=30,
        ge=1,
        le=300,
        description="API timeout in seconds"
    )
    api_retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Number of retry attempts for failed requests"
    )
    api_version: str = Field(
        default="v1",
        description="API version"
    )
    
    # API Retry & Resilience
    retry_strategy: Literal["exponential", "linear", "constant"] = Field(
        default="exponential",
        description="Retry strategy for failed requests"
    )
    retry_initial_delay: int = Field(
        default=1,
        ge=0,
        description="Initial retry delay in seconds"
    )
    retry_max_delay: int = Field(
        default=10,
        ge=1,
        description="Maximum retry delay in seconds"
    )
    retry_backoff_multiplier: float = Field(
        default=2.0,
        ge=1.0,
        description="Backoff multiplier for exponential strategy"
    )
    retry_status_codes: str = Field(
        default="500,502,503,504,429",
        description="HTTP status codes to retry (comma-separated)"
    )
    enable_circuit_breaker: bool = Field(
        default=False,
        description="Enable circuit breaker pattern"
    )
    circuit_breaker_threshold: int = Field(
        default=5,
        ge=1,
        description="Circuit breaker failure threshold"
    )
    circuit_breaker_timeout: int = Field(
        default=60,
        ge=1,
        description="Circuit breaker timeout in seconds"
    )
    
    # ============================================================================
    # AUTHENTICATION
    # ============================================================================
    auth_user: str = Field(
        default="test_user@example.com",
        description="Test user credentials for authentication"
    )
    auth_password: str = Field(
        default="SecurePassword123!",
        description="Test user password"
    )
    admin_user: str = Field(
        default="admin@example.com",
        description="Admin user credentials"
    )
    admin_password: str = Field(
        default="AdminPassword123!",
        description="Admin user password"
    )
    api_key: Optional[str] = Field(
        default=None,
        description="API Key for token-based auth"
    )
    api_token: Optional[str] = Field(
        default=None,
        description="API Token for token-based auth"
    )
    auth_type: Literal["basic", "bearer", "oauth2", "api_key"] = Field(
        default="bearer",
        description="Authentication type"
    )
    token_refresh_endpoint: str = Field(
        default="/auth/refresh",
        description="Token refresh endpoint"
    )
    token_expiration_buffer: int = Field(
        default=300,
        ge=0,
        description="Token expiration buffer in seconds"
    )
    auto_refresh_token: bool = Field(
        default=True,
        description="Enable automatic token refresh"
    )
    
    # OAuth2 Configuration
    oauth2_client_id: Optional[str] = Field(
        default=None,
        description="OAuth2 client ID"
    )
    oauth2_client_secret: Optional[str] = Field(
        default=None,
        description="OAuth2 client secret"
    )
    oauth2_scope: Optional[str] = Field(
        default=None,
        description="OAuth2 scope"
    )
    oauth2_token_url: Optional[str] = Field(
        default=None,
        description="OAuth2 token URL"
    )
    
    # ============================================================================
    # FRONTEND CONFIGURATION
    # ============================================================================
    frontend_base_url: str = Field(
        default="https://app.example.com",
        description="Base URL for the frontend application"
    )
    browser: Literal["chromium", "firefox", "webkit"] = Field(
        default="chromium",
        description="Browser selection for Playwright tests"
    )
    headless: bool = Field(
        default=True,
        description="Run browser in headless mode"
    )
    viewport_width: int = Field(
        default=1920,
        ge=320,
        description="Browser viewport width"
    )
    viewport_height: int = Field(
        default=1080,
        ge=240,
        description="Browser viewport height"
    )
    slow_mo: int = Field(
        default=0,
        ge=0,
        description="Slow down browser operations in milliseconds"
    )
    navigation_timeout: int = Field(
        default=30000,
        ge=1000,
        description="Default navigation timeout in milliseconds"
    )
    action_timeout: int = Field(
        default=10000,
        ge=1000,
        description="Default action timeout in milliseconds"
    )
    wait_for_network_idle: bool = Field(
        default=True,
        description="Wait for network idle before considering navigation complete"
    )
    capture_console_logs: bool = Field(
        default=True,
        description="Enable browser console log capture"
    )
    enable_tracing: bool = Field(
        default=False,
        description="Enable trace recording for debugging"
    )
    device_emulation: Optional[str] = Field(
        default=None,
        description="Device emulation (e.g., 'iPhone 12', 'Pixel 5')"
    )
    user_agent: Optional[str] = Field(
        default=None,
        description="User agent override"
    )
    
    # ============================================================================
    # DATABASE CONFIGURATION
    # ============================================================================
    db_host: str = Field(
        default="localhost",
        description="Database host"
    )
    db_port: int = Field(
        default=5432,
        ge=1,
        le=65535,
        description="Database port"
    )
    db_name: str = Field(
        default="test_database",
        description="Database name"
    )
    db_user: str = Field(
        default="test_user",
        description="Database user"
    )
    db_password: str = Field(
        default="test_password",
        description="Database password"
    )
    db_driver: str = Field(
        default="postgresql",
        description="Database driver"
    )
    db_pool_size: int = Field(
        default=10,
        ge=1,
        description="Database connection pool size"
    )
    db_max_overflow: int = Field(
        default=20,
        ge=0,
        description="Database connection pool max overflow"
    )
    db_pool_pre_ping: bool = Field(
        default=True,
        description="Pool pre-ping to verify connections"
    )
    db_pool_recycle: int = Field(
        default=3600,
        ge=0,
        description="Pool recycle time in seconds"
    )
    db_schema: str = Field(
        default="public",
        description="Database schema"
    )
    db_echo: bool = Field(
        default=False,
        description="Enable SQL query logging"
    )
    db_isolation_level: Literal["READ_COMMITTED", "REPEATABLE_READ", "SERIALIZABLE"] = Field(
        default="READ_COMMITTED",
        description="Database isolation level"
    )
    
    # ============================================================================
    # TEST EXECUTION CONFIGURATION
    # ============================================================================
    pytest_workers: str = Field(
        default="auto",
        description="Number of parallel workers for test execution"
    )
    max_failures: int = Field(
        default=5,
        ge=0,
        description="Maximum number of test failures before stopping"
    )
    test_timeout: int = Field(
        default=300,
        ge=1,
        description="Test timeout in seconds"
    )
    screenshot_on_failure: bool = Field(
        default=True,
        description="Screenshot on failure"
    )
    video_recording: bool = Field(
        default=False,
        description="Video recording for UI tests"
    )
    pytest_rerun_failures: int = Field(
        default=2,
        ge=0,
        description="Retry failed tests automatically"
    )
    pytest_rerun_delay: int = Field(
        default=1,
        ge=0,
        description="Delay between retries in seconds"
    )
    pytest_strict_markers: bool = Field(
        default=True,
        description="Enable strict markers"
    )
    pytest_capture: Literal["yes", "no", "all"] = Field(
        default="no",
        description="Capture console output"
    )
    pytest_verbose_summary: str = Field(
        default="error,failed",
        description="Show extra test summary info"
    )
    
    # ============================================================================
    # REPORTING CONFIGURATION
    # ============================================================================
    allure_results_dir: str = Field(
        default="reports/allure-results",
        description="Allure results directory"
    )
    allure_report_dir: str = Field(
        default="reports/allure-report",
        description="Allure report directory"
    )
    html_report_path: str = Field(
        default="reports/report.html",
        description="HTML report path"
    )
    
    # ============================================================================
    # INTEGRATION - ZEPHYR SCALE
    # ============================================================================
    zephyr_api_url: str = Field(
        default="https://api.zephyrscale.smartbear.com/v2",
        description="Zephyr Scale API URL"
    )
    zephyr_api_token: Optional[str] = Field(
        default=None,
        description="Zephyr Scale API token"
    )
    zephyr_project_key: str = Field(
        default="PROJ",
        description="Zephyr project key"
    )
    zephyr_sync_enabled: bool = Field(
        default=False,
        description="Enable automatic sync to Zephyr"
    )
    zephyr_test_cycle: str = Field(
        default="Automated Tests - ${ENV}",
        description="Test cycle name for Zephyr"
    )
    zephyr_folder_id: Optional[str] = Field(
        default=None,
        description="Folder ID in Zephyr"
    )
    zephyr_sync_only_on_ci: bool = Field(
        default=True,
        description="Sync only on CI environment"
    )
    zephyr_batch_size: int = Field(
        default=50,
        ge=1,
        description="Batch size for syncing test results"
    )
    
    # ============================================================================
    # INTEGRATION - JIRA
    # ============================================================================
    jira_url: str = Field(
        default="https://your-company.atlassian.net",
        description="Jira URL"
    )
    jira_api_token: Optional[str] = Field(
        default=None,
        description="Jira API token"
    )
    jira_project_key: str = Field(
        default="PROJ",
        description="Jira project key"
    )
    jira_user_email: Optional[str] = Field(
        default=None,
        description="Jira user email"
    )
    jira_auto_create_defects: bool = Field(
        default=False,
        description="Enable automatic defect creation on test failure"
    )
    jira_defect_issue_type: str = Field(
        default="Bug",
        description="Issue type for defects"
    )
    jira_defect_priority: str = Field(
        default="Medium",
        description="Default priority for auto-created defects"
    )
    jira_defect_labels: str = Field(
        default="automated-test,regression",
        description="Labels to add to auto-created defects"
    )
    
    # ============================================================================
    # INTEGRATION - SLACK
    # ============================================================================
    slack_webhook_url: Optional[str] = Field(
        default=None,
        description="Slack webhook URL"
    )
    slack_channel: str = Field(
        default="#test-automation",
        description="Slack channel"
    )
    slack_notifications_enabled: bool = Field(
        default=False,
        description="Enable Slack notifications"
    )
    slack_notify_on_failure_only: bool = Field(
        default=True,
        description="Notify only on failures"
    )
    slack_notify_only_on_ci: bool = Field(
        default=True,
        description="Notify only on CI environment"
    )
    slack_include_summary: bool = Field(
        default=True,
        description="Include test summary in notifications"
    )
    slack_mention_on_critical: Optional[str] = Field(
        default=None,
        description="Mention users on critical failures"
    )
    
    # ============================================================================
    # LOGGING CONFIGURATION
    # ============================================================================
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Log level for test execution"
    )
    log_file: str = Field(
        default="reports/pytest.log",
        description="Log file path"
    )
    log_format: Literal["simple", "detailed", "json"] = Field(
        default="detailed",
        description="Log format"
    )
    log_colored: bool = Field(
        default=True,
        description="Enable colored logs in console"
    )
    log_http_requests: bool = Field(
        default=True,
        description="Log HTTP requests and responses"
    )
    log_db_queries: bool = Field(
        default=False,
        description="Log database queries"
    )
    log_max_size_mb: int = Field(
        default=100,
        ge=0,
        description="Maximum log file size in MB"
    )
    log_backup_count: int = Field(
        default=5,
        ge=0,
        description="Number of log files to keep"
    )
    
    # ============================================================================
    # DATA GENERATION & TEST DATA FACTORY
    # ============================================================================
    faker_locale: str = Field(
        default="pt_BR",
        description="Locale for Faker data generation"
    )
    faker_seed: Optional[int] = Field(
        default=None,
        description="Seed for reproducible random data"
    )
    auto_cleanup_test_data: bool = Field(
        default=True,
        description="Enable automatic test data cleanup"
    )
    test_data_retention_hours: int = Field(
        default=0,
        ge=0,
        description="Test data retention time in hours"
    )
    test_data_prefix: str = Field(
        default="test_",
        description="Prefix for test data identification"
    )
    enable_data_factory_tracking: bool = Field(
        default=True,
        description="Enable test data factory tracking"
    )
    
    # ============================================================================
    # PERFORMANCE & MONITORING
    # ============================================================================
    enable_performance_metrics: bool = Field(
        default=True,
        description="Enable performance metrics collection"
    )
    api_response_time_threshold: int = Field(
        default=2000,
        ge=0,
        description="API response time threshold in milliseconds"
    )
    ui_page_load_threshold: int = Field(
        default=5000,
        ge=0,
        description="UI page load time threshold in milliseconds"
    )
    track_memory_usage: bool = Field(
        default=False,
        description="Enable memory usage tracking"
    )
    detect_flaky_tests: bool = Field(
        default=True,
        description="Enable flaky test detection"
    )
    flaky_test_runs: int = Field(
        default=3,
        ge=2,
        description="Number of runs to determine flakiness"
    )
    
    # ============================================================================
    # CI/CD CONFIGURATION
    # ============================================================================
    ci: bool = Field(
        default=False,
        description="CI environment flag"
    )
    build_number: str = Field(
        default="local",
        description="Build number or identifier"
    )
    git_branch: str = Field(
        default="main",
        description="Git branch name"
    )
    
    # ============================================================================
    # TEST DATA ISOLATION & CLEANUP
    # ============================================================================
    enable_test_isolation: bool = Field(
        default=True,
        description="Enable test isolation"
    )
    use_db_transactions: bool = Field(
        default=True,
        description="Use database transactions for test isolation"
    )
    cleanup_strategy: Literal["immediate", "deferred", "manual"] = Field(
        default="immediate",
        description="Cleanup strategy"
    )
    parallel_execution_safe: bool = Field(
        default=True,
        description="Enable parallel test execution safety"
    )
    test_data_namespace: str = Field(
        default="autotest_",
        description="Test data namespace prefix"
    )
    
    # ============================================================================
    # ENVIRONMENT-SPECIFIC OVERRIDES
    # ============================================================================
    dev_api_base_url: Optional[str] = Field(
        default="http://localhost:8000",
        description="Development API base URL"
    )
    dev_frontend_base_url: Optional[str] = Field(
        default="http://localhost:3000",
        description="Development frontend base URL"
    )
    dev_db_host: Optional[str] = Field(
        default="localhost",
        description="Development database host"
    )
    
    staging_api_base_url: Optional[str] = Field(
        default="https://staging-api.example.com",
        description="Staging API base URL"
    )
    staging_frontend_base_url: Optional[str] = Field(
        default="https://staging.example.com",
        description="Staging frontend base URL"
    )
    staging_db_host: Optional[str] = Field(
        default="staging-db.example.com",
        description="Staging database host"
    )
    
    prod_api_base_url: Optional[str] = Field(
        default="https://api.example.com",
        description="Production API base URL"
    )
    prod_frontend_base_url: Optional[str] = Field(
        default="https://app.example.com",
        description="Production frontend base URL"
    )
    prod_db_host: Optional[str] = Field(
        default="prod-db.example.com",
        description="Production database host"
    )
    
    # ============================================================================
    # OPTIONAL INTEGRATIONS
    # ============================================================================
    aws_access_key_id: Optional[str] = Field(
        default=None,
        description="AWS access key ID"
    )
    aws_secret_access_key: Optional[str] = Field(
        default=None,
        description="AWS secret access key"
    )
    aws_region: str = Field(
        default="us-east-1",
        description="AWS region"
    )
    
    email_host: Optional[str] = Field(
        default=None,
        description="Email service host"
    )
    email_port: int = Field(
        default=587,
        ge=1,
        le=65535,
        description="Email service port"
    )
    email_user: Optional[str] = Field(
        default=None,
        description="Email service user"
    )
    email_password: Optional[str] = Field(
        default=None,
        description="Email service password"
    )
    
    # ============================================================================
    # COMPUTED PROPERTIES
    # ============================================================================
    
    @computed_field
    @property
    def database_url(self) -> str:
        """
        Computed database URL for SQLAlchemy connection.
        
        Returns:
            str: Complete database connection string
        """
        return (
            f"{self.db_driver}://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )
    
    @computed_field
    @property
    def retry_status_codes_list(self) -> List[int]:
        """
        Convert comma-separated retry status codes to list of integers.
        
        Returns:
            List[int]: List of HTTP status codes to retry
        """
        return [int(code.strip()) for code in self.retry_status_codes.split(",")]
    
    @computed_field
    @property
    def jira_defect_labels_list(self) -> List[str]:
        """
        Convert comma-separated Jira labels to list of strings.
        
        Returns:
            List[str]: List of Jira labels
        """
        return [label.strip() for label in self.jira_defect_labels.split(",")]
    
    # ============================================================================
    # VALIDATORS
    # ============================================================================
    
    @field_validator("api_timeout", "test_timeout")
    @classmethod
    def validate_timeout(cls, v: int) -> int:
        """Validate timeout values are reasonable."""
        if v < 1:
            raise ValueError("Timeout must be at least 1 second")
        if v > 3600:
            raise ValueError("Timeout cannot exceed 3600 seconds (1 hour)")
        return v
    
    @field_validator("db_pool_size", "db_max_overflow")
    @classmethod
    def validate_pool_size(cls, v: int) -> int:
        """Validate database pool sizes are reasonable."""
        if v < 1:
            raise ValueError("Pool size must be at least 1")
        if v > 100:
            raise ValueError("Pool size cannot exceed 100")
        return v
    
    @field_validator("retry_max_delay")
    @classmethod
    def validate_retry_delay(cls, v: int, info) -> int:
        """Validate retry max delay is greater than initial delay."""
        if hasattr(info.data, "retry_initial_delay"):
            if v < info.data.get("retry_initial_delay", 1):
                raise ValueError("Max delay must be greater than or equal to initial delay")
        return v


# Singleton instance
_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the singleton Settings instance.
    
    Returns:
        Settings: The global settings instance
    """
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance


def reload_settings() -> Settings:
    """
    Reload settings from environment (useful for testing).
    
    Returns:
        Settings: New settings instance
    """
    global _settings_instance
    _settings_instance = Settings()
    return _settings_instance
