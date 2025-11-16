"""
Test file for validating API step definitions.

This test file uses pytest-bdd to execute scenarios from the
api_steps_validation.feature file, validating that all API step definitions
work correctly with the existing fixtures.
"""

import pytest
from pytest_bdd import scenarios

# Import step definitions to register them
# These imports must happen before scenarios() is called
from tests.bdd.steps.common_steps import *  # noqa: F401, F403
from tests.bdd.steps.assertions_steps import *  # noqa: F401, F403
from tests.bdd.steps.api_steps import *  # noqa: F401, F403

# Load all scenarios from the feature file
# Path is relative to the bdd_features_base_dir configured in pytest.ini
scenarios('api/api_steps_validation.feature')
