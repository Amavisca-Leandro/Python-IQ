"""Database-related step definitions for BDD tests."""

import allure
import logging
from pytest_bdd import given, when, then, parsers
from sqlalchemy import text
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Allure feature and story decorators for this module
allure.feature("Database Testing")
allure.story("Database Operations and Validation")


# ============================================================================
# DATA CREATION STEPS
# ============================================================================

@given(parsers.parse('I have a test user with email "{email}"'))
@allure.story("Test Data Creation")
def create_test_user(bdd_context, test_data_factory, test_data_context, db_manager, email):
    """
    Create a test user in the database with specified email.
    
    Args:
        bdd_context: BDD context for data sharing
        test_data_factory: Factory for creating test data
        test_data_context: Context for tracking test data
        db_manager: Database manager for session handling
        email: Email address for the user
    """
    with allure.step(f"Create test user with email {email}"):
        try:
            from core.database.models import User
            
            # Create user data
            user_data = test_data_factory.create_user_data(
                test_id=test_data_context.test_id,
                email=email
            )
            
            # Attach user data to Allure
            allure.attach(
                str(user_data),
                "User Data to Create",
                allure.attachment_type.JSON
            )
            
            # Create user in database
            with db_manager.get_session() as session:
                user = User(**user_data)
                session.add(user)
                session.flush()
                session.refresh(user)
                
                # Register for cleanup
                test_data_context.register_entity('User', user.id)
                
                # Store in context
                bdd_context.user = user
                bdd_context.user_id = user.id
                bdd_context.user_email = user.email
                
                allure.attach(
                    f"User ID: {user.id}\nUsername: {user.username}\nEmail: {user.email}",
                    "Created User",
                    allure.attachment_type.TEXT
                )
                
                logger.info(f"Created test user with id={user.id}, email={email}")
                
        except Exception as e:
            # Attach error details to Allure
            allure.attach(
                str(e),
                name="Error Details",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"Email: {email}",
                name="Failed User Creation Details",
                attachment_type=allure.attachment_type.TEXT
            )
            logger.error(f"Failed to create test user: {e}")
            raise


@given(parsers.parse('I have a test user with username "{username}"'))
def create_test_user_with_username(
    bdd_context,
    test_data_factory,
    test_data_context,
    db_manager,
    username
):
    """
    Create a test user in the database with specified username.
    
    Args:
        bdd_context: BDD context for data sharing
        test_data_factory: Factory for creating test data
        test_data_context: Context for tracking test data
        db_manager: Database manager for session handling
        username: Username for the user
    """
    with allure.step(f"Create test user with username {username}"):
        from core.database.models import User
        
        # Create user data
        user_data = test_data_factory.create_user_data(
            test_id=test_data_context.test_id,
            username=username
        )
        
        # Create user in database
        with db_manager.get_session() as session:
            user = User(**user_data)
            session.add(user)
            session.flush()
            session.refresh(user)
            
            # Register for cleanup
            test_data_context.register_entity('User', user.id)
            
            # Store in context
            bdd_context.user = user
            bdd_context.user_id = user.id
            bdd_context.username = user.username
            
            allure.attach(
                f"User ID: {user.id}\nUsername: {user.username}\nEmail: {user.email}",
                "Created User",
                allure.attachment_type.TEXT
            )
            
            logger.info(f"Created test user with id={user.id}, username={username}")


@given("I have a test user with profile")
def create_test_user_with_profile(
    bdd_context,
    test_data_factory,
    test_data_context
):
    """
    Create a test user with complete profile in the database.
    
    Args:
        bdd_context: BDD context for data sharing
        test_data_factory: Factory for creating test data
        test_data_context: Context for tracking test data
    """
    with allure.step("Create test user with profile"):
        # Use factory method that handles both user and profile creation
        result = test_data_factory.create_user_with_profile(
            test_id=test_data_context.test_id
        )
        
        # Store in context
        bdd_context.user = result['user']
        bdd_context.profile = result['profile']
        bdd_context.user_id = result['user_id']
        bdd_context.profile_id = result['profile_id']
        
        allure.attach(
            f"User ID: {result['user_id']}\n"
            f"Username: {result['username']}\n"
            f"Email: {result['email']}\n"
            f"Profile ID: {result['profile_id']}",
            "Created User with Profile",
            allure.attachment_type.TEXT
        )
        
        logger.info(
            f"Created test user with profile: user_id={result['user_id']}, "
            f"profile_id={result['profile_id']}"
        )


