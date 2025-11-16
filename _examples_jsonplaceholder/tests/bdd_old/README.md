# BDD Integration Guide

## Overview

This directory contains the Behavior-Driven Development (BDD) integration for the Python test automation framework. BDD allows you to write tests in natural language using Gherkin syntax, making tests readable and understandable by both technical and non-technical stakeholders.

The BDD integration uses **pytest-bdd** to enable Gherkin feature files while maintaining full compatibility with:
- Existing pytest infrastructure
- Allure reporting
- Database fixtures and test data management
- API client capabilities
- Test Explorer UI
- Parallel test execution

### Key Benefits

- **Business-Readable Tests**: Write tests in plain English using Given-When-Then syntax
- **Collaboration**: Enable product owners, QA, and developers to collaborate on test scenarios
- **Reusable Steps**: Build a library of step definitions that can be combined in different ways
- **Full Integration**: Leverage all existing framework features (fixtures, Allure, database, API client)
- **Flexible Execution**: Run tests via CLI, Test Explorer, or CI/CD pipelines

## Directory Structure

```
tests/bdd/
├── README.md                    # This file - BDD documentation
├── conftest.py                  # BDD-specific fixtures (bdd_context)
├── features/                    # Gherkin feature files
│   ├── api/                     # API testing scenarios
│   │   ├── posts.feature
│   │   ├── users.feature
│   │   └── comments.feature
│   ├── database/                # Database testing scenarios
│   │   └── data_management.feature
│   └── integration/             # End-to-end integration scenarios
│       └── end_to_end.feature
└── steps/                       # Step definitions (Python implementations)
    ├── __init__.py
    ├── common_steps.py          # Common setup steps
    ├── api_steps.py             # API-related steps
    ├── database_steps.py        # Database-related steps
    └── assertions_steps.py      # Assertion/validation steps
```

### Directory Conventions

