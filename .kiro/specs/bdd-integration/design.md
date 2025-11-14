# BDD Integration Design Document

## Overview

This design document outlines the integration of pytest-bdd into the existing Python test automation framework. The solution will enable writing tests in Gherkin syntax while maintaining full compatibility with existing pytest infrastructure, Allure reporting, database fixtures, and API client capabilities.

The design follows a layered approach where BDD scenarios act as high-level test specifications that leverage existing framework components through reusable step definitions.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Test Execution Layer                      │
│  (pytest, Test Explorer, CLI, CI/CD)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                    BDD Layer (pytest-bdd)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Feature    │  │   Scenario   │  │    Steps     │     │
│  │    Files     │  │   Parsing    │  │  Execution   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│              Step Definitions Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  API Steps   │  │   DB Steps   │  │ Common Steps │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│              Existing Framework Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  APIClient   │  │  DBManager   │  │   Fixtures   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Integration Points

1. **pytest-bdd Plugin**: Integrates with pytest's plugin system
2. **Allure Integration**: Uses allure-pytest hooks to capture BDD steps
3. **Fixture Injection**: Step definitions receive pytest fixtures via dependency injection
4. **Context Sharing**: Custom fixture provides scenario-scoped context for data sharing

## Components and Interfaces

### 1. Directory Structure

```
tests/
├── bdd/
│   ├── __init__.py
│   ├── README.md                    # BDD documentation
│   ├── features/                    # Gherkin feature files
│   │   ├── api/
│   │   │   ├── posts.feature
│   │   │   ├── users.feature
│   │   │   └── comments.feature
│   │   ├── database/
│   │   │   └── data_management.feature
│   │   └── integration/
│   │       └── end_to_end.feature
│   ├── steps/                       # Step definitions
│   │   ├── __init__.py
│   │   ├── api_steps.py            # API-related steps
│   │   ├── database_steps.py       # Database-related steps
│   │   ├── common_steps.py         # Common/shared steps
│   │   └── assertions_steps.py     # Assertion steps
│   └── conftest.py                  # BDD-specific fixtures
```

### 2. Feature Files

Feature files use standard Gherkin syntax with tags for pytest markers.

**Example: tests/bdd/features/api/posts.feature**

```gherkin
@smoke @backend @api
Feature: JSONPlaceholder Posts API
  As a QA engineer
  I want to test the Posts API endpoints
  So that I can ensure the API works correctly

  Background:
    Given the API client is configured
    And I am authenticated

  @crud
  Scenario: Get all posts
    When I send a GET request to "/posts"
    Then the response status code should be 200
    And the response should be a non-empty list
    And each post should have required fields:
      | userId |
      | id     |
      | title  |
      | body   |

  @crud
  Scenario: Create a new post
    Given I have post data:
      | field  | value                    |
      | userId | 1                        |
      | title  | Test Post from BDD       |
      | body   | This is a test post body |
    When I send a POST request to "/posts" with the post data
    Then the response status code should be 201
    And the response should contain field "id"
    And the response field "title" should equal "Test Post from BDD"

  @crud @validation
  Scenario Outline: Get post by ID
    When I send a GET request to "/posts/<post_id>"
    Then the response status code should be <status_code>
    
    Examples:
      | post_id | status_code |
      | 1       | 200         |
      | 50      | 200         |
      | 99999   | 404         |
```

### 3. Step Definitions

Step definitions are Python functions decorated with pytest-bdd decorators that receive fixtures.

**Example: tests/bdd/steps/api_steps.py**