@given(parsers.parse('I have {count:d} test users'))
def create_multiple_test_users(
    bdd_context,
    test_data_factory,
    test_data_context,
    count
):
    """
    Create multiple test users in the database.
    
    Args:
        bdd_context: BDD context for data sharing
        test_data_factory: Factory for creating test data
        test_data_context: Context for tracking test data
        count: Number of users to create
    """
    with allure.step(f"Create {count} test users"):
        # Create multiple users without profiles for simplicity
        users = test_data_factory.create_multiple_users(
            test_id=test_data_context.test_id,
            count=count,
            with_profiles=False
        )
        
        # Store in context
        bdd_context.users = users
        bdd_context.user_count = len(users)
        
        user_ids = [user['user_id'] for user in users]
        allure.attach(
            f"Created {count} users\nUser IDs: {user_ids}",
            "Created Users",
            allure.attachment_type.TEXT
        )
        
        logger.info(f"Created {count} test users with IDs: {user_ids}")


@given(parsers.parse('I create test data using factory:\n{data_table}'))
def create_test_data_from_table(
    bdd_context,
    test_data_factory,
    test_data_context,
    db_manager,
    data_table
):
    """
    Create test data from a data table specification.
    
    Args:
        bdd_context: BDD context for data sharing
        test_data_factory: Factory for creating test data
        test_data_context: Context for tracking test data
        db_manager: Database manager for session handling
        data_table: Gherkin data table with entity specifications
    """
    with allure.step("Create test data from table"):
        from core.database.models import User, UserProfile
        
        # Parse data table
        lines = data_table.strip().split('\n')
        if len(lines) < 2:
            raise ValueError("Data table must have header and at least one data row")
        
        # Parse header
        header = [col.strip() for col in lines[0].split('|')[1:-1]]
        
        # Parse data rows
        created_entities = []
        for line in lines[1:]:
            if '|' not in line:
                continue
            
            values = [val.strip() for val in line.split('|')[1:-1]]
            if len(values) != len(header):
                continue
            
            row_data = dict(zip(header, values))
            
            # Determine entity type
            entity_type = row_data.get('type', 'User')
            
            if entity_type == 'User':
                # Create user
                user_data = test_data_factory.create_user_data(
                    test_id=test_data_context.test_id,
                    username=row_data.get('username'),
                    email=row_data.get('email')
                )
                
                with db_manager.get_session() as session:
                    user = User(**user_data)
                    session.add(user)
                    session.flush()
                    session.refresh(user)
                    
                    test_data_context.register_entity('User', user.id)
                    created_entities.append({'type': 'User', 'id': user.id, 'entity': user})
        
        # Store in context
        bdd_context.created_entities = created_entities
        
        entity_summary = '\n'.join([
            f"{e['type']} ID: {e['id']}" for e in created_entities
        ])
        allure.attach(
            entity_summary,
            "Created Entities",
            allure.attachment_type.TEXT
        )
        
        logger.info(f"Created {len(created_entities)} entities from data table")


# ============================================================================
# DATABASE QUERY STEPS
# ============================================================================

@when(parsers.parse('I query the database for user with email "{email}"'))
@allure.story("Database Queries")
def query_user_by_email(bdd_context, db_manager, email):
    """
    Query database for user by email address.
    
    Args:
        bdd_context: BDD context for data sharing
        db_manager: Database manager for session handling
        email: Email address to search for
    """
    with allure.step(f"Query user with email {email}"):
        try:
            from core.database.models import User
            
            with db_manager.get_session() as session:
                user = session.query(User).filter(User.email == email).first()
                
                # Store in context
                bdd_context.db_result = user
                bdd_context.queried_user = user
                
                if user:
                    allure.attach(
                        f"Found User:\nID: {user.id}\nUsername: {user.username}\nEmail: {user.email}",
                        "Query Result",
                        allure.attachment_type.TEXT
                    )
                    logger.info(f"Found user with email {email}: id={user.id}")
                else:
                    allure.attach(
                        f"No user found with email: {email}",
                        "Query Result",
                        allure.attachment_type.TEXT
                    )
                    logger.info(f"No user found with email {email}")
                    
        except Exception as e:
            # Attach error details to Allure
            allure.attach(
                str(e),
                name="Error Details",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                f"Email: {email}",
                name="Failed Query Details",
                attachment_type=allure.attachment_type.TEXT
            )
            logger.error(f"Failed to query user by email: {e}")
            raise


