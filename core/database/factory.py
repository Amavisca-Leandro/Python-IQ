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

    __test__ = False  # Tell pytest this is not a test class

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

    __test__ = False  # Tell pytest this is not a test class

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
        
        This method deletes all tracked entities from the database in
        reverse order to respect foreign key constraints.
        
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
        
        # Cleanup via database if available
        if self.db_manager:
            try:
                self._cleanup_database_entities(test_id, context)
            except Exception as e:
                logger.error(f"Error during database cleanup for test {test_id}: {e}")
        
        # Clear tracking
        context.clear()
        del self.created_entities[test_id]
        
        logger.info(f"Cleanup completed for test {test_id}")
    
    def _cleanup_database_entities(self, test_id: str, context: TestDataContext):
        """
        Cleanup database entities in reverse order.
        
        Args:
            test_id: Test identifier
            context: Test data context
        """
        from core.database.models import User, UserProfile
        
        # Define cleanup order (reverse of creation to respect FK constraints)
        cleanup_order = [
            ('UserProfile', UserProfile),
            ('User', User),
            # Add more models here as needed
        ]
        
        with self.db_manager.get_session() as session:
            for entity_type, model_class in cleanup_order:
                entity_ids = context.get_entities(entity_type)
                
                if not entity_ids:
                    continue
                
                try:
                    # Delete entities
                    deleted_count = session.query(model_class).filter(
                        model_class.id.in_(entity_ids)
                    ).delete(synchronize_session=False)
                    
                    logger.debug(
                        f"Deleted {deleted_count} {entity_type} entities "
                        f"for test {test_id}"
                    )
                except Exception as e:
                    logger.error(
                        f"Error deleting {entity_type} entities "
                        f"for test {test_id}: {e}"
                    )
                    # Continue with other entities even if one fails
            
            # Commit all deletions
            session.commit()
            logger.debug(f"Database cleanup committed for test {test_id}")
    
    def create_user_with_profile(
        self,
        test_id: str,
        **overrides
    ) -> Dict[str, Any]:
        """
        Create complete user with profile using database.
        
        This method creates a user and associated profile in the database,
        tracks them for cleanup, and returns both instances.
        
        Args:
            test_id: Test identifier
            **overrides: Override default values (can include 'profile' dict for profile overrides)
            
        Returns:
            Dict[str, Any]: Dictionary with 'user' and 'profile' keys
            
        Example:
            >>> result = factory.create_user_with_profile(
            ...     test_id="test_123",
            ...     email="custom@example.com",
            ...     profile={"phone": "+5511999999999"}
            ... )
            >>> user = result['user']
            >>> profile = result['profile']
        """
        if not self.db_manager:
            raise ValueError("DatabaseManager is required for create_user_with_profile")
        
        # Import models here to avoid circular imports
        from core.database.models import User, UserProfile
        
        # Extract profile overrides
        profile_overrides = overrides.pop('profile', {})
        
        # Create user data
        user_data = self.create_user_data(test_id, **overrides)
        
        # Create user in database
        with self.db_manager.get_session() as session:
            # Create user
            user = User(**user_data)
            session.add(user)
            session.flush()  # Get user.id
            
            # Register user for cleanup
            self._register_for_cleanup(test_id, 'User', user.id)
            
            # Create profile data
            profile_data = self.create_profile_data(
                test_id,
                user_id=user.id,
                **profile_overrides
            )
            
            # Create profile
            profile = UserProfile(**profile_data)
            session.add(profile)
            session.flush()
            
            # Register profile for cleanup
            self._register_for_cleanup(test_id, 'UserProfile', profile.id)
            
            # Refresh to get all database values
            session.refresh(user)
            session.refresh(profile)
            
            logger.info(
                f"Created user with profile for test {test_id}: "
                f"user_id={user.id}, profile_id={profile.id}"
            )
            
            # Return as dictionary to avoid session issues
            return {
                'user': user,
                'profile': profile,
                'user_id': user.id,
                'profile_id': profile.id,
                'username': user.username,
                'email': user.email,
            }
    
    def create_multiple_users(
        self,
        test_id: str,
        count: int = 3,
        with_profiles: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Create multiple users for bulk testing scenarios.
        
        Args:
            test_id: Test identifier
            count: Number of users to create
            with_profiles: Whether to create profiles for each user
            
        Returns:
            List[Dict[str, Any]]: List of created user data
            
        Example:
            >>> users = factory.create_multiple_users(
            ...     test_id="test_123",
            ...     count=5,
            ...     with_profiles=True
            ... )
            >>> assert len(users) == 5
        """
        users = []
        
        for i in range(count):
            if with_profiles:
                user_data = self.create_user_with_profile(
                    test_id=test_id,
                    username=f"{self.settings.test_data_prefix}user_{i}_{test_id}"
                )
            else:
                if not self.db_manager:
                    raise ValueError("DatabaseManager is required for create_multiple_users")
                
                from core.database.models import User
                
                user_dict = self.create_user_data(
                    test_id=test_id,
                    username=f"{self.settings.test_data_prefix}user_{i}_{test_id}"
                )
                
                with self.db_manager.get_session() as session:
                    user = User(**user_dict)
                    session.add(user)
                    session.flush()
                    session.refresh(user)
                    
                    self._register_for_cleanup(test_id, 'User', user.id)
                    
                    user_data = {
                        'user': user,
                        'user_id': user.id,
                        'username': user.username,
                        'email': user.email,
                    }
            
            users.append(user_data)
        
        logger.info(f"Created {count} users for test {test_id}")
        
        return users
    
    def create_complete_order_scenario(
        self,
        test_id: str,
        user_id: Optional[int] = None,
        **overrides
    ) -> Dict[str, Any]:
        """
        Create complete order scenario with user, items, and payment.
        
        This is a placeholder for complex scenarios. Implement based on
        your application's domain model.
        
        Args:
            test_id: Test identifier
            user_id: Existing user ID (creates new user if not provided)
            **overrides: Override default values
            
        Returns:
            Dict[str, Any]: Complete order scenario data
            
        Example:
            >>> scenario = factory.create_complete_order_scenario(
            ...     test_id="test_123",
            ...     order_total=100.00
            ... )
        """
        # Create user if not provided
        if user_id is None:
            user_data = self.create_user_with_profile(test_id)
            user_id = user_data['user_id']
        
        # This is a placeholder - implement based on your domain model
        scenario_data = {
            'test_id': test_id,
            'user_id': user_id,
            'order_id': None,  # Would be created in actual implementation
            'items': [],  # Would contain order items
            'payment': None,  # Would contain payment info
            **overrides
        }
        
        logger.info(f"Created order scenario for test {test_id} with user_id={user_id}")
        
        return scenario_data
    
    def get_test_context(self, test_id: str) -> Optional[TestDataContext]:
        """
        Get test data context for a test.
        
        Args:
            test_id: Test identifier
            
        Returns:
            Optional[TestDataContext]: Test data context or None
        """
        return self.created_entities.get(test_id)
