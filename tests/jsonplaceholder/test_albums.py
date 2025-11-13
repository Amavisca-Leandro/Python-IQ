"""
Tests for JSONPlaceholder Albums API endpoints.

This module contains tests for all albums-related endpoints including:
- GET /albums - List all albums
- GET /albums/{id} - Get specific album

Requirements covered:
- 5.1: Content-Type validation
- 5.5: Schema validation for albums
"""

import pytest
from core.helpers.validators import (
    validate_response_status,
    validate_json_schema,
    validate_required_fields,
    validate_field_types
)
from core.clients.jsonplaceholder_schemas import ALBUM_SCHEMA


# ============================================================================
# GET TESTS
# ============================================================================

@pytest.mark.smoke
def test_get_albums_returns_200_and_list(jsonplaceholder_client):
    """
    Test that GET /albums returns status 200 and a list of albums.
    
    Requirements: 5.1, 5.5
    """
    response = jsonplaceholder_client.get_albums()
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Validate response is a list
    albums = response.json()
    assert isinstance(albums, list), "Response should be a list"
    assert len(albums) > 0, "Albums list should not be empty"


@pytest.mark.smoke
@pytest.mark.validation
def test_get_albums_validates_schema(jsonplaceholder_client):
    """
    Test that GET /albums returns albums with valid JSON schema.
    
    Requirements: 5.5
    """
    response = jsonplaceholder_client.get_albums()
    validate_response_status(response, 200)
    
    albums = response.json()
    
    # Validate first album against schema
    assert len(albums) > 0, "Should have at least one album"
    validate_json_schema(albums[0], ALBUM_SCHEMA)


@pytest.mark.validation
def test_get_albums_validates_data_types(jsonplaceholder_client):
    """
    Test that GET /albums returns albums with correct data types.
    
    Requirements: 5.5
    """
    response = jsonplaceholder_client.get_albums()
    validate_response_status(response, 200)
    
    albums = response.json()
    assert len(albums) > 0, "Should have at least one album"
    
    # Validate types for first album
    album = albums[0]
    validate_field_types(album, {
        "userId": int,
        "id": int,
        "title": str
    })


@pytest.mark.smoke
def test_get_album_by_id_returns_specific_album(jsonplaceholder_client):
    """
    Test that GET /albums/{id} returns a specific album with correct fields.
    
    Requirements: 5.1, 5.5
    """
    album_id = 1
    response = jsonplaceholder_client.get_album(album_id)
    
    # Validate status code
    validate_response_status(response, 200)
    
    # Validate Content-Type
    assert "application/json" in response.headers.get("Content-Type", "")
    
    # Validate response structure
    album = response.json()
    assert isinstance(album, dict), "Response should be a dictionary"
    
    # Validate required fields
    validate_required_fields(album, ["userId", "id", "title"])
    
    # Validate the ID matches
    assert album["id"] == album_id, f"Album ID should be {album_id}"


@pytest.mark.validation
def test_get_album_by_id_validates_schema(jsonplaceholder_client):
    """
    Test that GET /albums/{id} returns album with valid JSON schema.
    
    Requirements: 5.5
    """
    response = jsonplaceholder_client.get_album(1)
    validate_response_status(response, 200)
    
    album = response.json()
    validate_json_schema(album, ALBUM_SCHEMA)


@pytest.mark.validation
def test_get_album_by_id_validates_data_types(jsonplaceholder_client):
    """
    Test that GET /albums/{id} returns album with correct data types.
    
    Requirements: 5.5
    """
    response = jsonplaceholder_client.get_album(1)
    validate_response_status(response, 200)
    
    album = response.json()
    validate_field_types(album, {
        "userId": int,
        "id": int,
        "title": str
    })
