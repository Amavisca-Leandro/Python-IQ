"""Validators for HTTP responses, JSON schemas, and database data."""

from typing import Dict, List, Any, Optional, Union
import time
from jsonschema import validate as json_validate, ValidationError as JsonValidationError
import requests

# Optional SQLAlchemy import for database validators
try:
    from sqlalchemy.orm import Session
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False
    Session = Any  # Type hint fallback


class ValidationError(Exception):
    """Custom validation error for test assertions."""
    pass


def validate_response_status(
    response: requests.Response,
    expected_status: Union[int, List[int]],
    message: Optional[str] = None
) -> None:
    """
    Validate HTTP response status code.
    
    Args:
        response: requests.Response object
        expected_status: Expected status code or list of acceptable status codes
        message: Optional custom error message
        
    Raises:
        ValidationError: If status code doesn't match expected value(s)
    """
    expected_codes = [expected_status] if isinstance(expected_status, int) else expected_status
    
    if response.status_code not in expected_codes:
        error_msg = message or (
            f"Expected status code {expected_codes}, but got {response.status_code}. "
            f"Response: {response.text[:200]}"
        )
        raise ValidationError(error_msg)


def validate_response_time(
    response: requests.Response,
    max_time_ms: int,
    message: Optional[str] = None
) -> None:
    """
    Validate HTTP response time is within acceptable threshold.
    
    Args:
        response: requests.Response object
        max_time_ms: Maximum acceptable response time in milliseconds
        message: Optional custom error message
        
    Raises:
        ValidationError: If response time exceeds threshold
    """
    response_time_ms = response.elapsed.total_seconds() * 1000
    
    if response_time_ms > max_time_ms:
        error_msg = message or (
            f"Response time {response_time_ms:.2f}ms exceeds maximum {max_time_ms}ms"
        )
        raise ValidationError(error_msg)


def validate_required_fields(
    data: Dict[str, Any],
    required_fields: List[str],
    message: Optional[str] = None
) -> None:
    """
    Validate that all required fields are present in data dictionary.
    
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
        message: Optional custom error message
        
    Raises:
        ValidationError: If any required field is missing
    """
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        error_msg = message or f"Missing required fields: {', '.join(missing_fields)}"
        raise ValidationError(error_msg)


def validate_json_schema(
    data: Dict[str, Any],
    schema: Dict[str, Any],
    message: Optional[str] = None
) -> None:
    """
    Validate data against JSON schema.
    
    Args:
        data: Data to validate
        schema: JSON schema definition
        message: Optional custom error message
        
    Raises:
        ValidationError: If data doesn't match schema
    """
    try:
        json_validate(instance=data, schema=schema)
    except JsonValidationError as e:
        error_msg = message or f"JSON schema validation failed: {str(e)}"
        raise ValidationError(error_msg) from e


def validate_field_types(
    data: Dict[str, Any],
    field_types: Dict[str, type],
    message: Optional[str] = None
) -> None:
    """
    Validate that fields have expected types.
    
    Args:
        data: Dictionary to validate
        field_types: Dictionary mapping field names to expected types
        message: Optional custom error message
        
    Raises:
        ValidationError: If any field has incorrect type
    """
    type_errors = []
    
    for field, expected_type in field_types.items():
        if field in data and not isinstance(data[field], expected_type):
            actual_type = type(data[field]).__name__
            expected_type_name = expected_type.__name__
            type_errors.append(
                f"{field}: expected {expected_type_name}, got {actual_type}"
            )
    
    if type_errors:
        error_msg = message or f"Type validation failed: {'; '.join(type_errors)}"
        raise ValidationError(error_msg)


def validate_field_values(
    data: Dict[str, Any],
    field_validators: Dict[str, callable],
    message: Optional[str] = None
) -> None:
    """
    Validate field values using custom validator functions.
    
    Args:
        data: Dictionary to validate
        field_validators: Dictionary mapping field names to validator functions
        message: Optional custom error message
        
    Raises:
        ValidationError: If any field fails validation
    """
    validation_errors = []
    
    for field, validator in field_validators.items():
        if field in data:
            try:
                if not validator(data[field]):
                    validation_errors.append(f"{field}: validation failed")
            except Exception as e:
                validation_errors.append(f"{field}: {str(e)}")
    
    if validation_errors:
        error_msg = message or f"Field validation failed: {'; '.join(validation_errors)}"
        raise ValidationError(error_msg)


