"""BDD-specific fixtures and configuration."""

import pytest
from typing import Any, Dict

# Import step definitions to ensure they are registered with pytest-bdd
# This must be done before scenarios are collected
from tests.bdd.steps import common_steps  # noqa: F401
from tests.bdd.steps import assertions_steps  # noqa: F401
from tests.bdd.steps import api_steps  # noqa: F401
from tests.bdd.steps import database_steps  # noqa: F401

# NOTE: pytest_plugins cannot be defined in non-top-level conftest files
# All plugin registrations have been moved to tests/conftest.py


class BDDContext:
    """
    Context object for sharing data between BDD steps.
    
    Provides a simple namespace for storing and retrieving data
    within a scenario execution. This allows steps to pass data
    to subsequent steps in the same scenario.
    
    Examples:
        >>> context = BDDContext()
        >>> context.response = {"id": 1, "name": "Test"}
        >>> context.user_id = 123
        >>> print(context.response)
        {'id': 1, 'name': 'Test'}
        >>> print(context.has('user_id'))
        True
        >>> print(context.get('missing', 'default'))
        'default'
    """
    
    def __init__(self):
        """Initialize the BDD context with an empty data dictionary."""
        self._data: Dict[str, Any] = {}
    
    def __setattr__(self, name: str, value: Any):
        """
        Set an attribute on the context.
        
        Internal attributes (starting with '_') are set on the object itself.
        All other attributes are stored in the internal data dictionary.
        
        Args:
            name: Attribute name
            value: Attribute value
        """
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value
    
    def __getattr__(self, name: str) -> Any:
        """
        Get an attribute from the context.
        
        Args:
            name: Attribute name
            
        Returns:
            The attribute value
            
        Raises:
            AttributeError: If the attribute doesn't exist
        """
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
    
    def get(self, name: str, default: Any = None) -> Any:
        """
        Get a value from the context with a default fallback.
        
        Args:
            name: Attribute name
            default: Default value to return if attribute doesn't exist
            
        Returns:
            The attribute value or default if not found
        """
        return self._data.get(name, default)
    
    def has(self, name: str) -> bool:
        """
        Check if an attribute exists in the context.
        
        Args:
            name: Attribute name
            
        Returns:
            True if the attribute exists, False otherwise
        """
        return name in self._data
    
    def clear(self):
        """Clear all data from the context."""
        self._data.clear()
    
    def attach_to_allure(self, name: str = "BDD Context Data"):
        """
        Attach the current context data to Allure report.
        
        This method serializes the context data and attaches it to the
        Allure report for debugging and documentation purposes. It handles
        various data types and provides a readable representation.
        
        Args:
            name: Name for the Allure attachment
        """
        import allure
        import json
        
        # Create a serializable representation of the context data
        serializable_data = {}
        for key, value in self._data.items():
            try:
                # Try to convert to a string representation
                if hasattr(value, '__dict__'):
                    # For objects with __dict__, show their attributes
                    serializable_data[key] = str(value.__dict__)
                elif hasattr(value, 'json') and callable(value.json):
                    # For Response objects, get the JSON body
                    try:
                        serializable_data[key] = value.json()
                    except:
                        serializable_data[key] = str(value)
                else:
                    serializable_data[key] = value
            except:
                # Fallback to string representation
                serializable_data[key] = str(value)
        
        # Attach to Allure
        try:
            allure.attach(
                json.dumps(serializable_data, indent=2, default=str),
                name=name,
                attachment_type=allure.attachment_type.JSON
            )
        except:
            # If JSON serialization fails, attach as text
            allure.attach(
                str(serializable_data),
                name=name,
                attachment_type=allure.attachment_type.TEXT
            )


@pytest.fixture(scope="function")
def bdd_context(request):
    """
    Provide BDD context for sharing data between steps.
    
    This fixture creates a new BDDContext instance for each test scenario,
    ensuring data isolation between scenarios. The context is automatically
    cleaned up after the scenario completes. Context data is also attached
    to the Allure report for debugging purposes.
    
    Scope: function - New context for each scenario
    
    Yields:
        BDDContext: Context object for the scenario
        
    Examples:
        In step definitions:
        
        @given("I have some data")
        def store_data(bdd_context):
            bdd_context.my_data = {"key": "value"}
        
        @when("I process the data")
        def process_data(bdd_context):
            data = bdd_context.my_data
            # Process data...
            bdd_context.result = processed_data
        
        @then("the result should be correct")
        def verify_result(bdd_context):
            assert bdd_context.result == expected_value
    """
    context = BDDContext()
    yield context
    
    # Attach context data to Allure report after scenario completes
    # This helps with debugging by showing all data that was shared between steps
    try:
        if context._data:  # Only attach if there's data
            context.attach_to_allure("Scenario Context Data")
    except Exception:
        # Don't fail the test if attachment fails
        pass
    
    context.clear()