- **features/**: Organize feature files by functional area (api, database, integration, etc.)
- **steps/**: Group step definitions by type (api, database, common, assertions)
- **Feature files**: Use `.feature` extension and descriptive names (e.g., `posts.feature`)
- **Step files**: Use `_steps.py` suffix (e.g., `api_steps.py`)

## Writing Feature Files

Feature files use Gherkin syntax to describe test scenarios in a structured, readable format.

### Basic Structure

```gherkin
@tag1 @tag2
Feature: Feature Name
  As a [role]
  I want [feature]
  So that [benefit]

  Background:
    Given [common setup step]
    And [another setup step]

  @scenario_tag
  Scenario: Scenario description
    Given [precondition]
    When [action]
    Then [expected result]
    And [additional validation]
```

### Gherkin Keywords

- **Feature**: High-level description of the functionality being tested
- **Background**: Steps that run before each scenario in the feature
- **Scenario**: A specific test case with Given-When-Then steps
- **Scenario Outline**: Template scenario that runs multiple times with different data
- **Examples**: Data table for Scenario Outline
- **Given**: Preconditions and setup
- **When**: Actions or events
- **Then**: Expected outcomes and assertions
- **And/But**: Additional steps of the same type

### Tags

Tags are used to categorize and filter scenarios:

```gherkin
@smoke @backend @api
Feature: API Testing
```

Common tags:
- `@smoke`: Critical tests that should always pass
- `@backend`: Backend/API tests
- `@frontend`: UI tests
- `@database`: Database tests
- `@integration`: Integration tests
- `@crud`: Create/Read/Update/Delete operations
- `@validation`: Data validation tests

Tags are automatically converted to pytest markers, allowing you to filter tests:
```bash
pytest -m "smoke and backend"
```

### Example: Simple API Test

```gherkin
@smoke @api
Feature: Posts API
  As a QA engineer
  I want to test the Posts API
  So that I can ensure it works correctly

  Background:
    Given the API client is configured

  @crud @get
  Scenario: Get all posts
    When I send a GET request to "/posts"
    Then the response status code should be 200
    And the response should be a non-empty list
```

### Example: Scenario Outline with Data Tables

```gherkin
@validation
Scenario Outline: Get post by ID
  When I send a GET request to "/posts/<post_id>"
  Then the response status code should be <status_code>
  
  Examples:
    | post_id | status_code |
    | 1       | 200         |
    | 50      | 200         |
    | 99999   | 404         |
```

### Example: Data Tables in Steps

```gherkin
@crud @post
Scenario: Create a new post
  Given I have post data:
    | field  | value                    |
    | userId | 1                        |
    | title  | Test Post from BDD       |
    | body   | This is a test post body |
  When I send a POST request to "/posts" with the post data
  Then the response status code should be 201
```

## Writing Step Definitions

Step definitions are Python functions that implement the behavior described in Gherkin steps.

### Basic Step Definition

```python
from pytest_bdd import given, when, then
import allure

@given("the API client is configured")
def api_client_configured(jsonplaceholder_client):
    """Ensure API client is available."""
    assert jsonplaceholder_client is not None
    allure.attach(
        jsonplaceholder_client.base_url,
        "API Base URL",
        allure.attachment_type.TEXT
    )
```

### Step Definition with Parameters

Use `parsers.parse()` for parameterized steps:

```python
from pytest_bdd import when, parsers

@when(parsers.parse('I send a GET request to "{endpoint}"'))
def send_get_request(bdd_context, jsonplaceholder_client, endpoint):
    """Send GET request to endpoint."""
    with allure.step(f"Send GET request to {endpoint}"):
        response = jsonplaceholder_client.get(endpoint)
        bdd_context.response = response
```

### Step Definition with Data Tables

Parse data tables in step definitions:

```python
@given(parsers.parse('I have post data:\n{data_table}'))
def post_data(bdd_context, data_table):
    """Parse post data from table."""
    data = {}
    for line in data_table.strip().split('\n')[1:]:  # Skip header
        if '|' in line:
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) == 2:
                field, value = parts
                data[field] = int(value) if value.isdigit() else value
    
    bdd_context.post_data = data
```

### Step Definition Best Practices

1. **Keep steps focused**: Each step should do one thing
2. **Use descriptive names**: Function names should describe what the step does
3. **Add docstrings**: Document what the step does and its parameters
4. **Use Allure steps**: Wrap logic in `allure.step()` for better reporting
5. **Store data in context**: Use `bdd_context` to share data between steps
6. **Reuse fixtures**: Leverage existing pytest fixtures (api_client, db_manager, etc.)
7. **Handle errors gracefully**: Provide clear error messages in assertions

## Fixture Usage in Steps

Step definitions can use any pytest fixture by including it as a parameter.

### Available Fixtures

#### BDD-Specific Fixtures

**bdd_context** (function-scoped)
- Purpose: Share data between steps within a scenario
- Usage: Store API responses, test data, database results
- Example:
  ```python
  @when("I send a GET request")
  def send_request(bdd_context, api_client):
      response = api_client.get("/posts")
      bdd_context.response = response  # Store for later steps
  
  @then("the response should be valid")
  def check_response(bdd_context):
      assert bdd_context.response.status_code == 200
  ```

#### API Fixtures

**jsonplaceholder_client** (session-scoped)
- Purpose: JSONPlaceholder API client
- Methods: `get()`, `post()`, `put()`, `delete()`
- Example:
  ```python
  @when("I call the API")
  def call_api(jsonplaceholder_client):
      response = jsonplaceholder_client.get("/posts/1")
  ```

**api_client** (session-scoped)
- Purpose: Generic API client with authentication
- Methods: `get()`, `post()`, `put()`, `delete()`, `is_authenticated()`

#### Database Fixtures

**db_manager** (session-scoped)
- Purpose: Database connection manager
- Methods: `get_session()`, `execute_query()`
- Example:
  ```python
  @when("I query the database")
  def query_db(db_manager):
      with db_manager.get_session() as session:
          result = session.execute("SELECT * FROM users")
  ```

**test_data_factory** (session-scoped)
- Purpose: Create test data with automatic cleanup
- Methods: `create_user_data()`, `create_post_data()`
- Example:
  ```python
  @given("I have a test user")
  def create_user(test_data_factory, test_data_context):
      user = test_data_factory.create_user_data(
          test_id=test_data_context.test_id,
          email="test@example.com"
      )
  ```

**test_data_context** (function-scoped)
- Purpose: Track test data for automatic cleanup
- Attributes: `test_id`, `created_entities`

#### Configuration Fixtures

**settings** (session-scoped)
- Purpose: Application settings and configuration
- Attributes: `env`, `api_base_url`, `db_host`, `auth_user`, etc.

### Fixture Injection Example

```python
@given("I have a test user with email")
def create_test_user(
    bdd_context,           # BDD context for data sharing
    test_data_factory,     # Factory to create test data
    test_data_context,     # Context for cleanup tracking
    db_manager,            # Database manager
    settings               # Application settings
):
    """Create a test user in the database."""
    user_data = test_data_factory.create_user_data(
        test_id=test_data_context.test_id,
        email="test@example.com"
    )
    bdd_context.user_data = user_data
```

## BDD Context for Data Sharing

The `bdd_context` fixture is a special object for sharing data between steps within a scenario.

### Using BDD Context

```python
# Step 1: Store data
@given("I have some data")
def store_data(bdd_context):
    bdd_context.my_data = {"key": "value"}
    bdd_context.user_id = 123

# Step 2: Retrieve data
@when("I process the data")
def process_data(bdd_context):
    data = bdd_context.my_data
    user_id = bdd_context.user_id
    # Process...
    bdd_context.result = processed_data

# Step 3: Validate data
@then("the result should be correct")
def verify_result(bdd_context):
    assert bdd_context.result == expected_value
```

### BDD Context Methods

- `bdd_context.attribute = value`: Store data
- `value = bdd_context.attribute`: Retrieve data
- `bdd_context.get('attribute', default)`: Get with default
- `bdd_context.has('attribute')`: Check if exists
- `bdd_context.clear()`: Clear all data (automatic after scenario)

### Common Context Attributes

- `bdd_context.response`: API response object
- `bdd_context.post_data`: Data for POST requests
- `bdd_context.user_data`: User data from database
- `bdd_context.db_result`: Database query results
- `bdd_context.created_id`: ID of created resource

### Context Isolation

Each scenario gets a fresh `bdd_context` instance, ensuring complete isolation between tests. The context is automatically cleared after each scenario.

## Available Step Definitions

### Common Steps (common_steps.py)

```gherkin
Given the API client is configured
Given I am authenticated
Given the database is connected and ready
```

### API Steps (api_steps.py)

```gherkin
# GET requests
When I send a GET request to "/endpoint"

# POST requests
Given I have post data:
  | field | value |
When I send a POST request to "/endpoint" with the post data

# PUT requests
When I send a PUT request to "/endpoint" with the post data

# DELETE requests
When I send a DELETE request to "/endpoint"
```

### Database Steps (database_steps.py)

```gherkin
# Create test data
Given I have a test user with email "user@example.com"
Given I have a test user with username "testuser"
Given I have a test user with profile
Given I have {count} test users

# Query database
When I query the database for user with email "user@example.com"
When I query the database for user with username "testuser"
When I query the database for user with id {user_id}
When I query all users from the database
When I execute SQL query:
  """
  SELECT * FROM users WHERE active = true
  """

# Validate database
Then the user should exist in the database
Then the user should not exist in the database
Then the user should be active
Then the user should have field "email" equal to "user@example.com"
Then the database should contain at least {count} users
Then each user should have a valid email
```

### Assertion Steps (assertions_steps.py)

```gherkin
# Status code
Then the response status code should be {code}

# Response type
Then the response should be a list
Then the response should be a non-empty list
Then the response should be a dictionary

# Field validation
Then the response should contain field "fieldName"
Then the response field "fieldName" should equal "value"
Then the response list should have at least {count} items

# Required fields
Then each post should have required fields:
  | userId |
  | id     |
  | title  |
```

## Integration with Existing Framework

### API Client Integration

BDD steps use the existing `jsonplaceholder_client` fixture:

```python
@when(parsers.parse('I send a GET request to "{endpoint}"'))
def send_get_request(bdd_context, jsonplaceholder_client, endpoint):
    response = jsonplaceholder_client.get(endpoint)
    bdd_context.response = response
```

The API client provides:
- Automatic base URL configuration
- Request/response logging
- Error handling
- Session management

### Database Integration

BDD steps use existing database fixtures:

```python
@given("I have a test user")
def create_user(test_data_factory, test_data_context):
    user = test_data_factory.create_user_data(
        test_id=test_data_context.test_id,
        email="test@example.com"
    )
```

Database integration provides:
- Automatic connection management
- Test data isolation
- Automatic cleanup after tests
- Transaction rollback on failure

### Allure Integration

BDD scenarios automatically integrate with Allure reporting:

```python
@when("I perform an action")
def perform_action(bdd_context):
    with allure.step("Detailed step description"):
        # Step implementation
        allure.attach(data, "Attachment Name", allure.attachment_type.JSON)
```

Allure features:
- Feature files → Allure Features
- Scenarios → Allure Test Cases
- Given/When/Then → Allure Steps
- Tags → Allure Labels
- Automatic attachments for API requests/responses
- Context data attached to reports

## Example: Complete Feature File

```gherkin
@smoke @integration @end_to_end
Feature: End-to-End User Workflow
  As a QA engineer
  I want to test complete user workflows
  So that I can ensure the system works correctly

  Background:
    Given the API client is configured
    And the database is connected and ready

  @crud @data_flow
  Scenario: Create user and validate via API
    # Setup: Create user in database
    Given I have a test user with email "workflow@example.com"
    When I query the database for user with email "workflow@example.com"
    Then the user should exist in the database
    And the user should be active
    
    # Action: Call API
    When I send a GET request to "/posts"
    Then the response status code should be 200
    And the response should be a non-empty list
    
    # Validation: Verify database state
    When I query the database for user with email "workflow@example.com"
    Then the user should exist in the database

  @multi_step @data_sharing
  Scenario: Multi-step API workflow
    # Step 1: Create post
    Given I have post data:
      | field  | value              |
      | userId | 1                  |
      | title  | Workflow Test Post |
      | body   | Testing workflow   |
    When I send a POST request to "/posts" with the post data
    Then the response status code should be 201
    And the response should contain field "id"
    
    # Step 2: Update post
    Given I have post data:
      | field  | value                |
      | userId | 1                    |
      | id     | 101                  |
      | title  | Updated Post         |
      | body   | Updated content      |
    When I send a PUT request to "/posts/101" with the post data
    Then the response status code should be 200
    And the response field "title" should equal "Updated Post"
    
    # Step 3: Delete post
    When I send a DELETE request to "/posts/101"
    Then the response status code should be 200
```

## Next Steps

1. **Explore Examples**: Review the feature files in `features/` directory
2. **Run Tests**: See execution instructions in the next section
3. **Write Your Own**: Create new feature files and step definitions
4. **Extend Steps**: Add new step definitions to the `steps/` directory
5. **Integrate**: Use BDD tests alongside existing pytest tests

For execution instructions, see the "Running BDD Tests" section below.

## Running BDD Tests

### Prerequisites

Ensure pytest-bdd is installed:
```bash
pip install pytest-bdd
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### Command Line Execution

#### Run All BDD Tests

```bash
# Run all tests in the BDD directory
pytest tests/bdd/

# Run with verbose output
pytest tests/bdd/ -v

# Run with detailed output
pytest tests/bdd/ -vv
```

#### Run Specific Feature Files

```bash
# Run a specific feature file
pytest tests/bdd/features/api/posts.feature

# Run all features in a directory
pytest tests/bdd/features/api/

# Run multiple specific features
pytest tests/bdd/features/api/posts.feature tests/bdd/features/database/data_management.feature
```

#### Run Specific Scenarios

```bash
# Run a specific scenario by name
pytest tests/bdd/features/api/posts.feature -k "Get all posts"

# Run scenarios matching a pattern
pytest tests/bdd/features/api/posts.feature -k "Create"
```

### Filtering Tests with Markers

BDD scenarios support pytest markers through Gherkin tags.

#### Run Tests by Tag

```bash
# Run all smoke tests
pytest tests/bdd/ -m smoke

# Run all API tests
pytest tests/bdd/ -m api

# Run all database tests
pytest tests/bdd/ -m database

# Run all integration tests
pytest tests/bdd/ -m integration
```

#### Combine Multiple Markers

```bash
# Run smoke tests that are also backend tests
pytest tests/bdd/ -m "smoke and backend"

# Run API or database tests
pytest tests/bdd/ -m "api or database"

# Run smoke tests but exclude slow tests
pytest tests/bdd/ -m "smoke and not slow"

# Run CRUD operations that are smoke tests
pytest tests/bdd/ -m "crud and smoke"
```

#### Common Marker Combinations

```bash
# Critical API tests
pytest tests/bdd/ -m "smoke and api"

# All CRUD operations
pytest tests/bdd/ -m crud

# End-to-end integration tests
pytest tests/bdd/ -m "integration and end_to_end"

# Backend tests excluding database
pytest tests/bdd/ -m "backend and not database"
```

### Parallel Execution

BDD tests support parallel execution using pytest-xdist for faster test runs.

#### Install pytest-xdist

```bash
pip install pytest-xdist
```

#### Run Tests in Parallel

```bash
# Run with automatic worker count (recommended)
pytest tests/bdd/ -n auto

# Run with specific number of workers
pytest tests/bdd/ -n 4

# Run in parallel with verbose output
pytest tests/bdd/ -n auto -v

# Run specific markers in parallel
pytest tests/bdd/ -m smoke -n auto
```

#### Parallel Execution Notes

- Each worker gets its own database session and test data context
- Test data isolation is maintained through `test_data_context` fixture
- BDD context is function-scoped, ensuring no data sharing between parallel tests
- Recommended for large test suites to reduce execution time

### Allure Report Generation

Generate Allure reports for BDD tests with detailed step-by-step execution.

#### Generate Allure Results

```bash
# Run tests and generate Allure results
pytest tests/bdd/ --alluredir=reports/allure-results

# Run with markers and generate results
pytest tests/bdd/ -m smoke --alluredir=reports/allure-results

# Run in parallel and generate results
pytest tests/bdd/ -n auto --alluredir=reports/allure-results
```

#### View Allure Report

```bash
# Generate and open Allure report
allure serve reports/allure-results

# Generate static report
allure generate reports/allure-results -o reports/allure-report --clean

# Open existing report
allure open reports/allure-report
```

#### Allure Report Features for BDD

- **Features**: Feature files appear as Allure features
- **Scenarios**: Each scenario is a separate test case
- **Steps**: Given/When/Then steps shown with execution details
- **Attachments**: API requests/responses, database queries, context data
- **Tags**: Gherkin tags appear as Allure labels for filtering
- **Timeline**: Visual timeline of test execution
- **Graphs**: Test distribution by feature, severity, and status

### Test Explorer Integration

BDD tests are fully integrated with VS Code Test Explorer and other IDE test runners.

#### Discover Tests

1. Open VS Code
2. Open the Test Explorer panel (Testing icon in sidebar)
3. BDD scenarios appear as individual test items
4. Tests are grouped by feature file

#### Run Tests from Test Explorer

- **Run Single Scenario**: Click ▶️ next to a scenario
- **Run Feature File**: Click ▶️ next to a feature file
- **Run All BDD Tests**: Click ▶️ next to the `tests/bdd` folder
- **Run with Debugging**: Click 🐛 to debug with breakpoints

#### Test Explorer Features

- **Visual Feedback**: ✓ for passed tests, ✗ for failed tests
- **Inline Results**: See pass/fail status directly in the tree
- **Error Messages**: View failure details inline
- **Quick Navigation**: Click on test to open feature file
- **Filtering**: Filter by status (passed, failed, skipped)
- **Refresh**: Auto-refresh when files change

#### Debug BDD Tests

1. Set breakpoints in step definition files (`.py` files in `steps/`)
2. Click 🐛 debug button next to a scenario in Test Explorer
3. Debugger stops at breakpoints in step implementations
4. Inspect variables, context data, and fixture values
5. Step through code execution

### CI/CD Integration

BDD tests integrate seamlessly with CI/CD pipelines.

#### GitHub Actions Example

```yaml
name: BDD Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run BDD smoke tests
        run: |
          pytest tests/bdd/ -m smoke --alluredir=reports/allure-results
      
      - name: Generate Allure report
        if: always()
        run: |
          allure generate reports/allure-results -o reports/allure-report
      
      - name: Upload Allure report
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: allure-report
          path: reports/allure-report
```

#### Jenkins Pipeline Example

```groovy
pipeline {
    agent any
    
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Run BDD Tests') {
            steps {
                sh 'pytest tests/bdd/ -m smoke --alluredir=reports/allure-results'
            }
        }
        
        stage('Generate Report') {
            steps {
                allure includeProperties: false,
                       jdk: '',
                       results: [[path: 'reports/allure-results']]
            }
        }
    }
}
```

### Output and Reporting

#### Console Output

```bash
# Standard output
pytest tests/bdd/ -v

# Output with step details
pytest tests/bdd/ -vv

# Output with print statements
pytest tests/bdd/ -v -s

# Quiet mode (minimal output)
pytest tests/bdd/ -q
```

#### HTML Report

```bash
# Generate HTML report
pytest tests/bdd/ --html=reports/bdd_report.html --self-contained-html
```

#### JUnit XML Report

```bash
# Generate JUnit XML for CI/CD
pytest tests/bdd/ --junitxml=reports/junit.xml
```

### Troubleshooting

#### Tests Not Discovered

```bash
# Check pytest collection
pytest tests/bdd/ --collect-only

# Verify feature files are found
pytest tests/bdd/features/ --collect-only

# Check for syntax errors in feature files
pytest tests/bdd/ -v
```

#### Step Definition Not Found

- Ensure step definitions are imported in `tests/bdd/conftest.py`
- Check that step text exactly matches between feature file and step definition
- Verify parsers are used correctly for parameterized steps

#### Fixture Not Available

- Check that fixtures are defined in `conftest.py` files
- Verify `pytest_plugins` includes necessary modules
- Ensure fixture scope is appropriate (function, session, etc.)

#### Parallel Execution Issues

- Verify test data isolation using `test_data_context`
- Check for shared state between tests
- Ensure database transactions are properly managed

### Performance Tips

1. **Use Parallel Execution**: Run with `-n auto` for faster execution
2. **Filter Tests**: Use markers to run only relevant tests
3. **Session Fixtures**: Leverage session-scoped fixtures for expensive setup
4. **Database Optimization**: Use test data factory for efficient data creation
5. **Selective Reporting**: Generate Allure reports only when needed

### Example Commands

```bash
# Quick smoke test run
pytest tests/bdd/ -m smoke -v

# Full test run with report
pytest tests/bdd/ --alluredir=reports/allure-results -v

# Parallel smoke tests with report
pytest tests/bdd/ -m smoke -n auto --alluredir=reports/allure-results

# Debug specific scenario
pytest tests/bdd/features/api/posts.feature -k "Create a new post" -vv -s

# Run integration tests in parallel
pytest tests/bdd/ -m integration -n 4 -v

# Generate comprehensive report
pytest tests/bdd/ --alluredir=reports/allure-results --html=reports/bdd.html
allure serve reports/allure-results
```

## Framework Integration Details

### How BDD Uses API Client

BDD step definitions leverage the existing API client infrastructure for making HTTP requests.

#### JSONPlaceholder Client

The `jsonplaceholder_client` fixture provides a pre-configured client for the JSONPlaceholder API:

```python
# In step definition (api_steps.py)
@when(parsers.parse('I send a GET request to "{endpoint}"'))
def send_get_request(bdd_context, jsonplaceholder_client, endpoint):
    """Send GET request using existing API client."""
    with allure.step(f"Send GET request to {endpoint}"):
        # Uses the existing JSONPlaceholder client
        response = jsonplaceholder_client.get(endpoint)
        
        # Store response in context for later steps
        bdd_context.response = response
        
        # Attach to Allure report
        allure.attach(
            response.text,
            "Response Body",
            allure.attachment_type.JSON
        )
```

#### API Client Features Used by BDD

1. **Automatic Base URL**: Client is pre-configured with base URL from settings
2. **Session Management**: Reuses HTTP session for better performance
3. **Request Logging**: All requests are automatically logged
4. **Error Handling**: Built-in error handling and retries
5. **Authentication**: Supports authentication when configured

#### Generic API Client

For APIs requiring authentication, use the `api_client` fixture:

```python
@given("I am authenticated")
def authenticated(api_client, settings):
    """Use generic API client with authentication."""
    # API client automatically handles authentication
    # based on settings (Basic, Bearer, API Key)
    assert api_client.is_authenticated() or settings.auth_user
```

#### Reusing API Client in New Steps

To create new API-related steps:

```python
from pytest_bdd import when, parsers
import allure

@when(parsers.parse('I send a PATCH request to "{endpoint}"'))
def send_patch_request(bdd_context, jsonplaceholder_client, endpoint):
    """Example: Add new HTTP method step."""
    with allure.step(f"Send PATCH request to {endpoint}"):
        data = bdd_context.get('patch_data', {})
        response = jsonplaceholder_client.client.patch(endpoint, json=data)
        bdd_context.response = response
        
        allure.attach(
            response.text,
            "Response Body",
            allure.attachment_type.JSON
        )
```

### How BDD Uses Database Fixtures

BDD step definitions integrate with the existing database infrastructure for data management and validation.

#### Database Manager

The `db_manager` fixture provides database connection and query capabilities:

```python
# In step definition (database_steps.py)
@when(parsers.parse('I query the database for user with email "{email}"'))
def query_user_by_email(bdd_context, db_manager, email):
    """Query database using existing db_manager."""
    with allure.step(f"Query user with email {email}"):
        # Use db_manager to get a session
        with db_manager.get_session() as session:
            from sqlalchemy import text
            result = session.execute(
                text("SELECT * FROM users WHERE email = :email"),
                {"email": email}
            )
            bdd_context.db_result = result.fetchone()
```

#### Test Data Factory

The `test_data_factory` fixture creates test data with automatic cleanup:

```python
@given(parsers.parse('I have a test user with email "{email}"'))
def create_test_user(bdd_context, test_data_factory, test_data_context, email):
    """Create test user using existing factory."""
    with allure.step(f"Create test user with email {email}"):
        # Factory creates data and registers for cleanup
        user_data = test_data_factory.create_user_data(
            test_id=test_data_context.test_id,
            email=email
        )
        
        # Store in context for later steps
        bdd_context.user_data = user_data
        
        # Attach to Allure report
        allure.attach(
            str(user_data),
            "User Data",
            allure.attachment_type.JSON
        )
```

#### Test Data Context

The `test_data_context` fixture tracks created entities for automatic cleanup:

```python
@given("I have multiple test users")
def create_multiple_users(test_data_factory, test_data_context):
    """Create multiple users with automatic cleanup."""
    users = []
    for i in range(3):
        user = test_data_factory.create_user_data(
            test_id=test_data_context.test_id,
            email=f"user{i}@example.com"
        )
        users.append(user)
        # Entities are automatically tracked for cleanup
```

#### Database Integration Benefits

1. **Automatic Cleanup**: Test data is cleaned up after each scenario
2. **Transaction Management**: Database transactions are properly handled
3. **Connection Pooling**: Efficient connection reuse
4. **Isolation**: Each test gets isolated data via `test_id`
5. **Rollback on Failure**: Failed tests don't leave dirty data

#### Creating Custom Database Steps

```python
from pytest_bdd import given, when, then, parsers
from sqlalchemy import text
import allure

@when(parsers.parse('I execute custom query: {query}'))
def execute_custom_query(bdd_context, db_manager, query):
    """Example: Execute custom SQL query."""
    with allure.step(f"Execute query: {query}"):
        with db_manager.get_session() as session:
            result = session.execute(text(query))
            bdd_context.query_result = result.fetchall()
            
            allure.attach(
                query,
                "SQL Query",
                allure.attachment_type.TEXT
            )

@then(parsers.parse('the query should return {count:d} records'))
def verify_query_count(bdd_context, count):
    """Example: Verify query result count."""
    with allure.step(f"Verify query returned {count} records"):
        actual_count = len(bdd_context.query_result)
        assert actual_count == count, \
            f"Expected {count} records, got {actual_count}"
```

### How BDD Integrates with Allure

BDD scenarios automatically integrate with Allure reporting for rich, interactive test reports.

#### Automatic Allure Integration

pytest-bdd automatically creates Allure structure:

```
Feature File → Allure Feature
Scenario → Allure Test Case
Given/When/Then Steps → Allure Steps
Tags → Allure Labels
```

#### Allure Decorators in Step Definitions

Add Allure metadata to step definitions:

```python
import allure
from pytest_bdd import given, when, then

# Module-level decorators
allure.feature("API Testing")
allure.story("Posts Management")

@when("I create a post")
@allure.severity(allure.severity_level.CRITICAL)
def create_post(bdd_context, jsonplaceholder_client):
    """Step with Allure severity."""
    with allure.step("Create post via API"):
        response = jsonplaceholder_client.post("/posts", json={})
        bdd_context.response = response
```

#### Allure Attachments in Steps

Attach data to Allure reports for debugging:

```python
@when("I send a request")
def send_request(bdd_context, jsonplaceholder_client):
    """Step with multiple attachments."""
    with allure.step("Send API request"):
        response = jsonplaceholder_client.get("/posts/1")
        bdd_context.response = response
        
        # Attach request details
        allure.attach(
            "/posts/1",
            "Request URL",
            allure.attachment_type.TEXT
        )
        
        # Attach response
        allure.attach(
            response.text,
            "Response Body",
            allure.attachment_type.JSON
        )
        
        # Attach status code
        allure.attach(
            str(response.status_code),
            "Status Code",
            allure.attachment_type.TEXT
        )
```

#### BDD Context Allure Integration

The `bdd_context` automatically attaches its data to Allure reports:

```python
# Context data is automatically attached after each scenario
# No manual attachment needed - it happens in conftest.py

@when("I store data")
def store_data(bdd_context):
    """Data stored in context is automatically attached to Allure."""
    bdd_context.user_id = 123
    bdd_context.api_response = {"id": 1, "name": "Test"}
    # This data will appear in Allure report as "Scenario Context Data"
```

#### Allure Features Available in BDD

1. **Test Hierarchy**: Features → Test Cases → Steps
2. **Attachments**: Request/response data, screenshots, logs
3. **Labels**: Tags, severity, features, stories
4. **Links**: Link to issues, test cases, documentation
5. **Parameters**: Scenario outline parameters shown in report
6. **Timeline**: Visual timeline of test execution
7. **Graphs**: Distribution by feature, severity, status
8. **History**: Test execution history and trends
9. **Retries**: Retry information for flaky tests
10. **Categories**: Custom failure categorization

#### Custom Allure Integration

Add custom Allure features to steps:

```python
import allure
from pytest_bdd import when, parsers

@when(parsers.parse('I test feature "{feature_name}"'))
@allure.feature("Dynamic Feature")
@allure.link("https://docs.example.com", name="Documentation")
@allure.issue("JIRA-123", name="Related Issue")
def test_feature(feature_name):
    """Step with custom Allure metadata."""
    with allure.step(f"Testing {feature_name}"):
        # Add dynamic label
        allure.dynamic.tag(feature_name)
        allure.dynamic.severity(allure.severity_level.NORMAL)
        
        # Test implementation
        pass
```

### Reusing Existing Components

#### Reusing Pydantic Models

Use existing Pydantic models for response validation:

```python
from core.models.api_models import Post, User
from pytest_bdd import then
import allure

@then("the response should match Post model")
def validate_post_model(bdd_context):
    """Validate response against Pydantic model."""
    with allure.step("Validate response schema"):
        response_data = bdd_context.response.json()
        
        # Use existing Pydantic model for validation
        post = Post(**response_data)
        
        # Attach validated data
        allure.attach(
            post.json(),
            "Validated Post",
            allure.attachment_type.JSON
        )
```

#### Reusing Helper Functions

Use existing helper functions in step definitions:

```python
from core.helpers.allure_helpers import attach_response
from pytest_bdd import when

@when("I make an API call")
def make_api_call(bdd_context, jsonplaceholder_client):
    """Use existing helper functions."""
    response = jsonplaceholder_client.get("/posts/1")
    bdd_context.response = response
    
    # Reuse existing Allure helper
    attach_response(response)
```

#### Reusing Configuration

Access existing configuration in steps:

```python
from pytest_bdd import given

@given("the system is configured")
def check_configuration(settings):
    """Access existing settings."""
    # Settings fixture provides all configuration
    assert settings.env in ["dev", "staging", "prod"]
    assert settings.api_base_url
    assert settings.db_host
    
    # Use configuration in step logic
    if settings.env == "prod":
        # Production-specific logic
        pass
```

#### Reusing Database Models

Use existing SQLAlchemy models:

```python
from core.models.database_models import User, Post
from pytest_bdd import when
from sqlalchemy import select

@when("I query users with ORM")
def query_with_orm(bdd_context, db_manager):
    """Use existing SQLAlchemy models."""
    with db_manager.get_session() as session:
        # Use existing ORM models
        stmt = select(User).where(User.email.like("%@example.com"))
        users = session.execute(stmt).scalars().all()
        bdd_context.users = users
```

### Integration Best Practices

1. **Leverage Existing Fixtures**: Always use existing fixtures instead of creating new ones
2. **Reuse Helper Functions**: Don't duplicate logic that exists in helpers
3. **Follow Naming Conventions**: Match existing naming patterns for consistency
4. **Use Existing Models**: Validate data with existing Pydantic/SQLAlchemy models
5. **Maintain Allure Standards**: Follow existing Allure attachment patterns
6. **Respect Fixture Scopes**: Understand session vs function scope implications
7. **Use Test Data Factory**: Always use factory for test data creation
8. **Follow Error Handling**: Use existing error handling patterns
9. **Maintain Logging**: Use existing logging infrastructure
10. **Document Integration**: Comment how steps integrate with framework

### Example: Complete Integration

Here's a complete example showing integration with all framework components:

```python
"""Example step definition showing complete framework integration."""

import allure
from pytest_bdd import scenario, given, when, then, parsers
from core.models.api_models import Post
from core.helpers.allure_helpers import attach_response

# Scenario definition
@scenario(
    'features/integration/complete_example.feature',
    'Complete integration example'
)
def test_complete_integration():
    """Test demonstrating full framework integration."""
    pass

# Step using API client
@given("I have an API client")
def setup_api_client(jsonplaceholder_client, settings):
    """Use existing API client and settings."""
    assert jsonplaceholder_client is not None
    allure.attach(settings.api_base_url, "API URL", allure.attachment_type.TEXT)

# Step using database fixtures
@given("I have test data in database")
def setup_test_data(test_data_factory, test_data_context, bdd_context):
    """Use existing test data factory."""
    user = test_data_factory.create_user_data(
        test_id=test_data_context.test_id,
        email="integration@example.com"
    )
    bdd_context.user = user

# Step using API client with Allure integration
@when("I fetch a post")
def fetch_post(bdd_context, jsonplaceholder_client):
    """Use API client with Allure helpers."""
    with allure.step("Fetch post from API"):
        response = jsonplaceholder_client.get("/posts/1")
        bdd_context.response = response
        
        # Use existing Allure helper
        attach_response(response)

# Step using Pydantic model validation
@then("the post should be valid")
def validate_post(bdd_context):
    """Use existing Pydantic model."""
    with allure.step("Validate post schema"):
        data = bdd_context.response.json()
        
        # Use existing Pydantic model
        post = Post(**data)
        
        # Attach validated data
        allure.attach(
            post.json(),
            "Validated Post",
            allure.attachment_type.JSON
        )

# Step using database with ORM
@then("the user should exist in database")
def verify_user_in_db(bdd_context, db_manager):
    """Use database manager with ORM."""
    with allure.step("Verify user in database"):
        with db_manager.get_session() as session:
            from sqlalchemy import text
            result = session.execute(
                text("SELECT * FROM users WHERE email = :email"),
                {"email": bdd_context.user["email"]}
            )
            user = result.fetchone()
            assert user is not None
```

This example demonstrates:
- ✅ API client integration
- ✅ Database fixture usage
- ✅ Test data factory
- ✅ Allure reporting
- ✅ Pydantic model validation
- ✅ BDD context for data sharing
- ✅ Existing helper functions
- ✅ Settings configuration

## Summary

The BDD integration seamlessly extends the existing test automation framework by:

1. **Preserving All Features**: All existing framework capabilities remain available
2. **Adding Readability**: Gherkin syntax makes tests business-readable
3. **Enabling Collaboration**: Non-technical stakeholders can understand and contribute
4. **Maintaining Standards**: Follows existing patterns for API, database, and reporting
5. **Providing Flexibility**: Use BDD alongside traditional pytest tests

You can now write tests in natural language while leveraging the full power of the existing framework infrastructure.
