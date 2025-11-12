"""
Example tests demonstrating the use of global fixtures.

This module shows how to use the various fixtures provided by conftest.py
for test automation.
"""

import pytest
from core.database.models import User, UserProfile


class TestFixturesExample:
    """Example tests using global fixtures."""
    
    def test_settings_fixture(self, settings):
        """Test that settings fixture provides configuration."""
        assert settings is not None
        assert settings.env in ["dev", "staging", "prod"]
        assert settings.api_base_url.startswith("http")
        assert settings.api_timeout > 0
    
    def test_api_client_fixture(self, api_client):
        """Test that API client fixture is configured."""
        assert api_client is not None
        assert api_client.base_url is not None
        assert api_client.timeout > 0
        # Note: This test doesn't make actual API calls
    
    def test_unauthenticated_api_client(self, unauthenticated_api_client):
        """Test that unauthenticated API client is available."""
        assert unauthenticated_api_client is not None
        assert not unauthenticated_api_client.is_authenticated()
    
    @pytest.mark.database
    @pytest.mark.skip(reason="Requires database connection")
    def test_db_manager_fixture(self, db_manager):
        """Test that database manager fixture is configured."""
        assert db_manager is not None
        assert db_manager.engine is not None
        assert db_manager.session_factory is not None
    
    @pytest.mark.database
    @pytest.mark.skip(reason="Requires database connection")
    def test_test_data_factory_fixture(self, test_data_factory):
        """Test that test data factory fixture is available."""
        assert test_data_factory is not None
        assert test_data_factory.faker is not None
    
    @pytest.mark.database
    @pytest.mark.skip(reason="Requires database connection")
    def test_test_data_context_fixture(self, test_data_context):
        """Test that test data context provides unique test_id."""
        assert test_data_context is not None
        assert test_data_context.test_id is not None
        assert test_data_context.test_id.startswith("test_")
        assert test_data_context.cleanup_required is True
    
    @pytest.mark.database
    @pytest.mark.skip(reason="Requires database connection")
    def test_test_data_context_isolation(self, test_data_context):
        """Test that each test gets a unique test_id."""
        # This test_id should be different from the previous test
        assert test_data_context is not None
        assert test_data_context.test_id is not None
        # Each test execution gets a unique ID
    
    @pytest.mark.database
    @pytest.mark.skip(reason="Requires database connection")
    def test_create_user_data(self, test_data_factory, test_data_context):
        """Test creating user data with factory."""
        user_data = test_data_factory.create_user_data(
            test_id=test_data_context.test_id,
            email="test@example.com"
        )
        
        assert user_data is not None
        assert user_data['email'] == "test@example.com"
        assert user_data['username'] is not None
        assert user_data['password'] is not None
        assert user_data['is_active'] is True
    
    @pytest.mark.database
    @pytest.mark.skip(reason="Requires database connection")
    def test_create_profile_data(self, test_data_factory, test_data_context):
        """Test creating profile data with factory."""
        profile_data = test_data_factory.create_profile_data(
            test_id=test_data_context.test_id,
            user_id=123
        )
        
        assert profile_data is not None
        assert profile_data['user_id'] == 123
        assert profile_data['full_name'] is not None
        assert profile_data['phone'] is not None
        assert profile_data['country'] == 'BR'
    
    @pytest.mark.database
    @pytest.mark.skip(reason="Requires database connection")
    def test_isolated_test_data_fixture(self, isolated_test_data):
        """Test that isolated_test_data provides both context and session."""
        context, session = isolated_test_data
        
        assert context is not None
        assert session is not None
        assert context.test_id is not None
    
    @pytest.mark.database
    @pytest.mark.skip(reason="Requires database connection")
    def test_db_session_fixture(self, db_session):
        """Test that database session fixture works."""
        assert db_session is not None
        # Session is automatically managed by the fixture
    
    def test_entity_registration(self):
        """Test registering entities in test data context."""
        # Create a standalone context for testing
        from core.database.factory import TestDataContext
        test_data_context = TestDataContext()
        
        # Register some test entities
        test_data_context.register_entity('User', 1)
        test_data_context.register_entity('User', 2)
        test_data_context.register_entity('UserProfile', 1)
        
        # Verify entities are tracked
        users = test_data_context.get_entities('User')
        assert len(users) == 2
        assert 1 in users
        assert 2 in users
        
        profiles = test_data_context.get_entities('UserProfile')
        assert len(profiles) == 1
        assert 1 in profiles


@pytest.mark.smoke
class TestFixturesIntegration:
    """Integration tests for fixtures working together."""
    
    def test_api_client_with_settings(self, api_client, settings):
        """Test that API client uses settings configuration."""
        assert api_client.base_url == settings.api_base_url
        assert api_client.timeout == settings.api_timeout
    
    @pytest.mark.database
    @pytest.mark.skip(reason="Requires database connection")
    def test_factory_with_context(self, test_data_factory, test_data_context):
        """Test that factory and context work together."""
        # Create user data
        user_data = test_data_factory.create_user_data(
            test_id=test_data_context.test_id
        )
        
        # Verify data is created with test prefix
        assert user_data['username'].startswith('test_')
        
        # Context should track cleanup
        assert test_data_context.cleanup_required is True
    
    @pytest.mark.database
    @pytest.mark.skip(reason="Requires database connection")
    def test_multiple_fixtures_together(
        self,
        settings,
        api_client,
        db_manager,
        test_data_factory,
        test_data_context
    ):
        """Test that all fixtures can be used together."""
        # All fixtures should be available
        assert settings is not None
        assert api_client is not None
        assert db_manager is not None
        assert test_data_factory is not None
        assert test_data_context is not None
        
        # They should be properly configured
        assert api_client.base_url == settings.api_base_url
        assert test_data_factory.faker is not None
        assert test_data_context.test_id is not None