# Database-specific validators

def validate_db_record_exists(
    session: Session,
    model_class: Any,
    filters: Dict[str, Any],
    message: Optional[str] = None
) -> None:
    """
    Validate that a database record exists with given filters.
    
    Args:
        session: SQLAlchemy session
        model_class: SQLAlchemy model class
        filters: Dictionary of field filters
        message: Optional custom error message
        
    Raises:
        ValidationError: If record doesn't exist
    """
    query = session.query(model_class)
    for field, value in filters.items():
        query = query.filter(getattr(model_class, field) == value)
    
    record = query.first()
    
    if not record:
        error_msg = message or (
            f"Record not found in {model_class.__tablename__} with filters: {filters}"
        )
        raise ValidationError(error_msg)


def validate_db_record_count(
    session: Session,
    model_class: Any,
    expected_count: int,
    filters: Optional[Dict[str, Any]] = None,
    message: Optional[str] = None
) -> None:
    """
    Validate that database has expected number of records.
    
    Args:
        session: SQLAlchemy session
        model_class: SQLAlchemy model class
        expected_count: Expected number of records
        filters: Optional dictionary of field filters
        message: Optional custom error message
        
    Raises:
        ValidationError: If count doesn't match expected
    """
    query = session.query(model_class)
    
    if filters:
        for field, value in filters.items():
            query = query.filter(getattr(model_class, field) == value)
    
    actual_count = query.count()
    
    if actual_count != expected_count:
        error_msg = message or (
            f"Expected {expected_count} records in {model_class.__tablename__}, "
            f"but found {actual_count}"
        )
        raise ValidationError(error_msg)


def validate_db_field_value(
    session: Session,
    model_class: Any,
    record_id: Any,
    field_name: str,
    expected_value: Any,
    message: Optional[str] = None
) -> None:
    """
    Validate that a specific field has expected value in database.
    
    Args:
        session: SQLAlchemy session
        model_class: SQLAlchemy model class
        record_id: Record ID to check
        field_name: Name of field to validate
        expected_value: Expected field value
        message: Optional custom error message
        
    Raises:
        ValidationError: If field value doesn't match expected
    """
    record = session.query(model_class).filter(
        model_class.id == record_id
    ).first()
    
    if not record:
        raise ValidationError(f"Record with id {record_id} not found in {model_class.__tablename__}")
    
    actual_value = getattr(record, field_name)
    
    if actual_value != expected_value:
        error_msg = message or (
            f"Field {field_name} in {model_class.__tablename__} has value {actual_value}, "
            f"expected {expected_value}"
        )
        raise ValidationError(error_msg)


def validate_db_relationship(
    session: Session,
    parent_record: Any,
    relationship_name: str,
    expected_count: Optional[int] = None,
    message: Optional[str] = None
) -> None:
    """
    Validate database relationship exists and optionally has expected count.
    
    Args:
        session: SQLAlchemy session
        parent_record: Parent record object
        relationship_name: Name of relationship attribute
        expected_count: Optional expected count of related records
        message: Optional custom error message
        
    Raises:
        ValidationError: If relationship validation fails
    """
    if not hasattr(parent_record, relationship_name):
        raise ValidationError(
            f"Relationship {relationship_name} not found on {type(parent_record).__name__}"
        )
    
    related = getattr(parent_record, relationship_name)
    
    if expected_count is not None:
        # Handle both single relationships and collections
        if hasattr(related, '__len__'):
            actual_count = len(related)
        else:
            actual_count = 1 if related is not None else 0
        
        if actual_count != expected_count:
            error_msg = message or (
                f"Relationship {relationship_name} has {actual_count} records, "
                f"expected {expected_count}"
            )
            raise ValidationError(error_msg)
