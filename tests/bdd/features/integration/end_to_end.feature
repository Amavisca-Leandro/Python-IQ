@integration @end_to_end @smoke
Feature: End-to-End API and Database Integration
  As a QA engineer
  I want to test complete workflows combining API calls and database validation
  So that I can ensure data flows correctly through the entire system

  Background:
    Given the API client is configured

  @crud @data_flow @database
  Scenario: Create user in database and validate via API calls
    Given the database is connected and ready
    And I have a test user with email "e2e.integration@example.com"
    When I query the database for user with email "e2e.integration@example.com"
    Then the user should exist in the database
    And the user should have field "email" equal to "e2e.integration@example.com"
    And the user should be active
    When I send a GET request to "/posts"
    Then the response status code should be 200
    And the response should be a non-empty list
    And the response list should have at least 10 items
    When I send a GET request to "/posts/1"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "userId"
    And the response should contain field "title"

  @crud @multi_step @data_sharing
  Scenario: Multi-step API workflow with context data sharing
    # Step 1: Get all posts and store count
    When I send a GET request to "/posts"
    Then the response status code should be 200
    And the response should be a non-empty list
    
    # Step 2: Create a new post
    Given I have post data:
      | field  | value                                |
      | userId | 1                                    |
      | title  | E2E Integration Test Post            |
      | body   | Testing end-to-end data flow         |
    When I send a POST request to "/posts" with the post data
    Then the response status code should be 201
    And the response should be a dictionary
    And the response should contain field "id"
    And the response field "title" should equal "E2E Integration Test Post"
    And the response field "body" should equal "Testing end-to-end data flow"
    
    # Step 3: Update the created post
    Given I have post data:
      | field  | value                                |
      | userId | 1                                    |
      | id     | 101                                  |
      | title  | Updated E2E Integration Test Post    |
      | body   | Updated content for testing          |
    When I send a PUT request to "/posts/101" with the post data
    Then the response status code should be 200
    And the response should be a dictionary
    And the response field "title" should equal "Updated E2E Integration Test Post"
    
    # Step 4: Verify the update
    When I send a GET request to "/posts/101"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response field "id" should equal "101"

  @database @api @validation
  Scenario: Database state validation after API operations
    Given the database is connected and ready
    # Create test user in database
    And I have a test user with email "api.validation@example.com"
    When I query the database for user with email "api.validation@example.com"
    Then the user should exist in the database
    And the user should be active
    
    # Perform API operations
    When I send a GET request to "/users"
    Then the response status code should be 200
    And the response should be a non-empty list
    
    # Validate database state remains consistent
    When I query the database for user with email "api.validation@example.com"
    Then the user should exist in the database
    And the user should have field "email" equal to "api.validation@example.com"
    
    # Perform more API operations
    When I send a GET request to "/posts?userId=1"
    Then the response status code should be 200
    And the response should be a non-empty list
    And each post should have required fields:
      | userId |
      | id     |
      | title  |
      | body   |

  @complex @data_flow @multiple_entities @database
  Scenario: Complex workflow with multiple database entities and API calls
    Given the database is connected and ready
    # Create multiple test users
    And I have 3 test users
    When I query all users from the database
    Then the database should contain at least 3 users
    And each user should have a valid email
    
    # Perform API operations for different users
    When I send a GET request to "/posts?userId=1"
    Then the response status code should be 200
    And the response should be a non-empty list
    
    When I send a GET request to "/posts?userId=2"
    Then the response status code should be 200
    And the response should be a non-empty list
    
    # Create new post via API
    Given I have post data:
      | field  | value                                |
      | userId | 1                                    |
      | title  | Multi-Entity Test Post               |
      | body   | Testing with multiple database users |
    When I send a POST request to "/posts" with the post data
    Then the response status code should be 201
    And the response should contain field "id"
    
    # Verify database state
    When I query all users from the database
    Then the database should contain at least 3 users

  @api @database @sequential
  Scenario: Sequential API calls with database validation at each step
    Given the database is connected and ready
    # Step 1: Initial database setup
    And I have a test user with username "sequential_test"
    When I query the database for user with username "sequential_test"
    Then the user should exist in the database
    And the user should have field "username" equal to "sequential_test"
    
    # Step 2: First API call
    When I send a GET request to "/posts/1"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "userId"
    And the response field "userId" should equal "1"
    
    # Step 3: Database validation after API call
    When I query the database for user with username "sequential_test"
    Then the user should exist in the database
    
    # Step 4: Second API call
    When I send a GET request to "/users/1"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "id"
    
    # Step 5: Final database validation
    When I query all users from the database
    Then the database should contain at least 1 users

  @crud @full_cycle @database
  Scenario: Full CRUD cycle with database and API integration
    Given the database is connected and ready
    # Setup: Create database user
    And I have a test user with email "crud.cycle@example.com"
    When I query the database for user with email "crud.cycle@example.com"
    Then the user should exist in the database
    
    # CREATE: Create a new post via API
    Given I have post data:
      | field  | value                    |
      | userId | 1                        |
      | title  | CRUD Cycle Test Post     |
      | body   | Testing full CRUD cycle  |
    When I send a POST request to "/posts" with the post data
    Then the response status code should be 201
    And the response should contain field "id"
    
    # READ: Get the created post
    When I send a GET request to "/posts/101"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response field "title" should equal "CRUD Cycle Test Post"
    
    # UPDATE: Update the post
    Given I have post data:
      | field  | value                            |
      | userId | 1                                |
      | id     | 101                              |
      | title  | Updated CRUD Cycle Test Post     |
      | body   | Updated content                  |
    When I send a PUT request to "/posts/101" with the post data
    Then the response status code should be 200
    And the response field "title" should equal "Updated CRUD Cycle Test Post"
    
    # DELETE: Delete the post
    When I send a DELETE request to "/posts/101"
    Then the response status code should be 200
    
    # Verify database user still exists
    When I query the database for user with email "crud.cycle@example.com"
    Then the user should exist in the database

  @data_sharing @context @database
  Scenario: Demonstrate bdd_context usage for data sharing between steps
    Given the database is connected and ready
    # Create user and store in context
    And I have a test user with email "context.sharing@example.com"
    
    # Context automatically shares user data between steps
    When I query the database for user with email "context.sharing@example.com"
    Then the user should exist in the database
    
    # Make API call - response stored in context
    When I send a GET request to "/posts/1"
    Then the response status code should be 200
    
    # Context shares response data with validation steps
    And the response should be a dictionary
    And the response should contain field "id"
    And the response field "id" should equal "1"
    
    # Create post data - stored in context
    Given I have post data:
      | field  | value                        |
      | userId | 1                            |
      | title  | Context Sharing Test         |
      | body   | Demonstrating context usage  |
    
    # Context shares post data with request step
    When I send a POST request to "/posts" with the post data
    Then the response status code should be 201
    
    # Context shares new response with validation
    And the response field "title" should equal "Context Sharing Test"

  @error_handling @validation @database
  Scenario: Error handling and validation in integrated workflow
    Given the database is connected and ready
    # Setup database
    And I have a test user with email "error.handling@example.com"
    When I query the database for user with email "error.handling@example.com"
    Then the user should exist in the database
    
    # Valid API call
    When I send a GET request to "/posts/1"
    Then the response status code should be 200
    And the response should be a dictionary
    
    # Invalid API call (non-existent resource)
    When I send a GET request to "/posts/99999"
    Then the response status code should be 404
    
    # Database should remain consistent
    When I query the database for user with email "error.handling@example.com"
    Then the user should exist in the database
    And the user should be active

  @performance @bulk @database
  Scenario: Bulk operations with database and API
    Given the database is connected and ready
    # Create multiple users in database
    And I have 5 test users
    When I query all users from the database
    Then the database should contain at least 5 users
    And each user should have a valid email
    
    # Perform multiple API calls
    When I send a GET request to "/posts"
    Then the response status code should be 200
    And the response should be a non-empty list
    And the response list should have at least 10 items
    
    When I send a GET request to "/users"
    Then the response status code should be 200
    And the response should be a non-empty list
    
    When I send a GET request to "/comments"
    Then the response status code should be 200
    And the response should be a non-empty list
    
    # Verify database state after bulk operations
    When I query all users from the database
    Then the database should contain at least 5 users
