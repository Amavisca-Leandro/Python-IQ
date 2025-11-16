@database @backend
Feature: Database User Management
  As a QA engineer
  I want to create and query users in the database
  So that I can validate database operations

  @smoke
  Scenario: Create and query a test user by email
    Given I have a test user with email "test.user@example.com"
    When I query the database for user with email "test.user@example.com"
    Then the user should exist in the database
    And the user should have field "email" equal to "test.user@example.com"
    And the user should be active

  @smoke
  Scenario: Create and query a test user by username
    Given I have a test user with username "testuser123"
    When I query the database for user with username "testuser123"
    Then the user should exist in the database
    And the user should have field "username" equal to "testuser123"

  Scenario: Create user with profile
    Given I have a test user with profile
    Then the user should exist in the database
    And the user profile should exist

  Scenario: Create multiple users
    Given I have 3 test users
    When I query all users from the database
    Then the database should contain at least 3 users
    And each user should have a valid email

  Scenario: Query non-existent user
    When I query the database for user with email "nonexistent@example.com"
    Then the user should not exist in the database
