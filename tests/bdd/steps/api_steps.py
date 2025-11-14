"""
API-related step definitions for BDD tests.

This module provides step definitions for making HTTP requests, preparing data,
and validating API responses in BDD scenarios. It supports all common HTTP methods
(GET, POST, PUT, DELETE) and includes comprehensive response validation capabilities.

Steps:
- Request steps: Send GET, POST, PUT, DELETE requests
- Data preparation steps: Parse data tables into context
- Response validation steps: Validate status codes, fields, schemas, and list properties
"""

import allure
import logging
import json
from typing import Dict, Any, List
from pytest_bdd import given, when, then, parsers

logger = logging.getLogger(__name__)

# Allure feature and story decorators for this module
allure.feature("API Testing")
allure.story("HTTP Requests and Response Validation")


# ============================================================================
# REQUEST STEPS
# ============================================================================

@when(parsers.parse('I send a GET request to "{endpoint}"'))
@allure.story("GET Requests")
def send_get_request(bdd_context, jsonplaceholder_client, endpoint):
    """
    Send GET request to the specified endpoint.
    
    This step sends a GET request and stores the response in the BDD context
    for use in subsequent steps. Request and response details are attached
    to the Allure report for debugging.
    
    Args:
        bdd_context: BDD context for storing response
        jsonplaceholder_client: JSONPlaceholder API client fixture
        endpoint: API endpoint path (e.g., "/posts" or "/posts/1")
        
    Example in feature file:
        When I send a GET request to "/posts"
        When I send a GET request to "/posts/1"
        When I send a GET request to "/users/1/posts"
    """
    with allure.step(f"Send GET request to {endpoint}"):
        try:
            logger.info(f"Sending GET request to: {endpoint}")
            
            # Send request
            response = jsonplaceholder_client.client.get(endpoint)
            
            # Store response in context
            bdd_context.response = response
            bdd_context.last_endpoint = endpoint
            bdd_context.last_method = "GET"
            
            # Attach request details to Allure
            allure.attach(
                endpoint,
                name="Request Endpoint",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                "GET",
                name="Request Method",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Attach response details to Allure
            allure.attach(
                str(response.status_code),
                name="Response Status Code",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )
            
            logger.info(f"GET request completed with status: {response.status_code}")
            
        except Exception as e:
            # Attach error details to Allure
            allure.attach(
                str(e),
                name="Error Details",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"Endpoint: {endpoint}\nMethod: GET",
                name="Failed Request Details",
                attachment_type=allure.attachment_type.TEXT
            )
            logger.error(f"GET request failed: {e}")
            raise


@when(parsers.parse('I send a POST request to "{endpoint}" with the {data_name} data'))
@allure.story("POST Requests")
def send_post_request_with_data(bdd_context, jsonplaceholder_client, endpoint, data_name):
    """
    Send POST request with data from context.
    
    This step retrieves data from the BDD context (stored by a previous step)
    and sends it in a POST request. The response is stored in the context.
    
    Args:
        bdd_context: BDD context containing request data
        jsonplaceholder_client: JSONPlaceholder API client fixture
        endpoint: API endpoint path
        data_name: Name of the data attribute in context (e.g., "post", "user")
        
    Example in feature file:
        Given I have post data:
            | field  | value      |
            | userId | 1          |
            | title  | Test Post  |
        When I send a POST request to "/posts" with the post data
    """
    with allure.step(f"Send POST request to {endpoint}"):
        try:
            # Get data from context
            data_attr = f"{data_name}_data"
            if not bdd_context.has(data_attr):
                error_msg = f"No {data_name} data found in context. Use a data preparation step first."
                allure.attach(
                    error_msg,
                    name="Context Error",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise ValueError(error_msg)
            
            data = getattr(bdd_context, data_attr)
            
            logger.info(f"Sending POST request to: {endpoint}")
            logger.debug(f"Request data: {data}")
            
            # Send request
            response = jsonplaceholder_client.client.post(endpoint, json=data)
            
            # Store response in context
            bdd_context.response = response
            bdd_context.last_endpoint = endpoint
            bdd_context.last_method = "POST"
            
            # Attach request details to Allure
            allure.attach(
                endpoint,
                name="Request Endpoint",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                "POST",
                name="Request Method",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                json.dumps(data, indent=2),
                name="Request Body",
                attachment_type=allure.attachment_type.JSON
            )
            
            # Attach response details to Allure
            allure.attach(
                str(response.status_code),
                name="Response Status Code",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )
            
            logger.info(f"POST request completed with status: {response.status_code}")
            
        except Exception as e:
            # Attach error details to Allure
            allure.attach(
                str(e),
                name="Error Details",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"Endpoint: {endpoint}\nMethod: POST\nData Name: {data_name}",
                name="Failed Request Details",
                attachment_type=allure.attachment_type.TEXT
            )
            logger.error(f"POST request failed: {e}")
            raise


@when(parsers.parse('I send a PUT request to "{endpoint}" with the {data_name} data'))
@allure.story("PUT Requests")
def send_put_request_with_data(bdd_context, jsonplaceholder_client, endpoint, data_name):
    """
    Send PUT request with data from context.
    
    This step retrieves data from the BDD context and sends it in a PUT request
    to completely replace the resource at the endpoint.
    
    Args:
        bdd_context: BDD context containing request data
        jsonplaceholder_client: JSONPlaceholder API client fixture
        endpoint: API endpoint path
        data_name: Name of the data attribute in context
        
    Example in feature file:
        Given I have post data:
            | field  | value              |
            | userId | 1                  |
            | title  | Updated Post Title |
            | body   | Updated content    |
        When I send a PUT request to "/posts/1" with the post data
    """
    with allure.step(f"Send PUT request to {endpoint}"):
        try:
            # Get data from context
            data_attr = f"{data_name}_data"
            if not bdd_context.has(data_attr):
                error_msg = f"No {data_name} data found in context. Use a data preparation step first."
                allure.attach(
                    error_msg,
                    name="Context Error",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise ValueError(error_msg)
            
            data = getattr(bdd_context, data_attr)
            
            logger.info(f"Sending PUT request to: {endpoint}")
            logger.debug(f"Request data: {data}")
            
            # Send request
            response = jsonplaceholder_client.client.put(endpoint, json=data)
            
            # Store response in context
            bdd_context.response = response
            bdd_context.last_endpoint = endpoint
            bdd_context.last_method = "PUT"
            
            # Attach request details to Allure
            allure.attach(
                endpoint,
                name="Request Endpoint",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                "PUT",
                name="Request Method",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                json.dumps(data, indent=2),
                name="Request Body",
                attachment_type=allure.attachment_type.JSON
            )
            
            # Attach response details to Allure
            allure.attach(
                str(response.status_code),
                name="Response Status Code",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )
            
            logger.info(f"PUT request completed with status: {response.status_code}")
            
        except Exception as e:
            # Attach error details to Allure
            allure.attach(
                str(e),
                name="Error Details",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"Endpoint: {endpoint}\nMethod: PUT\nData Name: {data_name}",
                name="Failed Request Details",
                attachment_type=allure.attachment_type.TEXT
            )
            logger.error(f"PUT request failed: {e}")
            raise


@when(parsers.parse('I send a DELETE request to "{endpoint}"'))
@allure.story("DELETE Requests")
def send_delete_request(bdd_context, jsonplaceholder_client, endpoint):
    """
    Send DELETE request to the specified endpoint.
    
    This step sends a DELETE request to remove a resource and stores the
    response in the BDD context.
    
    Args:
        bdd_context: BDD context for storing response
        jsonplaceholder_client: JSONPlaceholder API client fixture
        endpoint: API endpoint path (e.g., "/posts/1")
        
    Example in feature file:
        When I send a DELETE request to "/posts/1"
        When I send a DELETE request to "/users/5"
    """
    with allure.step(f"Send DELETE request to {endpoint}"):
        try:
            logger.info(f"Sending DELETE request to: {endpoint}")
            
            # Send request
            response = jsonplaceholder_client.client.delete(endpoint)
            
            # Store response in context
            bdd_context.response = response
            bdd_context.last_endpoint = endpoint
            bdd_context.last_method = "DELETE"
            
            # Attach request details to Allure
            allure.attach(
                endpoint,
                name="Request Endpoint",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                "DELETE",
                name="Request Method",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Attach response details to Allure
            allure.attach(
                str(response.status_code),
                name="Response Status Code",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )
            
            logger.info(f"DELETE request completed with status: {response.status_code}")
            
        except Exception as e:
            # Attach error details to Allure
            allure.attach(
                str(e),
                name="Error Details",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"Endpoint: {endpoint}\nMethod: DELETE",
                name="Failed Request Details",
                attachment_type=allure.attachment_type.TEXT
            )
            logger.error(f"DELETE request failed: {e}")
            raise


# ============================================================================
# DATA PREPARATION STEPS
# ============================================================================

@given(parsers.parse('I have {data_name} data:\n{data_table}'))
@allure.story("Data Preparation")
def prepare_data_from_table(bdd_context, data_name, data_table):
    """
    Parse data table into context for use in requests.
    
    This step parses a Gherkin data table and stores the data in the BDD context.
    It supports automatic type conversion for common data types (integers, booleans,
    null values) and handles nested JSON structures.
    
    Args:
        bdd_context: BDD context for storing parsed data
        data_name: Name to use for storing data (e.g., "post", "user", "comment")
        data_table: Gherkin data table string
        
    Example in feature file:
        Given I have post data:
            | field  | value                    |
            | userId | 1                        |
            | title  | Test Post from BDD       |
            | body   | This is a test post body |
        
        Given I have user data:
            | field    | value              |
            | name     | John Doe           |
            | username | johndoe            |
            | email    | john@example.com   |
            | active   | true               |
    """
    with allure.step(f"Prepare {data_name} data from table"):
        try:
            logger.info(f"Parsing {data_name} data from table")
            
            # Attach raw data table to Allure
            allure.attach(
                data_table,
                name="Raw Data Table",
                attachment_type=allure.attachment_type.TEXT
            )
            
            data = {}
            lines = data_table.strip().split('\n')
            
            # Skip header row (first line)
            for line in lines[1:]:
                if '|' in line:
                    # Split by | and remove empty strings from edges
                    parts = [p.strip() for p in line.split('|')]
                    parts = [p for p in parts if p]  # Remove empty strings
                    
                    if len(parts) >= 2:
                        field = parts[0]
                        value = parts[1]
                        
                        # Convert value to appropriate type
                        converted_value = _convert_value(value)
                        data[field] = converted_value
                        
                        logger.debug(f"Parsed field '{field}': {converted_value} (type: {type(converted_value).__name__})")
            
            # Validate that we parsed some data
            if not data:
                error_msg = f"No data could be parsed from the table for {data_name}"
                allure.attach(
                    error_msg,
                    name="Parsing Error",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise ValueError(error_msg)
            
            # Store in context with naming convention
            data_attr = f"{data_name}_data"
            setattr(bdd_context, data_attr, data)
            
            # Attach to Allure report
            allure.attach(
                json.dumps(data, indent=2),
                name=f"{data_name.capitalize()} Data",
                attachment_type=allure.attachment_type.JSON
            )
            
            logger.info(f"Parsed {len(data)} fields for {data_name} data")
            
        except Exception as e:
            # Attach error details to Allure
            allure.attach(
                str(e),
                name="Error Details",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"Data Name: {data_name}\nTable:\n{data_table}",
                name="Failed Data Preparation Details",
                attachment_type=allure.attachment_type.TEXT
            )
            logger.error(f"Failed to prepare data from table: {e}")
            raise


@given(parsers.parse('I have {data_name} JSON data:\n{json_data}'))
@allure.story("Data Preparation")
def prepare_data_from_json(bdd_context, data_name, json_data):
    """
    Parse JSON data into context for use in requests.
    
    This step parses a JSON string and stores the data in the BDD context.
    Useful for complex nested data structures that are difficult to represent
    in a table format.
    
    Args:
        bdd_context: BDD context for storing parsed data
        data_name: Name to use for storing data
        json_data: JSON string
        
    Example in feature file:
        Given I have user JSON data:
            '''
            {
                "name": "John Doe",
                "username": "johndoe",
                "email": "john@example.com",
                "address": {
                    "street": "Main St",
                    "city": "New York"
                }
            }
            '''
    """
    with allure.step(f"Prepare {data_name} data from JSON"):
        try:
            logger.info(f"Parsing {data_name} data from JSON")
            
            # Attach raw JSON to Allure
            allure.attach(
                json_data,
                name="Raw JSON Data",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Parse JSON string
            data = json.loads(json_data.strip())
            
            # Validate that we got a dictionary
            if not isinstance(data, dict):
                error_msg = f"JSON data must be an object/dictionary, got {type(data).__name__}"
                allure.attach(
                    error_msg,
                    name="Validation Error",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise ValueError(error_msg)
            
            # Store in context
            data_attr = f"{data_name}_data"
            setattr(bdd_context, data_attr, data)
            
            # Attach to Allure report
            allure.attach(
                json.dumps(data, indent=2),
                name=f"{data_name.capitalize()} Data",
                attachment_type=allure.attachment_type.JSON
            )
            
            logger.info(f"Parsed JSON data for {data_name}")
            
        except json.JSONDecodeError as e:
            # Attach error details to Allure
            allure.attach(
                str(e),
                name="JSON Parse Error",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"Data Name: {data_name}\nJSON:\n{json_data}",
                name="Failed JSON Parsing Details",
                attachment_type=allure.attachment_type.TEXT
            )
            logger.error(f"Failed to parse JSON: {e}")
            raise ValueError(f"Invalid JSON data: {e}")
        except Exception as e:
            # Attach error details to Allure
            allure.attach(
                str(e),
                name="Error Details",
                attachment_type=allure.attachment_type.TEXT
            )
            logger.error(f"Failed to prepare data from JSON: {e}")
            raise


def _convert_value(value: str) -> Any:
    """
    Convert string value to appropriate Python type.
    
    Handles conversion for:
    - Integers (e.g., "123" -> 123)
    - Floats (e.g., "12.34" -> 12.34)
    - Booleans (e.g., "true" -> True, "false" -> False)
    - Null/None (e.g., "null" -> None, "none" -> None)
    - JSON objects/arrays (e.g., '{"key": "value"}' -> dict)
    - Strings (default)
    
    Args:
        value: String value to convert
        
    Returns:
        Converted value with appropriate type
    """
    # Handle null/none
    if value.lower() in ('null', 'none', ''):
        return None
    
    # Handle booleans
    if value.lower() == 'true':
        return True
    if value.lower() == 'false':
        return False
    
    # Try to parse as JSON (for objects/arrays)
    if value.startswith(('{', '[')):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
    
    # Try to parse as integer
    try:
        return int(value)
    except ValueError:
        pass
    
    # Try to parse as float
    try:
        return float(value)
    except ValueError:
        pass
    
    # Return as string
    return value


# ============================================================================
# RESPONSE VALIDATION STEPS
# ============================================================================

@then("the response should be a non-empty list")
@allure.story("Response Validation")
def validate_response_is_non_empty_list(bdd_context):
    """
    Validate that the response is a non-empty list.
    
    This step checks that the response body is a JSON array with at least
    one element.
    
    Args:
        bdd_context: BDD context containing the response
        
    Example in feature file:
        Then the response should be a non-empty list
    """
    with allure.step("Verify response is a non-empty list"):
        response = bdd_context.response
        data = response.json()
        
        # Check if it's a list
        assert isinstance(data, list), \
            f"Expected response to be a list, but got {type(data).__name__}"
        
        # Check if it's not empty
        assert len(data) > 0, \
            "Expected response list to be non-empty, but it was empty"
        
        # Attach validation result
        allure.attach(
            f"List length: {len(data)}",
            name="Validation Result",
            attachment_type=allure.attachment_type.TEXT
        )
        
        logger.info(f"Validated response is a non-empty list with {len(data)} items")


@then("the response should be a list")
@allure.story("Response Validation")
def validate_response_is_list(bdd_context):
    """
    Validate that the response is a list (can be empty).
    
    Args:
        bdd_context: BDD context containing the response
        
    Example in feature file:
        Then the response should be a list
    """
    with allure.step("Verify response is a list"):
        response = bdd_context.response
        data = response.json()
        
        assert isinstance(data, list), \
            f"Expected response to be a list, but got {type(data).__name__}"
        
        allure.attach(
            f"List length: {len(data)}",
            name="Validation Result",
            attachment_type=allure.attachment_type.TEXT
        )
        
        logger.info(f"Validated response is a list with {len(data)} items")


@then("the response should be a dictionary")
@allure.story("Response Validation")
def validate_response_is_dict(bdd_context):
    """
    Validate that the response is a dictionary/object.
    
    Args:
        bdd_context: BDD context containing the response
        
    Example in feature file:
        Then the response should be a dictionary
    """
    with allure.step("Verify response is a dictionary"):
        response = bdd_context.response
        data = response.json()
        
        assert isinstance(data, dict), \
            f"Expected response to be a dictionary, but got {type(data).__name__}"
        
        allure.attach(
            f"Dictionary keys: {', '.join(data.keys())}",
            name="Validation Result",
            attachment_type=allure.attachment_type.TEXT
        )
        
        logger.info(f"Validated response is a dictionary with {len(data)} keys")


@then(parsers.parse('the response should contain field "{field}"'))
@allure.story("Response Validation")
def validate_response_contains_field(bdd_context, field):
    """
    Validate that the response contains a specific field.
    
    Args:
        bdd_context: BDD context containing the response
        field: Field name to check for
        
    Example in feature file:
        Then the response should contain field "id"
        Then the response should contain field "email"
    """
    with allure.step(f"Verify response contains field '{field}'"):
        response = bdd_context.response
        data = response.json()
        
        assert field in data, \
            f"Expected response to contain field '{field}', but it was not found. Available fields: {list(data.keys())}"
        
        # Attach field value
        allure.attach(
            str(data[field]),
            name=f"Field '{field}' Value",
            attachment_type=allure.attachment_type.TEXT
        )
        
        logger.info(f"Validated response contains field '{field}' with value: {data[field]}")


@then(parsers.parse('the response field "{field}" should equal "{expected_value}"'))
@allure.story("Response Validation")
def validate_response_field_equals(bdd_context, field, expected_value):
    """
    Validate that a response field has a specific value.
    
    Args:
        bdd_context: BDD context containing the response
        field: Field name to check
        expected_value: Expected value (as string, will be converted)
        
    Example in feature file:
        Then the response field "title" should equal "Test Post"
        Then the response field "userId" should equal "1"
        Then the response field "completed" should equal "true"
    """
    with allure.step(f"Verify field '{field}' equals '{expected_value}'"):
        response = bdd_context.response
        data = response.json()
        
        # Check field exists
        assert field in data, \
            f"Field '{field}' not found in response. Available fields: {list(data.keys())}"
        
        actual_value = data[field]
        
        # Convert expected value to match actual value type
        converted_expected = _convert_value(expected_value)
        
        # Compare values
        assert actual_value == converted_expected, \
            f"Expected field '{field}' to equal '{converted_expected}', but got '{actual_value}'"
        
        # Attach comparison result
        allure.attach(
            f"Field: {field}\nExpected: {converted_expected}\nActual: {actual_value}\nMatch: ✓",
            name="Field Comparison",
            attachment_type=allure.attachment_type.TEXT
        )
        
        logger.info(f"Validated field '{field}' equals '{converted_expected}'")


@then(parsers.parse('each {item_name} should have required fields:\n{fields_table}'))
@allure.story("Response Validation")
def validate_list_items_have_fields(bdd_context, item_name, fields_table):
    """
    Validate that each item in a response list has required fields.
    
    This step is useful for validating list responses where each item
    should have a specific structure.
    
    Args:
        bdd_context: BDD context containing the response
        item_name: Name of items in the list (for logging)
        fields_table: Table with field names
        
    Example in feature file:
        Then each post should have required fields:
            | userId |
            | id     |
            | title  |
            | body   |
    """
    with allure.step(f"Verify each {item_name} has required fields"):
        response = bdd_context.response
        data = response.json()
        
        # Ensure response is a list
        assert isinstance(data, list), \
            f"Expected response to be a list, but got {type(data).__name__}"
        
        assert len(data) > 0, \
            "Cannot validate fields on empty list"
        
        # Parse required fields from table
        required_fields = []
        lines = fields_table.strip().split('\n')
        for line in lines:
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                parts = [p for p in parts if p]
                if parts:
                    required_fields.append(parts[0])
        
        logger.info(f"Validating {len(data)} items have fields: {required_fields}")
        
        # Validate each item
        missing_fields_items = []
        for index, item in enumerate(data):
            missing_fields = [field for field in required_fields if field not in item]
            if missing_fields:
                missing_fields_items.append({
                    'index': index,
                    'missing': missing_fields
                })
        
        # Assert no items are missing fields
        assert not missing_fields_items, \
            f"Some items are missing required fields: {missing_fields_items[:5]}"  # Show first 5
        
        # Attach validation result
        allure.attach(
            f"Validated {len(data)} items\nRequired fields: {', '.join(required_fields)}\nAll items valid: ✓",
            name="List Validation Result",
            attachment_type=allure.attachment_type.TEXT
        )
        
        logger.info(f"Validated all {len(data)} items have required fields")


@then(parsers.parse('the response list should have {count:d} items'))
@allure.story("Response Validation")
def validate_list_count(bdd_context, count):
    """
    Validate that the response list has a specific number of items.
    
    Args:
        bdd_context: BDD context containing the response
        count: Expected number of items
        
    Example in feature file:
        Then the response list should have 10 items
        Then the response list should have 1 items
    """
    with allure.step(f"Verify response list has {count} items"):
        response = bdd_context.response
        data = response.json()
        
        assert isinstance(data, list), \
            f"Expected response to be a list, but got {type(data).__name__}"
        
        actual_count = len(data)
        assert actual_count == count, \
            f"Expected list to have {count} items, but got {actual_count}"
        
        allure.attach(
            f"Expected: {count}\nActual: {actual_count}\nMatch: ✓",
            name="List Count Validation",
            attachment_type=allure.attachment_type.TEXT
        )
        
        logger.info(f"Validated response list has {count} items")


@then(parsers.parse('the response list should have at least {min_count:d} items'))
@allure.story("Response Validation")
def validate_list_min_count(bdd_context, min_count):
    """
    Validate that the response list has at least a minimum number of items.
    
    Args:
        bdd_context: BDD context containing the response
        min_count: Minimum expected number of items
        
    Example in feature file:
        Then the response list should have at least 1 items
        Then the response list should have at least 10 items
    """
    with allure.step(f"Verify response list has at least {min_count} items"):
        response = bdd_context.response
        data = response.json()
        
        assert isinstance(data, list), \
            f"Expected response to be a list, but got {type(data).__name__}"
        
        actual_count = len(data)
        assert actual_count >= min_count, \
            f"Expected list to have at least {min_count} items, but got {actual_count}"
        
        allure.attach(
            f"Minimum: {min_count}\nActual: {actual_count}\nValid: ✓",
            name="List Minimum Count Validation",
            attachment_type=allure.attachment_type.TEXT
        )
        
        logger.info(f"Validated response list has at least {min_count} items (actual: {actual_count})")
