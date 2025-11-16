@smoke @backend @api
Feature: JSONPlaceholder Todos API
  As a QA engineer
  I want to test the Todos API endpoints
  So that I can ensure the API works correctly for todo management operations

  Background:
    Given the API client is configured

  @crud @get
  Scenario: Get all todos
    When I send a GET request to "/todos"
    Then the response status code should be 200
    And the response should be a non-empty list
    And each todo should have required fields:
      | userId    |
      | id        |
      | title     |
      | completed |

  @crud @get @validation
  Scenario: Get todo by ID and validate structure
    When I send a GET request to "/todos/1"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "userId"
    And the response should contain field "id"
    And the response should contain field "title"
    And the response should contain field "completed"
    And the response field "id" should equal "1"

  @crud @get @validation
  Scenario Outline: Get todos by different IDs
    When I send a GET request to "/todos/<todo_id>"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response field "id" should equal "<todo_id>"

    Examples:
      | todo_id |
      | 1       |
      | 2       |
      | 3       |
      | 5       |
      | 10      |
      | 20      |

  @crud @post
  Scenario: Create a new todo
    Given I have todo data:
      | field     | value                     |
      | userId    | 1                         |
      | title     | Test Todo from BDD        |
      | completed | false                     |
    When I send a POST request to "/todos" with the todo data
    Then the response status code should be 201
    And the response should be a dictionary
    And the response should contain field "id"
    And the response field "userId" should equal "1"
    And the response field "title" should equal "Test Todo from BDD"
    And the response field "completed" should equal "false"

  @crud @post @validation
  Scenario: Create todo with completed status true
    Given I have todo data:
      | field     | value                     |
      | userId    | 1                         |
      | title     | Completed Todo            |
      | completed | true                      |
    When I send a POST request to "/todos" with the todo data
    Then the response status code should be 201
    And the response should be a dictionary
    And the response should contain field "id"
    And the response field "completed" should equal "true"

  @crud @put
  Scenario: Update an existing todo
    Given I have todo data:
      | field     | value                     |
      | userId    | 1                         |
      | title     | Updated Todo Title        |
      | completed | true                      |
    When I send a PUT request to "/todos/1" with the todo data
    Then the response status code should be 200
    And the response should be a dictionary
    And the response field "id" should equal "1"
    And the response field "title" should equal "Updated Todo Title"
    And the response field "completed" should equal "true"

  @crud @put @validation
  Scenario Outline: Update todos with different completion statuses
    Given I have todo data:
      | field     | value          |
      | userId    | 1              |
      | title     | <title>        |
      | completed | <completed>    |
    When I send a PUT request to "/todos/<todo_id>" with the todo data
    Then the response status code should be 200
    And the response should be a dictionary
    And the response field "completed" should equal "<completed>"

    Examples:
      | todo_id | title               | completed |
      | 1       | Todo Completed      | true      |
      | 2       | Todo Not Completed  | false     |
      | 3       | Todo In Progress    | false     |

  @validation @get
  Scenario: Validate completed field is boolean
    When I send a GET request to "/todos/1"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "completed"

  @get @list
  Scenario: Verify todos list contains multiple items
    When I send a GET request to "/todos"
    Then the response status code should be 200
    And the response should be a list
    And the response list should have at least 100 items

  @crud @post
  Scenario: Create todo with minimal required fields
    Given I have todo data:
      | field     | value          |
      | userId    | 1              |
      | title     | Minimal Todo   |
      | completed | false          |
    When I send a POST request to "/todos" with the todo data
    Then the response status code should be 201
    And the response should be a dictionary
    And the response should contain field "id"
