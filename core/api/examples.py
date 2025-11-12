"""
Example usage of the APIClient for test automation.

This module demonstrates common patterns and use cases for the APIClient.
"""

from core.api import APIClient
from core.config.settings import get_settings


def example_basic_usage():
    """Basic API client usage example."""
    print("=== Basic Usage Example ===\n")
    
    # Create client instance
    client = APIClient()
    print(f"Client initialized with base URL: {client.base_url}")
    
    # Make a simple GET request
    # response = client.get("/users")
    # print(f"Response status: {response.status_code}")
    
    print("✓ Basic usage example complete\n")


def example_authentication():
    """Authentication example."""
    print("=== Authentication Example ===\n")
    
    settings = get_settings()
    client = APIClient()
    
    # Authenticate with credentials
    try:
        # token = client.authenticate(
        #     username=settings.auth_user,
        #     password=settings.auth_password
        # )
        # print(f"Authenticated successfully!")
        # print(f"Token: {token[:20]}...")
        
        # Check authentication status
        print(f"Is authenticated: {client.is_authenticated()}")
        
        # Make authenticated request
        # response = client.get("/users/me")
        # print(f"User profile: {response.json()}")
        
    except Exception as e:
        print(f"Authentication failed: {e}")
    
    print("✓ Authentication example complete\n")


def example_with_context_manager():
    """Using APIClient as context manager."""
    print("=== Context Manager Example ===\n")
    
    # Client automatically closes session on exit
    with APIClient() as client:
        print(f"Client created: {client.base_url}")
        # response = client.get("/health")
        # print(f"Health check: {response.status_code}")
    
    print("✓ Session closed automatically")
    print("✓ Context manager example complete\n")


def example_custom_configuration():
    """Custom configuration example."""
    print("=== Custom Configuration Example ===\n")
    
    # Create client with custom settings
    client = APIClient(
        base_url="https://custom-api.example.com",
        timeout=60,
        retries=5
    )
    
    print(f"Custom base URL: {client.base_url}")
    print(f"Custom timeout: {client.timeout}s")
    print(f"Custom retries: {client.retries}")
    
    print("✓ Custom configuration example complete\n")


def example_request_hooks():
    """Request and response hooks example."""
    print("=== Hooks Example ===\n")
    
    client = APIClient()
    
    # Add request hook
    def log_request(method, url, **kwargs):
        print(f"[HOOK] Sending {method} request to {url}")
    
    # Add response hook
    def log_response(response):
        print(f"[HOOK] Received {response.status_code} response")
    
    client.add_request_hook(log_request)
    client.add_response_hook(log_response)
    
    print("Hooks registered")
    # response = client.get("/users")
    
    print("✓ Hooks example complete\n")


def example_token_management():
    """Token management example."""
    print("=== Token Management Example ===\n")
    
    client = APIClient()
    
    # Set token manually
    client.set_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example", "Bearer")
    print(f"Token set: {client.get_token()[:20]}...")
    print(f"Is authenticated: {client.is_authenticated()}")
    
    # Clear authentication
    client.clear_authentication()
    print(f"Authentication cleared")
    print(f"Is authenticated: {client.is_authenticated()}")
    
    print("✓ Token management example complete\n")


def example_error_handling():
    """Error handling example."""
    print("=== Error Handling Example ===\n")
    
    client = APIClient()
    
    try:
        # This will fail with connection error (example endpoint)
        # response = client.get("/nonexistent", timeout=1)
        print("Request would be attempted with retry logic")
        print("Automatic retry on 5xx errors and connection issues")
        print("Exponential backoff between retries")
    except Exception as e:
        print(f"Request failed after retries: {type(e).__name__}")
    
    print("✓ Error handling example complete\n")


if __name__ == "__main__":
    """Run all examples."""
    print("\n" + "="*60)
    print("APIClient Usage Examples")
    print("="*60 + "\n")
    
    example_basic_usage()
    example_authentication()
    example_with_context_manager()
    example_custom_configuration()
    example_request_hooks()
    example_token_management()
    example_error_handling()
    
    print("="*60)
    print("All examples completed!")
    print("="*60 + "\n")