```python
"""API-related step definitions for BDD tests."""

import allure
from pytest_bdd import given, when, then, parsers
from typing import Dict, Any


@given("the API client is configured")
def api_client_configured(jsonplaceholder_client):
    """Ensure API client is available."""
    assert jsonplaceholder_client is not None
    allure.attach(
        jsonplaceholder_client.base_url,
        "API Base URL",
        allure.attachment_type.TEXT
    )


@given("I am authenticated")
def authenticated(api_client, settings):
    """Authenticate with the API."""
    # Authentication happens automatically via api_client fixture
    assert api_client.is_authenticated() or settings.auth_user
    allure.attach("Authenticated", "Auth Status", allure.attachment_type.TEXT)


@given(parsers.parse('I have post data:\n{data_table}'))
def post_data(bdd_context, data_table):
    """Parse post data from table."""
    data = {}
    for line in data_table.strip().split('\n')[1:]:  # Skip header
        if '|' in line:
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) == 2:
                field, value = parts
                # Convert numeric strings to integers
                data[field] = int(value) if value.isdigit() else value
    
    bdd_context.post_data = data
    allure.attach(str(data), "Post Data", allure.attachment_type.JSON)


@when(parsers.parse('I send a GET request to "{endpoint}"'))
def send_get_request(bdd_context, jsonplaceholder_client, endpoint):
    """Send GET request to endpoint."""
    with allure.step(f"Send GET request to {endpoint}"):
        response = jsonplaceholder_client.get(endpoint)
        bdd_context.response = response
        allure.attach(
            response.text,
            "Response Body",
            allure.attachment_type.JSON
        )


@when(parsers.parse('I send a POST request to "{endpoint}" with the post data'))
def send_post_request_with_data(bdd_context, jsonplaceholder_client, endpoint):
    """Send POST request with data from context."""
    data = bdd_context.post_data
    with allure.step(f"Send POST request to {endpoint}"):
        response = jsonplaceholder_client.post(endpoint, json=data)
        bdd_context.response = response
        allure.attach(
            response.text,
            "Response Body",
            allure.attachment_type.JSON
        )


@then(parsers.parse('the response status code should be {status_code:d}'))
def check_status_code(bdd_context, status_code):
    """Verify response status code."""
    with allure.step(f"Verify status code is {status_code}"):
        assert bdd_context.response.status_code == status_code, \
            f"Expected {status_code}, got {bdd_context.response.status_code}"


@then("the response should be a non-empty list")
def check_non_empty_list(bdd_context):
    """Verify response is a non-empty list."""
    with allure.step("Verify response is a non-empty list"):
        data = bdd_context.response.json()
        assert isinstance(data, list), "Response should be a list"
        assert len(data) > 0, "Response list should not be empty"
        allure.attach(str(len(data)), "List Length", allure.attachment_type.TEXT)


@then(parsers.parse('the response should contain field "{field}"'))
def check_field_exists(bdd_context, field):
    """Verify response contains specified field."""
    with allure.step(f"Verify field '{field}' exists"):
        data = bdd_context.response.json()
        assert field in data, f"Field '{field}' not found in response"


@then(parsers.parse('the response field "{field}" should equal "{value}"'))
def check_field_value(bdd_context, field, value):
    """Verify response field has expected value."""
    with allure.step(f"Verify field '{field}' equals '{value}'"):
        data = bdd_context.response.json()
        actual_value = str(data.get(field))
        assert actual_value == value, \
            f"Expected '{value}', got '{actual_value}'"
```

**Example: tests/bdd/steps/database_steps.py**

```python
"""Database-related step definitions for BDD tests."""

import allure
from pytest_bdd import given, when, then, parsers
from sqlalchemy import text


@given(parsers.parse('I have a test user with email "{email}"'))
def create_test_user(bdd_context, test_data_factory, test_data_context, email):
    """Create a test user in the database."""
    with allure.step(f"Create test user with email {email}"):
        user_data = test_data_factory.create_user_data(
            test_id=test_data_context.test_id,
            email=email
        )
        bdd_context.user_data = user_data
        allure.attach(str(user_data), "User Data", allure.attachment_type.JSON)


@when(parsers.parse('I query the database for user with email "{email}"'))
def query_user_by_email(bdd_context, db_session, email):
    """Query database for user by email."""
    with allure.step(f"Query user with email {email}"):
        result = db_session.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email": email}
        )
        bdd_context.db_result = result.fetchone()


@then("the user should exist in the database")
def verify_user_exists(bdd_context):
    """Verify user exists in database."""
    with allure.step("Verify user exists in database"):
        assert bdd_context.db_result is not None, \
            "User should exist in database"


@then(parsers.parse('the database record should have field "{field}" with value "{value}"'))
def verify_db_field_value(bdd_context, field, value):
    """Verify database field has expected value."""
    with allure.step(f"Verify database field '{field}' equals '{value}'"):
        record = bdd_context.db_result
        actual_value = str(getattr(record, field, None))
        assert actual_value == value, \
            f"Expected '{value}', got '{actual_value}'"
```

