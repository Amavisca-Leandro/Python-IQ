"""
Database integration module for test automation.

This module provides database connectivity, ORM models, and test data
factory for comprehensive test data management.
"""

from core.database.manager import DatabaseManager
from core.database.factory import TestDataFactory, TestDataContext
from core.database.models import Base, User, UserProfile


__all__ = [
    "DatabaseManager",
    "TestDataFactory",
    "TestDataContext",
    "Base",
    "User",
    "UserProfile",
]
