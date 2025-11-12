# API Client Module

Robust HTTP client for test automation with advanced features including automatic retry, authentication management, and detailed logging.

## Features

- ✅ **Session Management**: Persistent HTTP sessions with connection pooling
- ✅ **Automatic Retry**: Configurable retry logic with exponential backoff
- ✅ **Authentication**: Support for Bearer, Basic, OAuth2, and API Key authentication
- ✅ **Token Management**: Automatic token refresh and expiry handling
- ✅ **Detailed Logging**: Comprehensive request/response logging
- ✅ **Request/Response Hooks**: Extensible hook system for custom logic
- ✅ **Context Manager**: Automatic resource cleanup
- ✅ **Type Safety**: Full type hints for better IDE support

## Quick Start

### Basic Usage

```python
from core.api import APIClient

# Create client instance
client = APIClient()

# Make requests
response = client.get("/users")
print(response.json())

# POST request
response = client.post("/users", json={"name": "John", "email": "john@example.com"})
```

### Authentication

```python
from core.api import APIClient

client = APIClient()

# Authenticate with credentials
token = client.authenticate("user@example.com", "password")

# Make authenticated requests
response = client.get("/users/me")
print(response.json())

# Check authentication status
if client.is_authenticated():
    print("Client is authenticated")
```

### Context Manager

```python
from core.api import APIClient

# Automatic session cleanup
with APIClient() as client:
    client.authenticate("user@example.com", "password")
    response = client.get("/users")
    print(response.json())
# Session automatically closed
```

## Configuration

The APIClient uses settings from `core.config.settings.Settings`:

```python
# .env file
API_BASE_URL=https://api.example.com
API_TIMEOUT=30
API_RETRIES=3
AUTH_USER=test@example.com
AUTH_PASSWORD=SecurePassword123!
AUTH_TYPE=bearer
```

### Custom Configuration

```python
from core.api import APIClient

# Override default settings
client = APIClient(
    base_url="https://custom-api.example.com",
    timeout=60,
    retries=5,
    verify_ssl=True
)
```

## Authentication Types

### Bearer Token (JWT)

```python
client = APIClient()
token = client.authenticate("user@example.com", "password")
# Token automatically added to all requests
```

### Basic Authentication

```python
# Set AUTH_TYPE=basic in .env
client = APIClient()
client.authenticate("username", "password")
```

### OAuth2

```python
# Configure OAuth2 in .env
# OAUTH2_CLIENT_ID=your_client_id
# OAUTH2_CLIENT_SECRET=your_secret
# OAUTH2_TOKEN_URL=https://auth.example.com/token

client = APIClient()
client.authenticate("user@example.com", "password")
```

### API Key

```python
# Set AUTH_TYPE=api_key in .env
client = APIClient()
client.authenticate(api_key="your-api-key")
```

## Token Management

### Manual Token Setting

```python
client = APIClient()
client.set_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "Bearer")
```

### Token Refresh

```python
client = APIClient()
client.authenticate("user@example.com", "password")

# Token automatically refreshes when expiring
# Or manually refresh
new_token = client.refresh_token()
```

### Clear Authentication

```python
client.clear_authentication()
```

## Request Methods

All standard HTTP methods are supported:

```python
client.get("/users")
client.post("/users", json={...})
client.put("/users/123", json={...})
client.patch("/users/123", json={...})
client.delete("/users/123")
client.head("/users")
client.options("/users")
```

### Advanced Request Options

```python
response = client.get(
    "/users",
    params={"page": 1, "limit": 10},
    headers={"X-Custom-Header": "value"},
    timeout=60
)
```

## Hooks

Add custom logic before/after requests:

```python
def log_request(method, url, **kwargs):
    print(f"Sending {method} to {url}")

def log_response(response):
    print(f"Received {response.status_code}")

client = APIClient()
client.add_request_hook(log_request)
client.add_response_hook(log_response)
```

## Retry Configuration

Automatic retry with exponential backoff:

```python
# .env configuration
API_RETRIES=3
RETRY_STRATEGY=exponential
RETRY_INITIAL_DELAY=1
RETRY_MAX_DELAY=10
RETRY_BACKOFF_MULTIPLIER=2.0
RETRY_STATUS_CODES=500,502,503,504,429
```

Retries are automatically applied for:
- 5xx server errors
- Connection errors
- Timeout errors
- Configurable status codes (e.g., 429 Too Many Requests)

## Logging

Detailed logging for debugging:

```python
# .env configuration
LOG_LEVEL=DEBUG
LOG_HTTP_REQUESTS=true
```

Logs include:
- Request method, URL, headers, body
- Response status, headers, body
- Request duration
- Retry attempts

## Error Handling

```python
from requests.exceptions import RequestException, Timeout, ConnectionError

client = APIClient()

try:
    response = client.get("/users")
    response.raise_for_status()
except Timeout:
    print("Request timed out")
except ConnectionError:
    print("Connection failed")
except RequestException as e:
    print(f"Request failed: {e}")
```

## Testing with APIClient

### Pytest Fixture

```python
import pytest
from core.api import APIClient

@pytest.fixture
def api_client():
    """Provide authenticated API client."""
    client = APIClient()
    client.authenticate()
    yield client
    client.close()

def test_get_users(api_client):
    response = api_client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) > 0
```

### Test Example

```python
def test_create_user(api_client):
    # Create user
    user_data = {
        "name": "Test User",
        "email": "test@example.com"
    }
    response = api_client.post("/users", json=user_data)
    assert response.status_code == 201
    
    # Verify user created
    user_id = response.json()["id"]
    response = api_client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]
```

## Best Practices

1. **Use Context Manager**: Always use `with` statement for automatic cleanup
2. **Reuse Client**: Create one client instance per test session
3. **Handle Errors**: Always handle potential exceptions
4. **Configure Timeouts**: Set appropriate timeouts for your API
5. **Use Hooks**: Add hooks for common operations (logging, metrics)
6. **Validate Responses**: Always check status codes and response data

## Advanced Features

### Credential Validation

```python
client = APIClient()
is_valid = client.validate_credentials("user@example.com", "password")
if is_valid:
    print("Credentials are valid")
```

### Token Expiry Check

Token expiry is automatically checked before each request. If the token is about to expire (within buffer time), it's automatically refreshed.

```python
# Configure in .env
TOKEN_EXPIRATION_BUFFER=300  # 5 minutes
AUTO_REFRESH_TOKEN=true
```

## Examples

See `core/api/examples.py` for comprehensive usage examples:

```bash
python core/api/examples.py
```

## Requirements

- Python 3.11+
- requests
- urllib3
- pydantic
- pydantic-settings

## Related Modules

- `core.config.settings`: Configuration management
- `core.helpers.validators`: Response validation helpers
- `core.models`: Pydantic models for request/response validation