### 4. BDD Context Fixture

A scenario-scoped fixture for sharing data between steps.

**tests/bdd/conftest.py**

```python
"""BDD-specific fixtures and configuration."""

import pytest
from typing import Any, Dict


class BDDContext:
    """
    Context object for sharing data between BDD steps.
    
    Provides a simple namespace for storing and retrieving data
    within a scenario execution.
    """
    
    def __init__(self):
        self._data: Dict[str, Any] = {}
    
    def __setattr__(self, name: str, value: Any):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value
    
    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
    
    def get(self, name: str, default: Any = None) -> Any:
        """Get value with default."""
        return self._data.get(name, default)
    
    def has(self, name: str) -> bool:
        """Check if attribute exists."""
        return name in self._data
    
    def clear(self):
        """Clear all data."""
        self._data.clear()


@pytest.fixture(scope="function")
def bdd_context():
    """
    Provide BDD context for sharing data between steps.
    
    Scope: function - New context for each scenario
    
    Yields:
        BDDContext: Context object for the scenario
    """
    context = BDDContext()
    yield context
    context.clear()
```

### 5. pytest.ini Configuration

Update pytest.ini to configure pytest-bdd:

```ini
[pytest]
# ... existing configuration ...

# BDD Configuration
bdd_features_base_dir = tests/bdd/features/
```

## Data Models

### BDDContext

```python
class BDDContext:
    """
    Scenario-scoped context for data sharing.
    
    Attributes:
        response: HTTP response from API calls
        post_data: Data for POST requests
        user_data: User data from database
        db_result: Database query results
        [dynamic]: Any other data stored during scenario execution
    """
```

## Error Handling

### Step Execution Errors

- **Assertion Failures**: Pytest captures and reports with full traceback
- **Fixture Errors**: Reported as setup/teardown failures
- **API Errors**: Logged with request/response details via Allure attachments

### Error Reporting Strategy

1. **Allure Steps**: Wrap operations in `allure.step()` for detailed failure context
2. **Attachments**: Attach request/response data, database queries, and error messages
3. **Screenshots**: For UI tests, attach screenshots on failure (future enhancement)
4. **Logs**: Capture pytest logs with detailed error information

### Example Error Handling in Steps

```python
@when(parsers.parse('I send a GET request to "{endpoint}"'))
def send_get_request(bdd_context, jsonplaceholder_client, endpoint):
    """Send GET request with error handling."""
    try:
        with allure.step(f"Send GET request to {endpoint}"):
            response = jsonplaceholder_client.get(endpoint)
            bdd_context.response = response
            
            # Attach response details
            allure.attach(
                response.text,
                "Response Body",
                allure.attachment_type.JSON
            )
            allure.attach(
                str(response.status_code),
                "Status Code",
                allure.attachment_type.TEXT
            )
    except Exception as e:
        # Attach error details
        allure.attach(
            str(e),
            "Error Details",
            allure.attachment_type.TEXT
        )
        raise
```

## Testing Strategy

### Unit Testing Step Definitions

Step definitions can be tested independently by mocking fixtures:

```python
def test_check_status_code_step():
    """Test status code verification step."""
    # Create mock context
    context = BDDContext()
    context.response = Mock(status_code=200)
    
    # Test step
    check_status_code(context, 200)  # Should pass
    
    with pytest.raises(AssertionError):
        check_status_code(context, 404)  # Should fail
```