@when(parsers.parse('I query the database for user with username "{username}"'))
def query_user_by_username(bdd_context, db_manager, username):
    """
    Query database for user by username.
    
    Args:
        bdd_context: BDD context for data sharing
        db_manager: Database manager for session handling
        username: Username to search for
    """
    with allure.step(f"Query user with username {username}"):
        from core.database.models import User
        
        with db_manager.get_session() as session:
            user = session.query(User).filter(User.username == username).first()
            
            # Store in context
            bdd_context.db_result = user
            bdd_context.queried_user = user
            
            if user:
                allure.attach(
                    f"Found User:\nID: {user.id}\nUsername: {user.username}\nEmail: {user.email}",
                    "Query Result",
                    allure.attachment_type.TEXT
                )
                logger.info(f"Found user with username {username}: id={user.id}")
            else:
                allure.attach(
                    f"No user found with username: {username}",
                    "Query Result",
                    allure.attachment_type.TEXT
                )
                logger.info(f"No user found with username {username}")


@when(parsers.parse('I query the database for user with id {user_id:d}'))
def query_user_by_id(bdd_context, db_manager, user_id):
    """
    Query database for user by ID.
    
    Args:
        bdd_context: BDD context for data sharing
        db_manager: Database manager for session handling
        user_id: User ID to search for
    """
    with allure.step(f"Query user with id {user_id}"):
        from core.database.models import User
        
        with db_manager.get_session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            
            # Store in context
            bdd_context.db_result = user
            bdd_context.queried_user = user
            
            if user:
                allure.attach(
                    f"Found User:\nID: {user.id}\nUsername: {user.username}\nEmail: {user.email}",
                    "Query Result",
                    allure.attachment_type.TEXT
                )
                logger.info(f"Found user with id {user_id}")
            else:
                allure.attach(
                    f"No user found with id: {user_id}",
                    "Query Result",
                    allure.attachment_type.TEXT
                )
                logger.info(f"No user found with id {user_id}")


@when(parsers.parse('I query the database for users where {field} equals "{value}"'))
def query_users_by_field(bdd_context, db_manager, field, value):
    """
    Query database for users by any field value.
    
    Args:
        bdd_context: BDD context for data sharing
        db_manager: Database manager for session handling
        field: Field name to filter by
        value: Value to match
    """
    with allure.step(f"Query users where {field} equals {value}"):
        from core.database.models import User
        
        with db_manager.get_session() as session:
            # Build query dynamically
            query = session.query(User)
            
            # Apply filter
            if hasattr(User, field):
                query = query.filter(getattr(User, field) == value)
                users = query.all()
                
                # Store in context
                bdd_context.db_results = users
                bdd_context.queried_users = users
                
                allure.attach(
                    f"Found {len(users)} users where {field} = {value}",
                    "Query Result",
                    allure.attachment_type.TEXT
                )
                logger.info(f"Found {len(users)} users where {field} = {value}")
            else:
                raise AttributeError(f"User model does not have field '{field}'")


@when(parsers.parse('I execute SQL query:\n{sql_query}'))
@allure.story("Database Queries")
def execute_custom_sql_query(bdd_context, db_manager, sql_query):
    """
    Execute custom SQL query and store results.
    
    Args:
        bdd_context: BDD context for data sharing
        db_manager: Database manager for session handling
        sql_query: SQL query to execute
    """
    with allure.step("Execute custom SQL query"):
        try:
            # Clean up the query (remove extra whitespace)
            sql_query = sql_query.strip()
            
            with db_manager.get_session() as session:
                result = session.execute(text(sql_query))
                
                # Fetch results
                rows = result.fetchall()
                
                # Convert to list of dictionaries
                if rows:
                    columns = result.keys()
                    results = [dict(zip(columns, row)) for row in rows]
                else:
                    results = []
                
                # Store in context
                bdd_context.db_results = results
                bdd_context.sql_query_results = results
                
                allure.attach(
                    sql_query,
                    "SQL Query",
                    allure.attachment_type.TEXT
                )
                allure.attach(
                    f"Returned {len(results)} rows",
                    "Query Result Count",
                    allure.attachment_type.TEXT
                )
                
                # Attach query results if not too large
                if results and len(results) <= 100:
                    import json
                    allure.attach(
                        json.dumps(results, indent=2, default=str),
                        "Query Results",
                        allure.attachment_type.JSON
                    )
                
                logger.info(f"Executed SQL query, returned {len(results)} rows")
                
        except Exception as e:
            # Attach error details to Allure
            allure.attach(
                str(e),
                name="Error Details",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                sql_query,
                name="Failed SQL Query",
                attachment_type=allure.attachment_type.TEXT
            )
            logger.error(f"Failed to execute SQL query: {e}")
            raise


