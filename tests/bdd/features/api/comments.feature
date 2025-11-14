@smoke @backend @api
Feature: JSONPlaceholder Comments API
  As a QA engineer
  I want to test the Comments API endpoints
  So that I can ensure the API works correctly for comment management operations

  Background:
    Given the API client is configured

  @crud @get
  Scenario: Get all comments
    When I send a GET request to "/comments"
    Then the response status code should be 200
    And the response should be a non-empty list
    And each comment should have required fields:
      | postId |
      | id     |
      | name   |
      | email  |
      | body   |

  @crud @get @validation
  Scenario: Get comment by ID and validate structure
    When I send a GET request to "/comments/1"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "postId"
    And the response should contain field "id"
    And the response should contain field "name"
    And the response should contain field "email"
    And the response should contain field "body"
    And the response field "id" should equal "1"

  @crud @get @validation
  Scenario Outline: Get comments by different IDs
    When I send a GET request to "/comments/<comment_id>"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response field "id" should equal "<comment_id>"

    Examples:
      | comment_id |
      | 1          |
      | 2          |
      | 3          |
      | 5          |
      | 10         |

  @crud @post
  Scenario: Create a new comment
    Given I have comment data:
      | field  | value                        |
      | postId | 1                            |
      | name   | Test Comment from BDD        |
      | email  | testcomment@example.com      |
      | body   | This is a test comment body  |
    When I send a POST request to "/comments" with the comment data
    Then the response status code should be 201
    And the response should be a dictionary
    And the response should contain field "id"
    And the response field "postId" should equal "1"
    And the response field "name" should equal "Test Comment from BDD"
    And the response field "email" should equal "testcomment@example.com"
    And the response field "body" should equal "This is a test comment body"

  @crud @post @validation
  Scenario: Create comment with minimal data
    Given I have comment data:
      | field  | value                   |
      | postId | 1                       |
      | name   | Minimal Comment         |
      | email  | minimal@example.com     |
      | body   | Minimal body content    |
    When I send a POST request to "/comments" with the comment data
    Then the response status code should be 201
    And the response should be a dictionary
    And the response should contain field "id"

  @validation @get
  Scenario: Validate comment data types
    When I send a GET request to "/comments/1"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "postId"
    And the response should contain field "id"
    And the response should contain field "name"
    And the response should contain field "email"
    And the response should contain field "body"

  @get @list
  Scenario: Verify comments list contains multiple items
    When I send a GET request to "/comments"
    Then the response status code should be 200
    And the response should be a list
    And the response list should have at least 100 items