### Integration Testing

BDD scenarios themselves serve as integration tests, validating:
- Step definition correctness
- Fixture integration
- API client functionality
- Database operations
- Allure reporting

### Test Execution Modes

1. **Test Explorer**: Visual execution and debugging
2. **CLI**: `pytest tests/bdd/`
3. **Filtered by tags**: `pytest -m "smoke and bdd"`
4. **Parallel**: `pytest tests/bdd/ -n auto`
5. **CI/CD**: Automated execution in pipelines

## Allure Integration

### Feature Mapping

- **Feature File** → Allure Feature
- **Scenario** → Allure Test Case
- **Given/When/Then Steps** → Allure Steps
- **Tags** → Allure Labels and Markers

### Allure Decorators in Step Definitions

```python
@allure.feature("JSONPlaceholder API")
@allure.story("Posts Management")
@when(parsers.parse('I send a POST request to "{endpoint}"'))
def send_post_request(bdd_context, jsonplaceholder_client, endpoint):
    """Send POST request."""
    with allure.step(f"POST {endpoint}"):
        # Implementation
        pass
```

### Automatic Allure Attachments

The framework will automatically attach:
- API request/response bodies
- HTTP headers
- Database query results
- Error messages and tracebacks
- Test data used in scenarios

## Test Explorer Integration

### Discovery

pytest-bdd scenarios are discovered by pytest's test collection mechanism:
- Each scenario becomes a test item
- Test Explorer displays scenarios grouped by feature file
- Tags are converted to pytest markers for filtering

### Execution

- **Run**: Click ▶️ next to scenario in Test Explorer
- **Debug**: Click 🐛 to debug with breakpoints in step definitions
- **Results**: Inline pass/fail indicators with error messages

### Display Format

```
tests/bdd/features/
├── api/
│   └── posts.feature
│       ├── ✓ Get all posts
│       ├── ✓ Create a new post
│       └── ✗ Get post by ID [post_id=99999, status_code=404]
```

## Migration Path

### Phase 1: Setup and Examples
1. Install pytest-bdd
2. Create directory structure
3. Implement core step definitions
4. Create example feature files
5. Document usage

### Phase 2: Convert Existing Tests
1. Identify high-value tests for conversion
2. Create feature files for selected tests
3. Implement missing step definitions
4. Validate Allure reporting
5. Update documentation

### Phase 3: Adoption
1. Train team on BDD practices
2. Establish conventions and guidelines
3. Create step definition library
4. Integrate into CI/CD
5. Monitor and refine

## Dependencies

### New Dependencies

```
pytest-bdd==7.0.1        # BDD support for pytest
```

### Existing Dependencies (Reused)

- pytest==7.4.3
- allure-pytest==2.13.2
- requests==2.31.0
- sqlalchemy==2.0.23
- pydantic==2.5.3

## Performance Considerations

### Step Definition Reusability

- Design generic, reusable steps to minimize duplication
- Use parsers for parameterized steps
- Group related steps in modules

### Fixture Scope

- Use appropriate fixture scopes (session, function)
- Leverage existing session-scoped fixtures (api_client_session, db_manager)
- BDD context is function-scoped for isolation

### Parallel Execution

- BDD scenarios support pytest-xdist for parallel execution
- Ensure step definitions are thread-safe
- Use test_data_context for data isolation

## Security Considerations

- Credentials managed via existing settings/environment variables
- No sensitive data in feature files (use placeholders)
- Database cleanup via existing test_data_factory
- API authentication via existing api_client fixture

## Documentation Requirements

### README.md (tests/bdd/)

Content:
- BDD overview and benefits
- Directory structure explanation
- How to write feature files
- How to write step definitions
- How to run BDD tests
- Integration with existing framework
- Examples and best practices

### Example Feature Files

Provide examples for:
- API testing (GET, POST, PUT, DELETE)
- Database operations
- Data validation
- Scenario outlines with examples
- Background sections
- Tags and markers

