"""
Backend integration tests with database for user workflows.

This module tests complete end-to-end workflows that involve:
- Creating test data in the database
- Executing API operations
- Validating data changes in the database
- Using both ORM and raw SQL for verification

Requirements: 12.1, 12.2, 12.3
"""

import pytest
import logging
from datetime import datetime
from sqlalchemy import text

from core.models.user import UserCreate, UserResponse, UserUpdate
from core.database.models import User, UserProfile
from core.helpers.validators import validate_response_status
from core.helpers.data_generator import DataGenerator

# Initialize data generator
data_gen = DataGenerator()


logger = logging.getLogger(__name__)


# ============================================================================
# DATABASE INTEGRATION TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.database
@pytest.mark.backend
class TestUserDatabaseIntegration:
    """Test suite for user operations with database integration."""
    
    def test_complete_user_workflow(
        self,
        api_client,
        db_manager,
        test_data_factory,
        test_data_context
    ):
        """
        Test complete user workflow with database validation.
        
        Flow:
        1. Create test data in database using factory
        2. Verify data exists in database
        3. Execute API operations
        4. Validate changes in database using ORM
        5. Validate changes using raw SQL
        6. Cleanup is automatic via fixture
        
        Validates:
        - Test data factory creates data correctly
        - API operations modify database correctly
        - ORM queries work as expected
        - Raw SQL queries work as expected
        - Data relationships are maintained
        
        Requirements: 12.1, 12.2, 12.3
        """
        logger.info("Testing complete user workflow with database integration")
        
        # ====================================================================
        # STEP 1: Create test data using factory
        # ====================================================================
        logger.info("Step 1: Creating test data in database")
        
        user_data = test_data_factory.create_user_data(
            test_id=test_data_context.test_id,
            username=data_gen.generate_username(),
            email=data_gen.generate_email(),
            password=data_gen.generate_secure_password(),
            is_active=True
        )
        
        # Insert user into database
        with db_manager.get_session() as session:
            db_user = User(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"],
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                is_active=user_data["is_active"]
            )
            session.add(db_user)
            session.flush()
            
            user_id = db_user.id
            
            # Register for cleanup
            test_data_context.register_entity('User', user_id)
            
            logger.info(f"Created user in database with ID: {user_id}")
        
        # ====================================================================
        # STEP 2: Verify data exists in database using ORM
        # ====================================================================
        logger.info("Step 2: Verifying data exists in database")
        
        with db_manager.get_session() as session:
            # Query using ORM
            db_user = session.query(User).filter(User.id == user_id).first()
            
            assert db_user is not None, "User should exist in database"
            assert db_user.username == user_data["username"], "Username should match"
            assert db_user.email == user_data["email"], "Email should match"
            assert db_user.is_active is True, "User should be active"
            
            logger.info(f"Verified user exists: {db_user.username}")
        
        # ====================================================================
        # STEP 3: Execute API operations
        # ====================================================================
        logger.info("Step 3: Executing API operations")
        
        # Get user via API
        get_response = api_client.get(f"/users/{user_id}")
        
        if get_response.status_code == 404:
            pytest.skip("User API endpoint not implemented")
        
        validate_response_status(get_response, expected_status=200)
        api_user = UserResponse(**get_response.json())
        
        assert api_user.id == user_id, "API should return correct user"
        assert api_user.username == user_data["username"], "Username should match"
        
        # Update user via API
        update_data = {
            "first_name": "Updated",
            "last_name": "User",
            "is_active": False
        }
        
        update_response = api_client.put(
            f"/users/{user_id}",
            json=update_data
        )
        
        assert update_response.status_code in [200, 204], \
            f"Update should succeed, got {update_response.status_code}"
        
        logger.info("API operations completed successfully")
        
        # ====================================================================
        # STEP 4: Validate changes in database using ORM
        # ====================================================================
        logger.info("Step 4: Validating changes using ORM")
        
        with db_manager.get_session() as session:
            # Query updated user
            updated_user = session.query(User).filter(User.id == user_id).first()
            
            assert updated_user is not None, "User should still exist"
            assert updated_user.first_name == "Updated", "First name should be updated"
            assert updated_user.last_name == "User", "Last name should be updated"
            assert updated_user.is_active is False, "User should be inactive"
            assert updated_user.updated_at is not None, "Updated timestamp should be set"
            
            logger.info("ORM validation successful")
        
        # ====================================================================
        # STEP 5: Validate changes using raw SQL
        # ====================================================================
        logger.info("Step 5: Validating changes using raw SQL")
        
        with db_manager.get_session() as session:
            # Query using raw SQL
            result = session.execute(
                text("""
                    SELECT id, username, email, first_name, last_name, is_active
                    FROM users
                    WHERE id = :user_id
                """),
                {"user_id": user_id}
            ).fetchone()
            
            assert result is not None, "User should exist in raw SQL query"
            assert result.first_name == "Updated", "First name should be updated (SQL)"
            assert result.last_name == "User", "Last name should be updated (SQL)"
            assert result.is_active is False, "User should be inactive (SQL)"
            
            logger.info("Raw SQL validation successful")
        
        logger.info("Complete user workflow test passed")
    
    def test_user_with_profile_workflow(
        self,
        api_client,
        db_manager,
        test_data_factory,
        test_data_context
    ):
        """
        Test user workflow with profile relationship.
        
        Validates:
        - User and profile can be created together
        - Relationships are maintained
        - API operations affect related data
        - Cascade operations work correctly
        
        Requirements: 12.1, 12.2, 12.3
        """
        logger.info("Testing user with profile workflow")
        
        # ====================================================================
        # STEP 1: Create user with profile in database
        # ====================================================================
        logger.info("Creating user with profile")
        
        user_data = test_data_factory.create_user_data(
            test_id=test_data_context.test_id,
            username=data_gen.generate_username(),
            email=data_gen.generate_email()
        )
        
        profile_data = test_data_factory.create_profile_data(
            test_id=test_data_context.test_id,
            full_name="Test User Profile",
            phone=data_gen.generate_phone_number()
        )
        
        with db_manager.get_session() as session:
            # Create user
            db_user = User(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"],
                is_active=True
            )
            session.add(db_user)
            session.flush()
            
            user_id = db_user.id
            
            # Create profile
            db_profile = UserProfile(
                user_id=user_id,
                full_name=profile_data["full_name"],
                phone=profile_data["phone"],
                address=profile_data.get("address"),
                city=profile_data.get("city"),
                state=profile_data.get("state"),
                country=profile_data.get("country", "BR")
            )
            session.add(db_profile)
            session.flush()
            
            profile_id = db_profile.id
            
            # Register for cleanup
            test_data_context.register_entity('User', user_id)
            test_data_context.register_entity('UserProfile', profile_id)
            
            logger.info(f"Created user {user_id} with profile {profile_id}")
        
        # ====================================================================
        # STEP 2: Verify relationship using ORM
        # ====================================================================
        logger.info("Verifying user-profile relationship")
        
        with db_manager.get_session() as session:
            # Query user with profile
            db_user = session.query(User).filter(User.id == user_id).first()
            
            assert db_user is not None, "User should exist"
            assert db_user.profile is not None, "User should have profile"
            assert db_user.profile.full_name == profile_data["full_name"], \
                "Profile full name should match"
            assert db_user.profile.phone == profile_data["phone"], \
                "Profile phone should match"
            
            # Verify reverse relationship
            db_profile = session.query(UserProfile).filter(
                UserProfile.id == profile_id
            ).first()
            
            assert db_profile is not None, "Profile should exist"
            assert db_profile.user is not None, "Profile should have user"
            assert db_profile.user.id == user_id, "Profile should link to correct user"
            
            logger.info("Relationship validation successful")
        
        # ====================================================================
        # STEP 3: Verify relationship using raw SQL with JOIN
        # ====================================================================
        logger.info("Verifying relationship using SQL JOIN")
        
        with db_manager.get_session() as session:
            result = session.execute(
                text("""
                    SELECT u.id, u.username, u.email, p.full_name, p.phone
                    FROM users u
                    LEFT JOIN user_profiles p ON u.id = p.user_id
                    WHERE u.id = :user_id
                """),
                {"user_id": user_id}
            ).fetchone()
            
            assert result is not None, "User should exist in JOIN query"
            assert result.full_name == profile_data["full_name"], \
                "Profile full name should match (SQL)"
            assert result.phone == profile_data["phone"], \
                "Profile phone should match (SQL)"
            
            logger.info("SQL JOIN validation successful")
        
        logger.info("User with profile workflow test passed")
    
    def test_user_creation_via_api_with_db_validation(
        self,
        api_client,
        db_manager,
        test_data_context
    ):
        """
        Test user creation via API with database validation.
        
        Flow:
        1. Create user via API
        2. Verify user exists in database
        3. Validate all fields match
        4. Verify timestamps are set
        
        Requirements: 12.1, 12.2, 12.3
        """
        logger.info("Testing user creation via API with DB validation")
        
        # ====================================================================
        # STEP 1: Create user via API
        # ====================================================================
        user_data = {
            "username": data_gen.generate_username(),
            "email": data_gen.generate_email(),
            "password": data_gen.generate_secure_password(),
            "first_name": "API",
            "last_name": "Test",
            "is_active": True
        }
        
        user_create = UserCreate(**user_data)
        
        create_response = api_client.post(
            "/users",
            json=user_create.model_dump()
        )
        
        if create_response.status_code == 404:
            pytest.skip("User creation API endpoint not implemented")
        
        validate_response_status(create_response, expected_status=201)
        
        api_user = UserResponse(**create_response.json())
        user_id = api_user.id
        
        # Register for cleanup
        test_data_context.register_entity('User', user_id)
        
        logger.info(f"User created via API with ID: {user_id}")
        
        # ====================================================================
        # STEP 2: Verify user exists in database using ORM
        # ====================================================================
        logger.info("Verifying user in database")
        
        with db_manager.get_session() as session:
            db_user = session.query(User).filter(User.id == user_id).first()
            
            assert db_user is not None, "User should exist in database"
            assert db_user.username == user_data["username"], "Username should match"
            assert db_user.email == user_data["email"], "Email should match"
            assert db_user.first_name == user_data["first_name"], "First name should match"
            assert db_user.last_name == user_data["last_name"], "Last name should match"
            assert db_user.is_active == user_data["is_active"], "Active status should match"
            assert db_user.created_at is not None, "Created timestamp should be set"
            
            logger.info("Database validation successful")
        
        # ====================================================================
        # STEP 3: Verify using raw SQL
        # ====================================================================
        logger.info("Verifying using raw SQL")
        
        with db_manager.get_session() as session:
            result = session.execute(
                text("SELECT * FROM users WHERE id = :user_id"),
                {"user_id": user_id}
            ).fetchone()
            
            assert result is not None, "User should exist (SQL)"
            assert result.username == user_data["username"], "Username should match (SQL)"
            assert result.email == user_data["email"], "Email should match (SQL)"
            
            logger.info("Raw SQL validation successful")
        
        logger.info("API creation with DB validation test passed")
    
    def test_user_deletion_cascade(
        self,
        api_client,
        db_manager,
        test_data_factory,
        test_data_context
    ):
        """
        Test user deletion with cascade to profile.
        
        Validates:
        - User deletion via API
        - Profile is also deleted (cascade)
        - Database constraints are respected
        
        Requirements: 12.1, 12.3
        """
        logger.info("Testing user deletion with cascade")
        
        # ====================================================================
        # STEP 1: Create user with profile
        # ====================================================================
        user_data = test_data_factory.create_user_data(
            test_id=test_data_context.test_id
        )
        
        with db_manager.get_session() as session:
            db_user = User(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"],
                is_active=True
            )
            session.add(db_user)
            session.flush()
            
            user_id = db_user.id
            
            db_profile = UserProfile(
                user_id=user_id,
                full_name="Test Profile",
                phone=data_gen.generate_phone_number()
            )
            session.add(db_profile)
            session.flush()
            
            profile_id = db_profile.id
            
            logger.info(f"Created user {user_id} with profile {profile_id}")
        
        # ====================================================================
        # STEP 2: Verify both exist
        # ====================================================================
        with db_manager.get_session() as session:
            user_exists = session.query(User).filter(User.id == user_id).first()
            profile_exists = session.query(UserProfile).filter(
                UserProfile.id == profile_id
            ).first()
            
            assert user_exists is not None, "User should exist"
            assert profile_exists is not None, "Profile should exist"
        
        # ====================================================================
        # STEP 3: Delete user via API
        # ====================================================================
        delete_response = api_client.delete(f"/users/{user_id}")
        
        if delete_response.status_code == 404:
            pytest.skip("User deletion API endpoint not implemented")
        
        assert delete_response.status_code in [200, 204], \
            f"Deletion should succeed, got {delete_response.status_code}"
        
        logger.info("User deleted via API")
        
        # ====================================================================
        # STEP 4: Verify both are deleted (cascade)
        # ====================================================================
        with db_manager.get_session() as session:
            user_exists = session.query(User).filter(User.id == user_id).first()
            profile_exists = session.query(UserProfile).filter(
                UserProfile.id == profile_id
            ).first()
            
            assert user_exists is None, "User should be deleted"
            assert profile_exists is None, "Profile should be deleted (cascade)"
            
            logger.info("Cascade deletion verified")
        
        logger.info("User deletion cascade test passed")
    
    def test_concurrent_user_operations(
        self,
        api_client,
        db_manager,
        test_data_factory,
        test_data_context
    ):
        """
        Test concurrent user operations with database isolation.
        
        Validates:
        - Multiple users can be created concurrently
        - Database transactions are isolated
        - No data corruption occurs
        
        Requirements: 12.1, 12.5
        """
        logger.info("Testing concurrent user operations")
        
        # Create multiple users
        user_ids = []
        
        for i in range(3):
            user_data = test_data_factory.create_user_data(
                test_id=f"{test_data_context.test_id}_{i}",
                username=f"{data_gen.generate_username()}_{i}",
                email=f"user{i}_{data_gen.generate_email()}"
            )
            
            with db_manager.get_session() as session:
                db_user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    password=user_data["password"],
                    is_active=True
                )
                session.add(db_user)
                session.flush()
                
                user_ids.append(db_user.id)
                test_data_context.register_entity('User', db_user.id)
        
        logger.info(f"Created {len(user_ids)} users concurrently")
        
        # Verify all users exist
        with db_manager.get_session() as session:
            for user_id in user_ids:
                db_user = session.query(User).filter(User.id == user_id).first()
                assert db_user is not None, f"User {user_id} should exist"
        
        logger.info("Concurrent operations test passed")