@when(parsers.parse('I query all users from the database'))
def query_all_users(bdd_context, db_manager):
    """
    Query all users from the database.
    
    Args:
        bdd_context: BDD context for data sharing
        db_manager: Database manager for session handling
    """
    with allure.step("Query all users from database"):
        from core.database.models import User
        
        with db_manager.get_session() as session:
            users = session.query(User).all()
            
            # Store in context
            bdd_context.db_results = users
            bdd_context.all_users = users
            
            allure.attach(
                f"Found {len(users)} total users in database",
                "Query Result",
                allure.attachment_type.TEXT
            )
            logger.info(f"Queried all users: found {len(users)} users")


# ============================================================================
# DATABASE VALIDATION STEPS
# ============================================================================

@then("the user should exist in the database")
@allure.story("Database Validation")
def verify_user_exists(bdd_context):
    """
    Verify that a user exists in the database.
    
    Args:
        bdd_context: BDD context for data sharing
    """
    with allure.step("Verify user exists in database"):
        assert bdd_context.db_result is not None, \
            "User should exist in database but was not found"
        
        allure.attach(
            "User exists in database",
            "Validation Result",
            allure.attachment_type.TEXT
        )
        logger.info("Verified user exists in database")


@then("the user should not exist in the database")
def verify_user_not_exists(bdd_context):
    """
    Verify that a user does not exist in the database.
    
    Args:
        bdd_context: BDD context for data sharing
    """
    with allure.step("Verify user does not exist in database"):
        assert bdd_context.db_result is None, \
            "User should not exist in database but was found"
        
        allure.attach(
            "User does not exist in database",
            "Validation Result",
            allure.attachment_type.TEXT
        )
        logger.info("Verified user does not exist in database")


@then(parsers.parse('the database record should have field "{field}" with value "{value}"'))
@allure.story("Database Validation")
def verify_db_field_value(bdd_context, field, value):
    """
    Verify database field has expected value.
    
    Args:
        bdd_context: BDD context for data sharing
        field: Field name to check
        value: Expected value
    """
    with allure.step(f"Verify database field '{field}' equals '{value}'"):
        record = bdd_context.db_result
        
        assert record is not None, "No database record found in context"
        
        # Get field value
        if hasattr(record, field):
            actual_value = str(getattr(record, field))
        else:
            raise AttributeError(f"Record does not have field '{field}'")
        
        assert actual_value == value, \
            f"Expected field '{field}' to be '{value}', but got '{actual_value}'"
        
        allure.attach(
            f"Field '{field}' has expected value '{value}'",
            "Validation Result",
            allure.attachment_type.TEXT
        )
        logger.info(f"Verified database field {field} = {value}")


@then(parsers.parse('the database should contain {count:d} users'))
@allure.story("Database Validation")
def verify_user_count(bdd_context, count):
    """
    Verify the number of users in query results.
    
    Args:
        bdd_context: BDD context for data sharing
        count: Expected number of users
    """
    with allure.step(f"Verify database contains {count} users"):
        results = bdd_context.get('db_results', [])
        actual_count = len(results)
        
        assert actual_count == count, \
            f"Expected {count} users, but found {actual_count}"
        
        allure.attach(
            f"Database contains {count} users as expected",
            "Validation Result",
            allure.attachment_type.TEXT
        )
        logger.info(f"Verified database contains {count} users")


@then(parsers.parse('the database should contain at least {min_count:d} users'))
def verify_minimum_user_count(bdd_context, min_count):
    """
    Verify minimum number of users in query results.
    
    Args:
        bdd_context: BDD context for data sharing
        min_count: Minimum expected number of users
    """
    with allure.step(f"Verify database contains at least {min_count} users"):
        results = bdd_context.get('db_results', [])
        actual_count = len(results)
        
        assert actual_count >= min_count, \
            f"Expected at least {min_count} users, but found {actual_count}"
        
        allure.attach(
            f"Database contains {actual_count} users (minimum {min_count})",
            "Validation Result",
            allure.attachment_type.TEXT
        )
        logger.info(f"Verified database contains at least {min_count} users (found {actual_count})")


@then(parsers.parse('the user should have field "{field}" equal to "{value}"'))
def verify_user_field_value(bdd_context, field, value):
    """
    Verify user field has expected value.
    
    Args:
        bdd_context: BDD context for data sharing
        field: Field name to check
        value: Expected value
    """
    with allure.step(f"Verify user field '{field}' equals '{value}'"):
        user = bdd_context.get('queried_user') or bdd_context.get('user')
        
        assert user is not None, "No user found in context"
        
        # Get field value
        if hasattr(user, field):
            actual_value = str(getattr(user, field))
        else:
            raise AttributeError(f"User does not have field '{field}'")
        
        assert actual_value == value, \
            f"Expected user field '{field}' to be '{value}', but got '{actual_value}'"
        
        allure.attach(
            f"User field '{field}' has expected value '{value}'",
            "Validation Result",
            allure.attachment_type.TEXT
        )
        logger.info(f"Verified user field {field} = {value}")