### Step Definition Documentation

- Docstrings for all step definitions
- Parameter descriptions
- Usage examples
- Fixture dependencies

## Additional Components (Implemented)

### 6. Allure Helpers Module

**Location:** `core/helpers/allure_helpers.py`

Provides utility functions to simplify Allure reporting integration:

```python
"""Allure reporting helpers and utilities."""

import json
import logging
import functools
from typing import Any, Callable, Optional, Dict
from pathlib import Path

import allure
import requests
from allure_commons.types import AttachmentType


def allure_step(step_title: str) -> Callable:
    """
    Decorator to create Allure steps with custom titles.
    Supports dynamic title formatting with args/kwargs.
    """
    # Implementation...


def attach_request_response(
    response: requests.Response,
    request_name: str = "HTTP Request",
    response_name: str = "HTTP Response"
) -> None:
    """
    Attach HTTP request and response details to Allure report.
    Automatically formats request/response bodies as JSON.
    """
    # Implementation...


def attach_screenshot(screenshot_bytes: bytes, name: str = "Screenshot") -> None:
    """Attach a screenshot to the Allure report."""
    # Implementation...


def attach_json(data: Dict[str, Any], name: str = "JSON Data") -> None:
    """Attach JSON data to the Allure report."""
    # Implementation...


def set_environment_info(env_data: Dict[str, str]) -> None:
    """Set environment information for the Allure report."""
    # Implementation...


def add_jira_link(issue_key: str) -> None:
    """Add a link to a Jira issue."""
    # Implementation...


def add_test_case_link(test_case_id: str) -> None:
    """Add a link to a test case."""
    # Implementation...
```

**Usage in Step Definitions:**

```python
from core.helpers.allure_helpers import attach_request_response, allure_step

@when(parsers.parse('I send a GET request to "{endpoint}"'))
def send_get_request(bdd_context, jsonplaceholder_client, endpoint):
    """Send GET request with automatic Allure attachment."""
    with allure.step(f"Send GET request to {endpoint}"):
        response = jsonplaceholder_client.get(endpoint)
        bdd_context.response = response

        # Automatic request/response attachment
        attach_request_response(response)
```

### 7. Metrics Collection System

**Components:**
- `core/helpers/metrics_collector.py` - Metrics collection engine
- `core/helpers/pytest_metrics_plugin.py` - Automatic pytest plugin
- `core/helpers/metrics_reporter.py` - Report and dashboard generation

**Features:**
- Automatic collection via pytest hooks (no manual instrumentation)
- Pass/fail rate tracking
- Execution time analysis
- Flakiness detection
- API endpoint coverage tracking
- Historical trend analysis
- HTML dashboard generation
- Markdown report generation
- ROI calculations

**Automatic Integration:**

The metrics plugin is automatically loaded by pytest and requires no configuration:

```python
# pytest_metrics_plugin.py
def pytest_configure(config):
    """Register metrics collector plugin."""
    collector = MetricsCollector()
    config.pluginmanager.register(collector, "metrics_collector")

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Display metrics summary after test run."""
    # Automatic summary display...
```

**Generated Outputs:**
- `reports/metrics/dashboard.html` - Interactive HTML dashboard
- `reports/metrics/summary.md` - Markdown summary report
- `reports/metrics/metrics.json` - Raw metrics data
- Console output with key metrics after test run

### 8. Test Explorer Troubleshooting Guide

**Location:** `COMO_VER_TESTES_BDD.md`

Comprehensive guide for resolving Test Explorer issues:

**Contents:**
1. Status verification checklist
2. Step-by-step refresh procedures
3. Cache clearing instructions
4. Configuration verification
5. Python interpreter selection
6. Extension troubleshooting
7. Manual verification commands
8. Expected directory structure
9. Common error solutions

**Example Usage:**

```bash
# Verify BDD tests are discoverable
pytest --collect-only tests/bdd/ -q

# Clear pytest cache
rmdir /s /q .pytest_cache
rmdir /s /q tests\bdd\__pycache__

# Refresh Test Explorer
Ctrl+Shift+P → "Test: Refresh Tests"
```

