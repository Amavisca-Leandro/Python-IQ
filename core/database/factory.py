"""
Test data factory for creating and managing test data.

This module provides a TestDataFactory class that uses the factory pattern
to create test data with automatic tracking and cleanup.
"""

import logging
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime

from faker import Faker

from core.config.settings import get_settings


logger = logging.getLogger(__name__)


class TestDataContext:
    """
    Context for test data with unique identifier and tracking.
    
    Attributes:
        test_id: Unique identifier for the test
        created_entities: Dictionary tracking created entities by type
        cleanup_required: Whether cleanup is needed
    """
    
    def __init__(self, test_id: Optional[str] = None):
        """
        Initialize test data context.
        
        Args:
            test_id: Unique test identifier (auto-generated if not provided)
        """
        self.test_id = test_id or self._generate_test_id()
        self.created_entities: Dict[str, List[Any]] = {}
        self.cleanup_required = True
        
        logger.debug(f"TestDataContext created with test_id: {self.test_id}")
    
    @staticmethod
    def _generate_test_id() -> str:
        """
        Generate unique test ID.
        
        Returns:
            str: Unique test identifier
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"test_{timestamp}_{unique_id}"
    
    def register_entity(self, entity_type: str, entity_id: Any):
        """
        Register created entity for tracking.
        
        Args:
            entity_type: Type of entity (e.g., 'User', 'Order')
            entity_id: Entity identifier
        """
        if entity_type not in self.created_entities:
            self.created_entities[entity_type] = []
        
        self.created_entities[entity_type].append(entity_id)
        logger.debug(f"Registered {entity_type} with id {entity_id} for test {self.test_id}")
    
    def get_entities(self, entity_type: str) -> List[Any]:
        """
        Get all registered entities of a specific type.
        
        Args:
            entity_type: Type of entity
            
        Returns:
            List[Any]: List of entity IDs
        """
        return self.created_entities.get(entity_type, [])
    
    def clear(self):
        """Clear all tracked entities."""
        self.created_entities.clear()
        logger.debug(f"Cleared all entities for test {self.test_id}")


class TestDataFactory:
    """
    Factory for creating test data with automatic tracking and cleanup.
    
    Features:
    - Factory pattern for consistent data creation
    - Faker integration for realistic test data
    - Automatic entity tracking for cleanup
    - Support for complex data scenarios
    - Brazilian locale support
    
    Example:
        >>> factory = TestDataFactory(db_manager)
        >>> user_data = factory.create_user_data(test_id="test_123")
        >>> print(user_data['email'])
    """
    
    def __init__(self, db_manager: Any = None):
        """
        Initialize test data factory.
        
        Args:
            db_manager: DatabaseManager instance (optional)
        """
        self.settings = get_settings()
        self.db_manager = db_manager
        
        # Initialize Faker with configured locale
        self.faker = Faker(self.settings.faker_locale)
        
        # Set seed for reproducible data if configured
        if self.settings.faker_seed:
            Faker.seed(self.settings.faker_seed)
        
        # Track created entities by test_id
        self.created_entities: Dict[str, TestDataContext] = {}
        
        logger.info(f"TestDataFactory initialized with locale: {self.settings.faker_locale}")
    
    def _register_for_cleanup(
        self,
        test_id: str,
        entity_type: str,
        entity_id: Any
    ):
        """
        Register entity for cleanup.
        
        Args:
            test_id: Test identifier
            entity_type: Type of entity
            entity_id: Entity identifier
        """
        if not self.settings.enable_data_factory_tracking:
            return
        
        if test_id not in self.created_entities:
            self.created_entities[test_id] = TestDataContext(test_id)
        
        self.created_entities[test_id].register_entity(entity_type, entity_id)
    
    def create_user_data(
        self,
        test_id: str,
        **overrides
    ) -> Dict[str, Any]:
        """
        Create user test data.
        
        Args:
            test_id: Test identifier
            **overrides: Override default values
            
        Returns:
            Dict[str, Any]: User data dictionary
            
        Example:
            >>> user_data = factory.create_user_data(
            ...     test_id="test_123",
            ...     email="custom@example.com"
            ... )
        """
        user_data = {
            "username": self.faker.user_name(),
            "email": self.faker.email(),
            "password": self._generate_secure_password(),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "is_active": True,
            "created_at": datetime.now(),
            **overrides
        }
        
        # Add test prefix if configured
        if self.settings.test_data_prefix:
            user_data["username"] = f"{self.settings.test_data_prefix}{user_data['username']}"
        
        logger.debug(f"Created user data for test {test_id}: {user_data['username']}")
        
        return user_data
    
    def create_profile_data(
        self,
        test_id: str,
        user_id: Optional[int] = None,
        **overrides
    ) -> Dict[str, Any]:
        """
        Create user profile test data.
        
        Args:
            test_id: Test identifier
            user_id: Associated user ID
            **overrides: Override default values
            
        Returns:
            Dict[str, Any]: Profile data dictionary
        """
        profile_data = {
            "user_id": user_id,
            "full_name": self.faker.name(),
            "phone": self.faker.phone_number(),
            "address": self.faker.address(),
            "city": self.faker.city(),
            "state": self.faker.state_abbr(),
            "country": "BR",
            "postal_code": self.faker.postcode(),
            **overrides
        }
        
        logger.debug(f"Created profile data for test {test_id}")
        
        return profile_data
    
    def _generate_secure_password(self, length: int = 12) -> str:
        """
        Generate secure password.
        
        Args:
            length: Password length
            
        Returns:
            str: Secure password
        """
        return self.faker.password(
            length=length,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True
        )
    
    def cleanup_test_data(self, test_id: str):
        """
        Cleanup all test data for a specific test.
        
        Args:
            test_id: Test identifier
        """
        if not self.settings.auto_cleanup_test_data:
            logger.info(f"Auto cleanup disabled, skipping cleanup for test {test_id}")
            return
        
        if test_id not in self.created_entities:
            logger.debug(f"No entities to cleanup for test {test_id}")
            return
        
        context = self.created_entities[test_id]
        
        if not context.cleanup_required:
            logger.debug(f"Cleanup not required for test {test_id}")
            return
        
        logger.info(f"Cleaning up test data for test {test_id}")
        
        # Cleanup via database manager if available
        if self.db_manager:
            try:
                self.db_manager.cleanup_by_test_id(test_id)
            except Exception as e:
                logger.error(f"Error during cleanup for test {test_id}: {e}")
        
        # Clear tracking
        context.clear()
        del self.created_entities[test_id]
        
        logger.info(f"Cleanup completed for test {test_id}")
    
    def get_test_context(self, test_id: str) -> Optional[TestDataContext]:
        """
        Get test data context for a test.
        
        Args:
            test_id: Test identifier
            
        Returns:
            Optional[TestDataContext]: Test data context or None
        """
        return self.created_entities.get(test_id)