@then(parsers.parse('the user should be active'))
def verify_user_is_active(bdd_context):
    """
    Verify user is active.
    
    Args:
        bdd_context: BDD context for data sharing
    """
    with allure.step("Verify user is active"):
        user = bdd_context.get('queried_user') or bdd_context.get('user')
        
        assert user is not None, "No user found in context"
        assert user.is_active is True, \
            f"Expected user to be active, but is_active = {user.is_active}"
        
        allure.attach(
            "User is active",
            "Validation Result",
            allure.attachment_type.TEXT
        )
        logger.info("Verified user is active")


@then(parsers.parse('the user should not be active'))
def verify_user_is_not_active(bdd_context):
    """
    Verify user is not active.
    
    Args:
        bdd_context: BDD context for data sharing
    """
    with allure.step("Verify user is not active"):
        user = bdd_context.get('queried_user') or bdd_context.get('user')
        
        assert user is not None, "No user found in context"
        assert user.is_active is False, \
            f"Expected user to be inactive, but is_active = {user.is_active}"
        
        allure.attach(
            "User is not active",
            "Validation Result",
            allure.attachment_type.TEXT
        )
        logger.info("Verified user is not active")


@then(parsers.parse('the database query should return {count:d} records'))
def verify_query_record_count(bdd_context, count):
    """
    Verify the number of records returned by a query.
    
    Args:
        bdd_context: BDD context for data sharing
        count: Expected number of records
    """
    with allure.step(f"Verify query returned {count} records"):
        results = bdd_context.get('sql_query_results') or bdd_context.get('db_results', [])
        actual_count = len(results)
        
        assert actual_count == count, \
            f"Expected query to return {count} records, but got {actual_count}"
        
        allure.attach(
            f"Query returned {count} records as expected",
            "Validation Result",
            allure.attachment_type.TEXT
        )
        
        # Attach query results summary
        if results:
            results_summary = f"Total records: {actual_count}\n"
            if isinstance(results[0], dict):
                results_summary += f"Fields: {', '.join(results[0].keys())}"
            
            allure.attach(
                results_summary,
                "Query Results Summary",
                allure.attachment_type.TEXT
            )
        
        logger.info(f"Verified query returned {count} records")


@then(parsers.parse('each user should have a valid email'))
def verify_users_have_valid_email(bdd_context):
    """
    Verify all users have valid email addresses.
    
    Args:
        bdd_context: BDD context for data sharing
    """
    with allure.step("Verify all users have valid email"):
        users = bdd_context.get('db_results') or bdd_context.get('all_users', [])
        
        assert len(users) > 0, "No users found to validate"
        
        import re
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        
        invalid_emails = []
        for user in users:
            email = user.email if hasattr(user, 'email') else user.get('email')
            if not email or not email_pattern.match(email):
                invalid_emails.append(email)
        
        assert len(invalid_emails) == 0, \
            f"Found {len(invalid_emails)} users with invalid emails: {invalid_emails}"
        
        allure.attach(
            f"All {len(users)} users have valid email addresses",
            "Validation Result",
            allure.attachment_type.TEXT
        )
        logger.info(f"Verified all {len(users)} users have valid emails")


@then(parsers.parse('the user profile should exist'))
def verify_user_profile_exists(bdd_context, db_manager):
    """
    Verify user has an associated profile.
    
    Args:
        bdd_context: BDD context for data sharing
        db_manager: Database manager for session handling
    """
    with allure.step("Verify user profile exists"):
        user = bdd_context.get('queried_user') or bdd_context.get('user')
        
        assert user is not None, "No user found in context"
        
        from core.database.models import UserProfile
        
        with db_manager.get_session() as session:
            profile = session.query(UserProfile).filter(
                UserProfile.user_id == user.id
            ).first()
            
            assert profile is not None, \
                f"User {user.id} should have a profile but none was found"
            
            # Store profile in context
            bdd_context.profile = profile
            
            allure.attach(
                f"User {user.id} has profile with ID {profile.id}",
                "Validation Result",
                allure.attachment_type.TEXT
            )
            logger.info(f"Verified user {user.id} has profile {profile.id}")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

import logging
logger = logging.getLogger(__name__)
