"""
Assertion step definitions for BDD tests.

This module provides reusable step definitions for common assertions
used in API testing scenarios. All assertions are wrapped with Allure
steps for detailed reporting.

Steps:
- Then the response status code should be {status_code}
- Then the response should be a list
- Then the response should be a non-empty list
- Then the response should be a dict
- Then the response should contain field "{field}"
- Then the response field "{field}" should equal "{value}"
- Then each item in the response should have field "{field}"
"""

import allure
import logging
from pytest_bdd import then, parsers
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# Allure feature and story decorators for this module
allure.feature("Response Assertions")
allure.story("API Response Validation")


@then(parsers.parse('the response status code should be {status_code:d}'))
@allure.story("Status Code Validation")
def check_status_code(bdd_context, status_code: int):
    """
    Verify the HTTP response status code matches the expected value.
    
    This step checks that the last API response stored in the BDD context
    has the expected status code. It's wrapped in an Allure step for
    detailed reporting.
    
    Args:
        bdd_context: BDD context containing the response
        status_code: Expected HTTP status code (e.g., 200, 201, 404)
        
    Raises:
        AssertionError: If the status code doesn't match
        AttributeError: If no response is stored in context
        
    Example in feature file:
        Then the response status code should be 200
        Then the response status code should be 404
    """
    with allure.step(f"Verify response status code is {status_code}"):
        assert hasattr(bdd_context, 'response'), \
            "No response found in context. Make sure a request step was executed first."
        
        actual_status = bdd_context.response.status_code
        
        # Attach status codes to Allure report
        allure.attach(
            str(actual_status),
            name="Actual Status Code",
            attachment_type=allure.attachment_type.TEXT
        )
        
        allure.attach(
            str(status_code),
            name="Expected Status Code",
            attachment_type=allure.attachment_type.TEXT
        )
        
        assert actual_status == status_code, \
            f"Expected status code {status_code}, but got {actual_status}"
        
        logger.info(f"Status code verification passed: {status_code}")


@then("the response should be a list")
@allure.story("Response Type Validation")
def check_response_is_list(bdd_context):
    """
    Verify the response body is a list (array).
    
    This step checks that the JSON response is a list type. It's useful
    for endpoints that return collections of items.
    
    Args:
        bdd_context: BDD context containing the response
        
    Raises:
        AssertionError: If the response is not a list
        AttributeError: If no response is stored in context
        
    Example in feature file:
        Then the response should be a list
    """
    with allure.step("Verify response is a list"):
        assert hasattr(bdd_context, 'response'), \
            "No response found in context. Make sure a request step was executed first."
        
        data = bdd_context.response.json()
        
        assert isinstance(data, list), \
            f"Expected response to be a list, but got {type(data).__name__}"
        
        # Attach response type to Allure report
        allure.attach(
            f"List with {len(data)} items",
            name="Response Type",
            attachment_type=allure.attachment_type.TEXT
        )
        
        logger.info(f"Response is a list with {len(data)} items")


@then("the response should be a non-empty list")
def check_response_is_non_empty_list(bdd_context):
    """
    Verify the response body is a non-empty list.
    
    This step checks that the JSON response is a list and contains
    at least one item. It's useful for endpoints that should always
    return data.
    
    Args:
        bdd_context: BDD context containing the response
        
    Raises:
        AssertionError: If the response is not a list or is empty
        AttributeError: If no response is stored in context
        
    Example in feature file:
        Then the response should be a non-empty list
    """
    with allure.step("Verify response is a non-empty list"):
        assert hasattr(bdd_context, 'response'), \
            "No response found in context. Make sure a request step was executed first."
        
        data = bdd_context.response.json()
        
        assert isinstance(data, list), \
            f"Expected response to be a list, but got {type(data).__name__}"
        
        assert len(data) > 0, \
            "Expected response list to contain at least one item, but it was empty"
        
        # Attach list details to Allure report
        allure.attach(
            str(len(data)),
            name="List Length",
            attachment_type=allure.attachment_type.TEXT
        )
        
        logger.info(f"Response is a non-empty list with {len(data)} items")


@then("the response should be a dict")
@allure.story("Response Type Validation")
def check_response_is_dict(bdd_context):
    """
    Verify the response body is a dictionary (object).
    
    This step checks that the JSON response is a dictionary type. It's
    useful for endpoints that return single objects.
    
    Args:
        bdd_context: BDD context containing the response
        
    Raises:
        AssertionError: If the response is not a dictionary
        AttributeError: If no response is stored in context
        
    Example in feature file:
        Then the response should be a dict
    """
    with allure.step("Verify response is a dictionary"):
        assert hasattr(bdd_context, 'response'), \
            "No response found in context. Make sure a request step was executed first."
        
        data = bdd_context.response.json()
        
        assert isinstance(data, dict), \
            f"Expected response to be a dict, but got {type(data).__name__}"
        
        # Attach response type to Allure report
        allure.attach(
            f"Dictionary with {len(data)} fields",
            name="Response Type",
            attachment_type=allure.attachment_type.TEXT
        )
        
        logger.info(f"Response is a dictionary with {len(data)} fields")


