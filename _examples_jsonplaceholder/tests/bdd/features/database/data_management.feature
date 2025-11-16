@database @integration
Feature: Database Data Management
  As a QA engineer
  I want to create and manage test data in the database
  So that I can validate database operations and data integrity

  Background:
    Given the database is connected and ready

  @data_creation @smoke
  Scenario: Create and query test user
    Given I have a test user with email "test.user@example.com"
    When I query the database for user with email "test.user@example.com"
    Then the user should exist in the database
    And the user should have field "email" equal to "test.user@example.com"
    And the user should be active

  @data_creation
  Scenario: Create test user with username
    Given I have a test user with username "testuser123"
    When I query the database for user with username "testuser123"
    Then the user should exist in the database
    And the user should have field "username" equal to "testuser123"
    And the database record should have field "is_active" with value "True"

  @data_creation @profile
  Scenario: Create test user with profile
    Given I have a test user with profile
    Then the user should exist in the database
    And the user profile should exist

  @data_creation @bulk
  Scenario: Create multiple test users
    Given I have 5 test users
    When I query all users from the database
    Then the database should contain at least 5 users
    And each user should have a valid email

  @data_validation @api_integration
  Scenario: Validate database state after API operation
    Given the API client is configured
    And I have a test user with email "api.test@example.com"
    When I query the database for user with email "api.test@example.com"
    Then the user should exist in the database
    And the user should have field "email" equal to "api.test@example.com"
    When I send a GET request to "/users/1"
    Then the response status code should be 200
    And the response should be a dictionary

  @data_cleanup @smoke
  Scenario: Demonstrate test data cleanup
    Given I have a test user with email "cleanup.test@example.com"
    When I query the database for user with email "cleanup.test@example.com"
    Then the user should exist in the database
    # Note: Cleanup happens automatically after scenario via test_data_context fixture

  @query @advanced
  Scenario: Execute custom SQL query
    Given I have 3 test users
    When I execute SQL query:
      """
      SELECT COUNT(*) as user_count FROM users WHERE is_active = true
      """
    Then the database query should return 1 records

  @query @filter
  Scenario: Query users by field value
    Given I have a test user with username "filtertest"
    When I query the database for users where username equals "filtertest"
    Then the database should contain 1 users

  @data_creation @table
  Scenario: Create test data from table specification
    Given I create test data using factory:
      | type | username    | email                  |
      | User | tableuser1  | table1@example.com     |
      | User | tableuser2  | table2@example.com     |
    When I query the database for user with email "table1@example.com"
    Then the user should exist in the database
    And the user should have field "username" equal to "tableuser1"

  @validation @state
  Scenario: Validate database field values
    Given I have a test user with email "validation.test@example.com"
    When I query the database for user with email "validation.test@example.com"
    Then the user should exist in the database
    And the database record should have field "is_active" with value "True"
    And the user should be active

  @integration @end_to_end
  Scenario: End-to-end database and API integration
    Given the API client is configured
    And I have a test user with email "e2e.test@example.com"
    When I query the database for user with email "e2e.test@example.com"
    Then the user should exist in the database
    And the user should have field "email" equal to "e2e.test@example.com"
    When I send a GET request to "/posts"
    Then the response status code should be 200
    And the response should be a non-empty list
    When I query all users from the database
    Then the database should contain at least 1 users

  @query @id
  Scenario: Query user by ID
    Given I have a test user with email "id.query@example.com"
    When I query the database for user with email "id.query@example.com"
    Then the user should exist in the database
    When I query the database for user with id 1
    Then the user should exist in the database

  @validation @negative
  Scenario: Verify non-existent user
    When I query the database for user with email "nonexistent@example.com"
    Then the user should not exist in the database

  @data_creation @validation
  Scenario: Create user and validate all fields
    Given I have a test user with email "complete.test@example.com"
    When I query the database for user with email "complete.test@example.com"
    Then the user should exist in the database
    And the user should have field "email" equal to "complete.test@example.com"
    And the user should be active
    And each user should have a valid email
