@smoke @backend @api
Feature: JSONPlaceholder Users API
  As a QA engineer
  I want to test the Users API endpoints
  So that I can ensure the API works correctly for user management operations

  Background:
    Given the API client is configured

  @crud @get
  Scenario: Get all users
    When I send a GET request to "/users"
    Then the response status code should be 200
    And the response should be a non-empty list
    And the response list should have at least 1 items
    And each user should have required fields:
      | id       |
      | name     |
      | username |
      | email    |

  @crud @get @validation
  Scenario Outline: Get user by ID
    When I send a GET request to "/users/<user_id>"
    Then the response status code should be <status_code>
    
    Examples:
      | user_id | status_code |
      | 1       | 200         |
      | 5       | 200         |
      | 10      | 200         |

  @crud @get
  Scenario: Get specific user and validate structure
    When I send a GET request to "/users/1"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "id"
    And the response should contain field "name"
    And the response should contain field "username"
    And the response should contain field "email"
    And the response should contain field "address"
    And the response should contain field "phone"
    And the response should contain field "website"
    And the response should contain field "company"
    And the response field "id" should equal "1"

  @crud @post
  Scenario: Create a new user
    Given I have user data:
      | field    | value                  |
      | name     | Test User from BDD     |
      | username | testuser               |
      | email    | testuser@example.com   |
    When I send a POST request to "/users" with the user data
    Then the response status code should be 201
    And the response should be a dictionary
    And the response should contain field "id"
    And the response field "name" should equal "Test User from BDD"
    And the response field "username" should equal "testuser"
    And the response field "email" should equal "testuser@example.com"

  @crud @put
  Scenario: Update an existing user
    Given I have user data:
      | field    | value                     |
      | id       | 1                         |
      | name     | Updated User Name         |
      | username | updateduser               |
      | email    | updated@example.com       |
    When I send a PUT request to "/users/1" with the user data
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "id"
    And the response field "name" should equal "Updated User Name"
    And the response field "username" should equal "updateduser"
    And the response field "email" should equal "updated@example.com"

  @crud @delete
  Scenario: Delete a user
    When I send a DELETE request to "/users/1"
    Then the response status code should be 200

  @validation @get
  Scenario Outline: Validate user fields for different users
    When I send a GET request to "/users/<user_id>"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response field "id" should equal "<user_id>"
    And the response field "name" should equal "<name>"
    
    Examples:
      | user_id | name              |
      | 1       | Leanne Graham     |
      | 2       | Ervin Howell      |
      | 3       | Clementine Bauch  |
      | 4       | Patricia Lebsack  |
      | 5       | Chelsey Dietrich  |

  @crud @post @validation
  Scenario: Create user with all required fields and validate response
    Given I have user data:
      | field    | value                                |
      | name     | Complete Test User                   |
      | username | completeuser                         |
      | email    | complete@example.com                 |
      | phone    | 1-555-123-4567                       |
      | website  | testuser.example                     |
    When I send a POST request to "/users" with the user data
    Then the response status code should be 201
    And the response should be a dictionary
    And the response should contain field "id"
    And the response should contain field "name"
    And the response should contain field "username"
    And the response should contain field "email"
    And the response field "name" should equal "Complete Test User"
    And the response field "username" should equal "completeuser"
    And the response field "email" should equal "complete@example.com"

  @get @list
  Scenario: Verify users list contains multiple items
    When I send a GET request to "/users"
    Then the response status code should be 200
    And the response should be a list
    And the response list should have at least 10 items

  @get @nested
  Scenario: Validate user address structure
    When I send a GET request to "/users/1"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "address"

  @get @nested
  Scenario: Validate user company structure
    When I send a GET request to "/users/1"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "company"

  @validation @get
  Scenario Outline: Validate multiple user IDs return success
    When I send a GET request to "/users/<user_id>"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "id"
    And the response should contain field "email"
    
    Examples:
      | user_id |
      | 1       |
      | 2       |
      | 3       |
      | 4       |
      | 5       |
      | 6       |
      | 7       |
      | 8       |
      | 9       |
      | 10      |

  @crud @put @validation
  Scenario Outline: Update different users with new data
    Given I have user data:
      | field    | value                |
      | id       | <user_id>            |
      | name     | Updated User <user_id> |
      | email    | user<user_id>@test.com |
    When I send a PUT request to "/users/<user_id>" with the user data
    Then the response status code should be 200
    And the response should be a dictionary
    And the response field "id" should equal "<user_id>"
    
    Examples:
      | user_id |
      | 1       |
      | 2       |
      | 3       |

  @get @filter
  Scenario: Get users and verify email format
    When I send a GET request to "/users"
    Then the response status code should be 200
    And the response should be a non-empty list
    And each user should have required fields:
      | email |

  @crud @post
  Scenario: Create user with minimal required fields
    Given I have user data:
      | field    | value              |
      | name     | Minimal User       |
      | username | minuser            |
      | email    | min@example.com    |
    When I send a POST request to "/users" with the user data
    Then the response status code should be 201
    And the response should be a dictionary
    And the response should contain field "id"
