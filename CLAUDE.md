# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python-IQ is a comprehensive test automation framework for functional testing of backend (API) and frontend (UI) applications. The framework uses pytest as the test runner, Playwright for UI automation, SQLAlchemy for database integration, and Pydantic for data validation.

**Current Status:** The framework is production-ready with 85% completion. Core features are fully implemented including API testing, UI automation, database integration, Allure reporting, and VS Code Test Explorer integration. Optional features like CI/CD pipelines and Zephyr Scale integration are planned but not yet implemented.

## Project Structure

```
qa-automation/
├── core/                       # Framework core components
│   ├── api/                    # API client and endpoints
│   ├── config/                 # Configuration management (Settings with Pydantic)
│   ├── database/               # Database integration (SQLAlchemy)
│   │   ├── manager.py          # Database connection manager with pooling
│   │   ├── factory.py          # Test data factory pattern
│   │   ├── models.py           # SQLAlchemy ORM models
│   │   └── fixtures.py         # Database fixtures
│   ├── helpers/                # Validators and data generators (Faker)
│   ├── models/                 # Pydantic data models for API validation
│   └── ui/                     # UI automation components (Playwright)
├── tests/                      # Test suites
│   ├── backend/                # API tests
│   ├── frontend/               # UI tests (Page Objects)
│   ├── integration/            # End-to-end tests with database
│   └── conftest.py             # Global fixtures
├── fixtures/                   # Test data and fixtures
│   ├── sql/                    # SQL scripts for test data
│   └── json/                   # JSON test data files
├── scripts/                    # Utility scripts
└── reports/                    # Generated reports (Allure)
```

## Key Technologies

- **Test Runner**: pytest with markers (smoke, regression, backend, frontend, slow, integration)
- **API Testing**: requests library with retry logic and session management
- **UI Automation**: Playwright (supports Chromium, Firefox, WebKit)
- **Data Validation**: Pydantic models for type safety and schema validation
- **Database**: SQLAlchemy ORM (equivalent to Entity Framework in .NET)
- **Test Data**: Faker for generating Brazilian-localized test data (CPF, phone, etc.)
- **Reporting**: Allure with Jira integration
- **Test Management**: Zephyr Scale integration for result synchronization

## Running Tests

### Common Commands

```bash
# Run smoke tests
pytest -m smoke

# Run backend API tests
pytest -m backend

# Run frontend UI tests
pytest -m frontend

# Run regression suite
pytest -m regression

# Run with parallel execution (backend)
pytest -m backend -n 4

# Run specific test file
pytest tests/backend/test_authentication.py

# Run with detailed logging
pytest -v --log-cli-level=DEBUG

# Generate Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Environment Configuration

The framework uses Pydantic Settings for configuration management:
- Create `.env` file from `.env.example`
- Supports multiple environments: dev, staging, prod
- Configuration includes: API URLs, database credentials, browser settings, authentication tokens

## Architecture Guidelines

### Database Integration Pattern

The framework uses SQLAlchemy ORM for database operations:

1. **Connection Management**: DatabaseManager with connection pooling and context managers for automatic rollback
2. **Test Data Factory**: Creates complex test data scenarios with related entities (users, profiles, orders)
3. **Cleanup Strategy**: Automatic cleanup of test data using test_id tracking
4. **Transaction Isolation**: Each test runs in isolated session with rollback support

**Example test pattern**:
```python
def test_complete_workflow(test_data_context, db_manager, test_data_factory, api_client):
    # 1. Create test data
    user_data = test_data_factory.create_user_with_profile(test_data_context.test_id)

    # 2. Verify data readiness
    with db_manager.get_session() as session:
        user = session.query(User).filter(User.id == user_data.user.id).first()
        assert user is not None

    # 3. Execute API calls
    response = api_client.post(f"/users/{user_data.user.id}/activate")

    # 4. Validate changes in database
    with db_manager.get_session() as session:
        updated_user = session.query(User).filter(User.id == user_data.user.id).first()
        assert updated_user.is_active is True

    # 5. Cleanup is automatic via test_data_context fixture
```

### API Testing Pattern

- **APIClient**: Centralized HTTP client with retry logic, automatic authentication, and request/response logging
- **Pydantic Models**: All API requests/responses use Pydantic models for validation
- **Fixtures**: `api_client()` fixture provides authenticated session
- **Validators**: Helper functions for status code, response time, and schema validation

### Frontend Testing Pattern

- **Page Object Model**: Each page has a dedicated class with locators and actions
- **BasePage**: Common functionality (click, fill, wait_for_selector, screenshot capture)
- **Browser Support**: Multi-browser testing (Chromium, Firefox, WebKit)
- **Fixtures**: `authenticated_page` fixture provides logged-in browser context

### Test Markers

Use pytest markers to categorize tests:
- `@pytest.mark.smoke` - Critical path tests (run on every PR)
- `@pytest.mark.regression` - Full test suite (run on push to main)
- `@pytest.mark.backend` - API tests
- `@pytest.mark.frontend` - UI tests
- `@pytest.mark.slow` - Tests taking >30 seconds
- `@pytest.mark.integration` - End-to-end tests with database

### Parallel Execution

- **Backend tests**: Use `pytest-xdist` with `-n` flag for parallel workers
- **Frontend tests**: Multiple browser instances with isolated contexts
- **Database isolation**: Each test uses unique test_id for data isolation
- Optimal worker count: 2-4 for local, 8+ for CI/CD

## CI/CD Integration

The framework integrates with GitHub Actions:
- **PR triggers**: Smoke tests on Chromium (2 workers)
- **Push to main**: Regression suite on Chrome + Firefox (4 workers)
- **Nightly schedule**: Full suite on all browsers (8 workers)
- **Artifacts**: Allure reports, screenshots, videos, JUnit XML
- **Notifications**: Slack notifications on failures
- **Zephyr Sync**: Automatic test result synchronization

## Data Generation

Use Faker for Brazilian-localized test data:
- CPF, phone numbers, addresses
- Secure password generation
- Integration with TestDataFactory for database records
- Consistent data across test runs

## Reporting

- **Allure**: Rich HTML reports with steps, attachments, screenshots
- **Zephyr Scale**: Bi-directional sync with test management tool
- **Metrics**: Pass/fail rates, flakiness detection, execution time trends
- **Traceability**: Jira ticket links via `@allure.link()`

## Development Notes

- Framework language: Portuguese (requirements and documentation in PT-BR)
- Test data: Brazilian locale (pt_BR)
- Database: PostgreSQL primary target, supports MySQL, SQL Server, SQLite
- Python version: 3.11+
- Project status: **85% Complete - Production Ready** (core framework fully implemented, CI/CD and Zephyr Scale are optional future additions)