@then(parsers.parse('the response should contain field "{field}"'))
@allure.story("Field Validation")
def check_field_exists(bdd_context, field: str):
    """
    Verify the response contains a specific field.
    
    This step checks that a field (key) exists in the JSON response
    dictionary. It doesn't validate the value, only the presence of the field.
    
    Args:
        bdd_context: BDD context containing the response
        field: Name of the field to check for
        
    Raises:
        AssertionError: If the field doesn't exist in the response
        AttributeError: If no response is stored in context
        
    Example in feature file:
        Then the response should contain field "id"
        Then the response should contain field "email"
    """
    with allure.step(f"Verify response contains field '{field}'"):
        assert hasattr(bdd_context, 'response'), \
            "No response found in context. Make sure a request step was executed first."
        
        data = bdd_context.response.json()
        
        assert isinstance(data, dict), \
            f"Cannot check field in {type(data).__name__}. Response must be a dictionary."
        
        assert field in data, \
            f"Field '{field}' not found in response. Available fields: {list(data.keys())}"
        
        # Attach field information to Allure report
        allure.attach(
            field,
            name="Field Name",
            attachment_type=allure.attachment_type.TEXT
        )
        
        allure.attach(
            str(data[field]),
            name="Field Value",
            attachment_type=allure.attachment_type.TEXT
        )
        
        logger.info(f"Field '{field}' exists in response with value: {data[field]}")


@then(parsers.parse('the response field "{field}" should equal "{value}"'))
@allure.story("Field Validation")
def check_field_value(bdd_context, field: str, value: str):
    """
    Verify a response field has a specific value.
    
    This step checks that a field in the JSON response has the expected
    value. The comparison is done as strings to handle different data types.
    
    Args:
        bdd_context: BDD context containing the response
        field: Name of the field to check
        value: Expected value (as string)
        
    Raises:
        AssertionError: If the field value doesn't match
        AttributeError: If no response is stored in context
        
    Example in feature file:
        Then the response field "title" should equal "Test Post"
        Then the response field "userId" should equal "1"
    """
    with allure.step(f"Verify response field '{field}' equals '{value}'"):
        assert hasattr(bdd_context, 'response'), \
            "No response found in context. Make sure a request step was executed first."
        
        data = bdd_context.response.json()
        
        assert isinstance(data, dict), \
            f"Cannot check field in {type(data).__name__}. Response must be a dictionary."
        
        assert field in data, \
            f"Field '{field}' not found in response. Available fields: {list(data.keys())}"
        
        actual_value = str(data[field])
        
        # Attach comparison details to Allure report
        allure.attach(
            actual_value,
            name="Actual Value",
            attachment_type=allure.attachment_type.TEXT
        )
        
        allure.attach(
            value,
            name="Expected Value",
            attachment_type=allure.attachment_type.TEXT
        )
        
        assert actual_value == value, \
            f"Expected field '{field}' to equal '{value}', but got '{actual_value}'"
        
        logger.info(f"Field '{field}' has expected value: {value}")


@then(parsers.parse('each item in the response should have field "{field}"'))
@allure.story("List Item Validation")
def check_each_item_has_field(bdd_context, field: str):
    """
    Verify each item in a response list contains a specific field.
    
    This step checks that every item in a list response has the specified
    field. It's useful for validating collection endpoints.
    
    Args:
        bdd_context: BDD context containing the response
        field: Name of the field to check for in each item
        
    Raises:
        AssertionError: If any item is missing the field or response is not a list
        AttributeError: If no response is stored in context
        
    Example in feature file:
        Then each item in the response should have field "id"
        Then each item in the response should have field "email"
    """
    with allure.step(f"Verify each item has field '{field}'"):
        assert hasattr(bdd_context, 'response'), \
            "No response found in context. Make sure a request step was executed first."
        
        data = bdd_context.response.json()
        
        assert isinstance(data, list), \
            f"Cannot check items in {type(data).__name__}. Response must be a list."
        
        assert len(data) > 0, \
            "Cannot verify field in empty list"
        
        # Check each item for the field
        missing_field_indices = []
        for index, item in enumerate(data):
            if not isinstance(item, dict):
                raise AssertionError(
                    f"Item at index {index} is not a dictionary. "
                    f"Got {type(item).__name__} instead."
                )
            
            if field not in item:
                missing_field_indices.append(index)
        
        # Attach validation details to Allure report
        allure.attach(
            str(len(data)),
            name="Total Items Checked",
            attachment_type=allure.attachment_type.TEXT
        )
        
        allure.attach(
            field,
            name="Required Field",
            attachment_type=allure.attachment_type.TEXT
        )
        
        if missing_field_indices:
            allure.attach(
                str(missing_field_indices),
                name="Items Missing Field",
                attachment_type=allure.attachment_type.TEXT
            )
            
            raise AssertionError(
                f"Field '{field}' is missing in {len(missing_field_indices)} items "
                f"at indices: {missing_field_indices}"
            )
        
        logger.info(f"All {len(data)} items have field '{field}'")
