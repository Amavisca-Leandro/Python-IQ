"""
JSONPlaceholder API JSON Schemas.

This module defines JSON schemas for validating responses from the JSONPlaceholder API.
Each schema follows the JSON Schema specification and defines the structure, required
fields, and data types for each resource type.

The schemas are used with jsonschema library to validate API responses and ensure
data integrity in automated tests.

Resources:
- Posts: Blog posts with userId, title, and body
- Users: User profiles with contact and address information
- Comments: Comments on posts with email and body
- Todos: Todo items with completion status
- Albums: Photo albums associated with users

Example:
    >>> from jsonschema import validate
    >>> from core.clients.jsonplaceholder_schemas import POST_SCHEMA
    >>> 
    >>> post_data = {
    ...     "userId": 1,
    ...     "id": 1,
    ...     "title": "Test Post",
    ...     "body": "Post content"
    ... }
    >>> validate(instance=post_data, schema=POST_SCHEMA)
"""

# ============================================================================
# POST SCHEMA
# ============================================================================

POST_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title", "body"],
    "properties": {
        "userId": {
            "type": "integer",
            "description": "ID of the user who created the post"
        },
        "id": {
            "type": "integer",
            "description": "Unique identifier for the post"
        },
        "title": {
            "type": "string",
            "description": "Title of the post"
        },
        "body": {
            "type": "string",
            "description": "Content/body of the post"
        }
    },
    "additionalProperties": False
}

# ============================================================================
# USER SCHEMA
# ============================================================================

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "username", "email"],
    "properties": {
        "id": {
            "type": "integer",
            "description": "Unique identifier for the user"
        },
        "name": {
            "type": "string",
            "description": "Full name of the user"
        },
        "username": {
            "type": "string",
            "description": "Username for the user"
        },
        "email": {
            "type": "string",
            "format": "email",
            "description": "Email address of the user"
        },
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "suite": {"type": "string"},
                "city": {"type": "string"},
                "zipcode": {"type": "string"},
                "geo": {
                    "type": "object",
                    "properties": {
                        "lat": {"type": "string"},
                        "lng": {"type": "string"}
                    }
                }
            },
            "description": "Address information for the user"
        },
        "phone": {
            "type": "string",
            "description": "Phone number of the user"
        },
        "website": {
            "type": "string",
            "description": "Website URL of the user"
        },
        "company": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "catchPhrase": {"type": "string"},
                "bs": {"type": "string"}
            },
            "description": "Company information for the user"
        }
    },
    "additionalProperties": False
}

# ============================================================================
# COMMENT SCHEMA
# ============================================================================

COMMENT_SCHEMA = {
    "type": "object",
    "required": ["postId", "id", "name", "email", "body"],
    "properties": {
        "postId": {
            "type": "integer",
            "description": "ID of the post this comment belongs to"
        },
        "id": {
            "type": "integer",
            "description": "Unique identifier for the comment"
        },
        "name": {
            "type": "string",
            "description": "Name/title of the comment"
        },
        "email": {
            "type": "string",
            "format": "email",
            "description": "Email address of the comment author"
        },
        "body": {
            "type": "string",
            "description": "Content/body of the comment"
        }
    },
    "additionalProperties": False
}

# ============================================================================
# TODO SCHEMA
# ============================================================================

TODO_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title", "completed"],
    "properties": {
        "userId": {
            "type": "integer",
            "description": "ID of the user who owns this todo"
        },
        "id": {
            "type": "integer",
            "description": "Unique identifier for the todo"
        },
        "title": {
            "type": "string",
            "description": "Title/description of the todo task"
        },
        "completed": {
            "type": "boolean",
            "description": "Completion status of the todo"
        }
    },
    "additionalProperties": False
}

# ============================================================================
# ALBUM SCHEMA
# ============================================================================

ALBUM_SCHEMA = {
    "type": "object",
    "required": ["userId", "id", "title"],
    "properties": {
        "userId": {
            "type": "integer",
            "description": "ID of the user who owns this album"
        },
        "id": {
            "type": "integer",
            "description": "Unique identifier for the album"
        },
        "title": {
            "type": "string",
            "description": "Title of the album"
        }
    },
    "additionalProperties": False
}

# ============================================================================
# SCHEMA REGISTRY
# ============================================================================

SCHEMAS = {
    "post": POST_SCHEMA,
    "user": USER_SCHEMA,
    "comment": COMMENT_SCHEMA,
    "todo": TODO_SCHEMA,
    "album": ALBUM_SCHEMA
}
"""
Registry of all available schemas for easy lookup.

Example:
    >>> from core.clients.jsonplaceholder_schemas import SCHEMAS
    >>> post_schema = SCHEMAS["post"]
    >>> user_schema = SCHEMAS["user"]
"""
