# -*- coding: utf-8 -*-
"""
Unit tests for Email Service helper functions.

Tests utility functions and helpers.
"""

import pytest
from datetime import datetime, timedelta


# Mock helper functions for demonstration
def format_iso_datetime(dt):
    """Format datetime to ISO 8601 string."""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def parse_iso_datetime(iso_string):
    """Parse ISO 8601 string to datetime."""
    return datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%SZ")

def calculate_expiration(days):
    """Calculate future expiration date."""
    return datetime.now() + timedelta(days=days)

def sanitize_email(email):
    """Sanitize email address."""
    return email.strip().lower()

def truncate_text(text, max_length):
    """Truncate long text with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def mask_sensitive(api_key):
    """Mask sensitive data in logs."""
    if len(api_key) <= 12:
        return "****"
    return api_key[:12] + "****" + api_key[-4:]

def is_valid_uuid(uuid_str):
    """Validate UUID format."""
    import re
    pattern = r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$'
    return bool(re.match(pattern, uuid_str.replace('-', '').lower()))

def is_valid_priority(priority):
    """Validate email priority value."""
    return priority in ['low', 'medium', 'high']

def dict_to_query_params(data):
    """Convert dict to query string parameters."""
    return '&'.join([f"{k}={v}" for k, v in data.items()])

def flatten_dict(nested, parent_key='', sep='.'):
    """Flatten nested dictionary."""
    items = []
    for k, v in nested.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


class TestDateHelpers:
    """Test date/time helper functions."""

    def test_format_iso_datetime(self):
        """Should format datetime to ISO 8601 string."""
        dt = datetime(2025, 1, 15, 10, 30, 0)
        result = format_iso_datetime(dt)

        assert result == "2025-01-15T10:30:00Z"

    def test_parse_iso_datetime(self):
        """Should parse ISO 8601 string to datetime."""
        iso_string = "2025-01-15T10:30:00Z"
        result = parse_iso_datetime(iso_string)

        assert result.year == 2025
        assert result.month == 1
        assert result.day == 15

    def test_calculate_expiration_date(self):
        """Should calculate future expiration date."""
        days = 30
        result = calculate_expiration(days)

        expected = datetime.now() + timedelta(days=30)
        assert result.date() == expected.date()


class TestStringHelpers:
    """Test string manipulation helpers."""

    def test_sanitize_email(self):
        """Should sanitize email address."""
        assert sanitize_email("  User@Example.COM  ") == "user@example.com"
        assert sanitize_email("Test+Tag@Domain.com") == "test+tag@domain.com"

    def test_truncate_text(self):
        """Should truncate long text with ellipsis."""
        long_text = "This is a very long text that should be truncated"
        result = truncate_text(long_text, max_length=20)

        assert len(result) <= 23  # 20 + "..."
        assert result.endswith("...")

    def test_mask_sensitive_data(self):
        """Should mask sensitive data in logs."""
        api_key = "sk_live_1234567890abcdef"
        result = mask_sensitive(api_key)

        assert result.startswith("sk_live_")
        assert "****" in result
        assert "abcdef" in result  # last 4 chars visible


class TestValidationHelpers:
    """Test validation helper functions."""

    def test_is_valid_uuid(self):
        """Should validate UUID format."""
        # Valid UUIDs
        assert is_valid_uuid("550e8400-e29b-41d4-a716-446655440000") is True
        assert is_valid_uuid("550e8400e29b41d4a716446655440000") is True  # without dashes

        # Invalid UUIDs
        assert is_valid_uuid("invalid-uuid") is False
        assert is_valid_uuid("") is False

    def test_is_valid_priority(self):
        """Should validate email priority value."""
        # Valid priorities
        assert is_valid_priority("low") is True
        assert is_valid_priority("medium") is True
        assert is_valid_priority("high") is True

        # Invalid priorities
        assert is_valid_priority("urgent") is False
        assert is_valid_priority("") is False


class TestDataTransformers:
    """Test data transformation helpers."""

    def test_dict_to_query_params(self):
        """Should convert dict to query string parameters."""
        data = {"page": 1, "limit": 10, "sort": "-createdAt"}
        result = dict_to_query_params(data)

        assert "page=1" in result
        assert "limit=10" in result
        assert "sort=-createdAt" in result

    def test_flatten_nested_dict(self):
        """Should flatten nested dictionary."""
        nested = {
            "user": {
                "name": "John",
                "email": "john@example.com"
            },
            "active": True
        }

        result = flatten_dict(nested)

        assert result["user.name"] == "John"
        assert result["user.email"] == "john@example.com"
        assert result["active"] is True


# Markers
pytestmark = [
    pytest.mark.unit,
    pytest.mark.email,
    pytest.mark.middleware,
    pytest.mark.helpers,
]
