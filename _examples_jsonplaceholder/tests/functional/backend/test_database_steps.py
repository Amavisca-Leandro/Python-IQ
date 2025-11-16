"""
Test file for validating database step definitions.

This test file uses pytest-bdd to execute scenarios from the
user_management.feature file, validating that all database step definitions
work correctly with the existing fixtures.
"""

import pytest
from pytest_bdd import scenarios

# Import ALL step definitions to ensure they are registered
# pytest-bdd requires explicit imports in the test file
import tests.bdd.steps.common_steps  # noqa: F401
import tests.bdd.steps.assertions_steps  # noqa: F401
import tests.bdd.steps.database_steps  # noqa: F401

# Load all scenarios from the feature file
# Path is relative to the bdd_features_base_dir configured in pytest.ini
scenarios('database/user_management.feature')
