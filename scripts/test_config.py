"""
Simple script to test the configuration system.

This script verifies that the Settings and Environment Manager
are working correctly.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import (
    get_settings,
    get_environment,
    get_current_environment,
    list_environments,
    is_development,
    apply_environment_overrides,
)


def test_settings():
    """Test Settings class."""
    print("=" * 80)
    print("Testing Settings Class")
    print("=" * 80)
    
    settings = get_settings()
    
    print(f"✓ Environment: {settings.env}")
    print(f"✓ API Base URL: {settings.api_base_url}")
    print(f"✓ Frontend Base URL: {settings.frontend_base_url}")
    print(f"✓ Database URL: {settings.database_url}")
    print(f"✓ Browser: {settings.browser}")
    print(f"✓ Headless: {settings.headless}")
    print(f"✓ Log Level: {settings.log_level}")
    print(f"✓ Pytest Workers: {settings.pytest_workers}")
    print(f"✓ Retry Status Codes: {settings.retry_status_codes_list}")
    print()


def test_environments():
    """Test Environment Manager."""
    print("=" * 80)
    print("Testing Environment Manager")
    print("=" * 80)
    
    # List all environments
    envs = list_environments()
    print(f"✓ Available environments: {', '.join(envs)}")
    print()
    
    # Test each environment
    for env_name in envs:
        env = get_environment(env_name)
        print(f"Environment: {env.name}")
        print(f"  - API URL: {env.api_base_url}")
        print(f"  - Frontend URL: {env.frontend_base_url}")
        print(f"  - DB Host: {env.db_host}")
        print(f"  - Overrides: {len(env.overrides)} settings")
        print()


def test_current_environment():
    """Test current environment detection."""
    print("=" * 80)
    print("Testing Current Environment Detection")
    print("=" * 80)
    
    current_env = get_current_environment()
    print(f"✓ Current environment: {current_env.name}")
    print(f"✓ Is development: {is_development()}")
    print()


def test_environment_overrides():
    """Test applying environment overrides."""
    print("=" * 80)
    print("Testing Environment Overrides")
    print("=" * 80)
    
    settings = get_settings()
    
    print(f"Before override:")
    print(f"  - API URL: {settings.api_base_url}")
    print(f"  - Headless: {settings.headless}")
    print()
    
    # Apply staging overrides
    apply_environment_overrides(settings, "staging")
    
    print(f"After applying 'staging' overrides:")
    print(f"  - API URL: {settings.api_base_url}")
    print(f"  - Headless: {settings.headless}")
    print()


def test_computed_properties():
    """Test computed properties."""
    print("=" * 80)
    print("Testing Computed Properties")
    print("=" * 80)
    
    settings = get_settings()
    
    print(f"✓ Database URL: {settings.database_url}")
    print(f"✓ Retry Status Codes List: {settings.retry_status_codes_list}")
    print(f"✓ Jira Defect Labels List: {settings.jira_defect_labels_list}")
    print()


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "Configuration System Test" + " " * 33 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    try:
        test_settings()
        test_environments()
        test_current_environment()
        test_environment_overrides()
        test_computed_properties()
        
        print("=" * 80)
        print("✓ All tests passed successfully!")
        print("=" * 80)
        print()
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
