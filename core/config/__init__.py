"""
Configuration management module.

This module provides centralized configuration management with support
for multiple environments and automatic environment variable loading.
"""

from core.config.settings import (
    Settings,
    get_settings,
    reload_settings,
)

from core.config.environments import (
    Environment,
    get_environment,
    get_current_environment,
    apply_environment_overrides,
    list_environments,
    get_environment_info,
    is_production,
    is_development,
    is_staging,
    DEV_ENVIRONMENT,
    STAGING_ENVIRONMENT,
    PROD_ENVIRONMENT,
)

__all__ = [
    # Settings
    "Settings",
    "get_settings",
    "reload_settings",
    # Environments
    "Environment",
    "get_environment",
    "get_current_environment",
    "apply_environment_overrides",
    "list_environments",
    "get_environment_info",
    "is_production",
    "is_development",
    "is_staging",
    "DEV_ENVIRONMENT",
    "STAGING_ENVIRONMENT",
    "PROD_ENVIRONMENT",
]