### 9. Extended Marker System

**Location:** `pytest.ini`

**Total Markers:** 50+ (20 original + 30+ BDD-specific)

**BDD-Specific Markers:**
```ini
bdd: BDD tests written in Gherkin syntax
get: HTTP GET request tests
post: HTTP POST request tests
put: HTTP PUT request tests
delete: HTTP DELETE request tests
filter: Query filtering and parameter tests
list: List/collection endpoint tests
nested: Nested resource endpoint tests
data_creation: Tests for creating test data in database
data_validation: Tests for validating database data
data_cleanup: Tests demonstrating automatic test data cleanup
query: Database query tests
advanced: Advanced database operations
bulk: Bulk data operations
profile: User profile related tests
state: Database state validation tests
end_to_end: End-to-end integration tests
negative: Negative test cases
id: ID-based query tests
api_integration: Tests combining API and database operations
table: Tests using data tables
data_flow: Tests demonstrating data flow through steps
multi_step: Tests with multiple sequential steps
data_sharing: Tests demonstrating context data sharing
complex: Complex workflow tests
multiple_entities: Tests with multiple database entities
sequential: Sequential operation tests
full_cycle: Full CRUD cycle tests
context: Tests demonstrating bdd_context usage
error_handling: Error handling and validation tests
```

**Tag-to-Marker Conversion:**

pytest-bdd automatically converts Gherkin tags to pytest markers:

```gherkin
@smoke @backend @api @get @list
Feature: JSONPlaceholder Posts API

  Scenario: Get all posts
    # This scenario will have markers: smoke, backend, api, get, list
```

**Usage:**
```bash
# Run only smoke BDD tests
pytest -m "smoke and bdd"

# Run API GET tests
pytest -m "get and api"

# Run complex integration tests
pytest -m "complex and end_to_end"
```

## Implementation Statistics

### BDD Tests Implemented

**Total:** 92 BDD tests across 8 test files

**Breakdown:**
- **API Tests:** 46 scenarios
  - `test_posts_api.py` - 16 tests
  - `test_users_api.py` - 30 tests

- **Database Tests:** 19 scenarios
  - `test_data_management.py` - 14 tests
  - `test_database_steps.py` - 5 tests

- **Integration Tests:** 9 scenarios
  - `test_end_to_end_integration.py` - 9 tests

- **Validation Tests:** 18 scenarios
  - `test_api_steps_validation.py` - 3 tests
  - `test_explorer_verification.py` - 13 tests
  - `test_bdd_context.py` - 2 tests

### Feature Files Created

- `features/api/posts.feature` - 16 scenarios
- `features/api/users.feature` - 30 scenarios
- `features/database/data_management.feature` - 14 scenarios
- `features/integration/end_to_end.feature` - 9 scenarios

### Step Definitions Implemented

- `steps/api_steps.py` - 928 lines, ~40 step definitions
- `steps/database_steps.py` - Database CRUD steps
- `steps/common_steps.py` - Setup and configuration steps
- `steps/assertions_steps.py` - Validation steps

### Documentation Files Created

1. `tests/bdd/README.md` - Complete BDD guide (1456 lines, 44KB)
2. `tests/bdd/TEST_EXPLORER_VERIFICATION.md` - Test Explorer verification
3. `COMO_VER_TESTES_BDD.md` - Troubleshooting guide (219 lines)
4. Updated main `README.md` with BDD section

## Quality Metrics

### Code Coverage
- Step definitions cover all common testing patterns
- Reusable steps minimize duplication
- All fixtures integrated (api_client, db_manager, test_data_factory)

### Test Organization
- Clear directory structure
- Logical feature grouping
- Comprehensive tagging system
- Multiple execution modes supported

### Maintainability
- Extensive documentation
- Clear naming conventions
- Modular step definitions
- Fixture-based dependency injection
