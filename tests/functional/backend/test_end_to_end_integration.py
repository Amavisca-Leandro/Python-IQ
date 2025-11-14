"""
Test file for End-to-End Integration BDD scenarios.

This test file uses pytest-bdd to execute scenarios from the
end_to_end.feature file, providing comprehensive testing of
integrated workflows combining API calls and database operations.

The scenarios demonstrate:
- Data flow through Given-When-Then steps
- Usage of bdd_context for data sharing between steps
- Multiple API calls in sequence
- Database validation after API operations
- Complex workflows with multiple entities
"""

import pytest
from pytest_bdd import scenarios

# Import step definitions to register them
# These imports must happen before scenarios() is called
from tests.bdd.steps.common_steps import *  # noqa: F401, F403
from tests.bdd.steps.assertions_steps import *  # noqa: F401, F403
from tests.bdd.steps.api_steps import *  # noqa: F401, F403
from tests.bdd.steps.database_steps import *  # noqa: F401, F403

# Load all scenarios from the end-to-end integration feature file
# Path is relative to the bdd_features_base_dir configured in pytest.ini
scenarios('integration/end_to_end.feature')
