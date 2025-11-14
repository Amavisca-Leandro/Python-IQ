"""
Integration tests for database framework.

This module tests the complete database integration including:
- DatabaseManager with connection pooling
- SQLAlchemy models with relationships
- TestDataFactory with automatic cleanup
"""

import pytest
from sqlalchemy import text

from core.database.models import User, UserProfile
from core.database.manager import DatabaseManager
from core.database.factory import TestDataFactory, TestDataContext


@pytest.mark.database
@pytest.mark.integration
class TestDatabaseManager:
    """Test DatabaseManager functionality."""
    
    def test_database_connection(self, db_manager: DatabaseManager):
        """Test basic database connectivity."""
        with db_manager.get_session() as session:
            result = session.execute(text("SELECT 1 as value"))
            value = result.scalar()
            assert value == 1
    
    def test_create_test_data_with_orm(self, db_manager: DatabaseManager, test_data_context: TestDataContext):
        """Test creating data using ORM."""
        user_data = {
            "username": f"test_user_{test_data_context.test_id}",
            "email": f"test_{test_data_context.test_id}@example.com",
            "password": "SecurePassword123!",
            "is_active": True
        }
        
        user = db_manager.create_test_data(User, user_data)
        
        assert user.id is not None
        assert user.username == user_data["username"]
        assert user.email == user_data["email"]
        assert user.is_active is True
    
    def test_verify_data_exists(self, db_manager: DatabaseManager, db_session):
        """Test data existence verification."""
        # Create a user
        user = User(
            username="verify_test_user",
            email="verify@example.com",
            password="password123"
        )
        db_session.add(user)
        db_session.flush()
        
        # Verify it exists
        exists = db_manager.verify_data_exists(
            User,
            username="verify_test_user"
        )
        
        assert exists is True
        
        # Verify non-existent data
        not_exists = db_manager.verify_data_exists(
            User,
            username="nonexistent_user"
        )
        
        assert not_exists is False
    
    def test_query_data_as_dict(self, db_manager: DatabaseManager, db_session):
        """Test querying data and returning as dictionaries."""
        # Create test users
        user1 = User(username="query_user1", email="query1@example.com", password="pass")
        user2 = User(username="query_user2", email="query2@example.com", password="pass")
        db_session.add_all([user1, user2])
        db_session.flush()
        
        # Query users
        results = db_manager.query_data(
            "SELECT id, username, email FROM users WHERE username LIKE :pattern",
            {"pattern": "query_user%"}
        )
        
        assert len(results) >= 2
        assert all(isinstance(row, dict) for row in results)
        assert all("username" in row for row in results)


@pytest.mark.database
@pytest.mark.integration
class TestSQLAlchemyModels:
    """Test SQLAlchemy models."""
    
    def test_user_model_creation(self, db_session):
        """Test User model creation."""
        user = User(
            username="model_test_user",
            email="model@example.com",
            password="SecurePass123!",
            first_name="Test",
            last_name="User"
        )
        
        db_session.add(user)
        db_session.flush()
        
        assert user.id is not None
        assert user.username == "model_test_user"
        assert user.full_name == "Test User"
        assert user.is_active is True
        assert user.is_admin is False
    
    def test_user_profile_relationship(self, db_session):
        """Test User and UserProfile relationship."""
        # Create user
        user = User(
            username="relationship_user",
            email="relationship@example.com",
            password="password"
        )
        db_session.add(user)
        db_session.flush()
        
        # Create profile
        profile = UserProfile(
            user_id=user.id,
            full_name="Relationship Test User",
            phone="+5511999999999",
            city="São Paulo",
            state="SP"
        )
        db_session.add(profile)
        db_session.flush()
        
        # Test relationship
        assert user.profile is not None
        assert user.profile.id == profile.id
        assert profile.user.id == user.id
    
    def test_user_convenience_methods(self, db_session):
        """Test User model convenience methods."""
        user = User(
            username="convenience_user",
            email="convenience@example.com",
            password="password"
        )
        db_session.add(user)
        db_session.flush()
        
        # Test activation/deactivation
        user.deactivate()
        assert user.is_active is False
        
        user.activate()
        assert user.is_active is True
        
        # Test admin privileges
        user.make_admin()
        assert user.is_admin is True
        
        user.revoke_admin()
        assert user.is_admin is False
        
        # Test to_dict
        user_dict = user.to_dict()
        assert isinstance(user_dict, dict)
        assert user_dict["username"] == "convenience_user"


@pytest.mark.database
@pytest.mark.integration
class TestDataFactoryIntegration:
    """Test TestDataFactory with database integration."""
    
    def test_create_user_data(self, test_data_factory: TestDataFactory, test_data_context: TestDataContext):
        """Test creating user data."""
        user_data = test_data_factory.create_user_data(
            test_id=test_data_context.test_id,
            email="custom@example.com"
        )
        
        assert "username" in user_data
        assert user_data["email"] == "custom@example.com"
        assert "password" in user_data
        assert user_data["is_active"] is True
    
    def test_create_user_with_profile(
        self,
        test_data_factory: TestDataFactory,
        test_data_context: TestDataContext,
        db_manager: DatabaseManager
    ):
        """Test creating complete user with profile."""
        result = test_data_factory.create_user_with_profile(
            test_id=test_data_context.test_id,
            email="withprofile@example.com",
            profile={"phone": "+5511988887777"}
        )
        
        assert "user" in result
        assert "profile" in result
        assert result["user"].id is not None
        assert result["profile"].id is not None
        assert result["user"].email == "withprofile@example.com"
        assert result["profile"].phone == "+5511988887777"
        
        # Verify in database
        with db_manager.get_session() as session:
            user = session.query(User).filter(User.id == result["user_id"]).first()
            assert user is not None
            assert user.profile is not None
    
    def test_create_multiple_users(
        self,
        test_data_factory: TestDataFactory,
        test_data_context: TestDataContext
    ):
        """Test creating multiple users."""
        users = test_data_factory.create_multiple_users(
            test_id=test_data_context.test_id,
            count=3,
            with_profiles=True
        )
        
        assert len(users) == 3
        assert all("user_id" in user for user in users)
        assert all("profile_id" in user for user in users)
    
    def test_cleanup_test_data(
        self,
        test_data_factory: TestDataFactory,
        test_data_context: TestDataContext,
        db_manager: DatabaseManager
    ):
        """Test automatic cleanup of test data."""
        # Create user with profile
        result = test_data_factory.create_user_with_profile(
            test_id=test_data_context.test_id
        )
        
        user_id = result["user_id"]
        profile_id = result["profile_id"]
        
        # Verify data exists
        assert db_manager.verify_data_exists(User, id=user_id)
        assert db_manager.verify_data_exists(UserProfile, id=profile_id)
        
        # Cleanup
        test_data_factory.cleanup_test_data(test_data_context.test_id)
        
        # Verify data is deleted
        assert not db_manager.verify_data_exists(User, id=user_id)
        assert not db_manager.verify_data_exists(UserProfile, id=profile_id)
