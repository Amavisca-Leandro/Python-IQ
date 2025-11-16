"""
Test file for Posts API BDD scenarios.

This test file uses pytest-bdd to execute scenarios from the
posts.feature file, providing comprehensive testing of the
JSONPlaceholder Posts API endpoints.
"""

import pytest
from pytest_bdd import scenarios

# Import step definitions to register them
# These imports must happen before scenarios() is called
from tests.bdd.steps.common_steps import *  # noqa: F401, F403
from tests.bdd.steps.assertions_steps import *  # noqa: F401, F403
from tests.bdd.steps.api_steps import *  # noqa: F401, F403

# Load all scenarios from the posts feature file
# Path is relative to the bdd_features_base_dir configured in pytest.ini
scenarios('api/posts.feature')
