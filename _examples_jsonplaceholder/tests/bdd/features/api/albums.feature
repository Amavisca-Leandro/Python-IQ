@smoke @backend @api
Feature: JSONPlaceholder Albums API
  As a QA engineer
  I want to test the Albums API endpoints
  So that I can ensure the API works correctly for album management operations

  Background:
    Given the API client is configured

  @crud @get
  Scenario: Get all albums
    When I send a GET request to "/albums"
    Then the response status code should be 200
    And the response should be a non-empty list
    And each album should have required fields:
      | userId |
      | id     |
      | title  |

  @crud @get @validation
  Scenario: Get album by ID and validate structure
    When I send a GET request to "/albums/1"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "userId"
    And the response should contain field "id"
    And the response should contain field "title"
    And the response field "id" should equal "1"

  @crud @get @validation
  Scenario Outline: Get albums by different IDs
    When I send a GET request to "/albums/<album_id>"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response field "id" should equal "<album_id>"

    Examples:
      | album_id |
      | 1        |
      | 2        |
      | 3        |
      | 5        |
      | 10       |
      | 20       |
      | 50       |

  @validation @get
  Scenario: Validate album data types
    When I send a GET request to "/albums/1"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "userId"
    And the response should contain field "id"
    And the response should contain field "title"

  @get @list
  Scenario: Verify albums list contains multiple items
    When I send a GET request to "/albums"
    Then the response status code should be 200
    And the response should be a list
    And the response list should have at least 50 items

  @crud @get @validation
  Scenario Outline: Validate albums belong to correct users
    When I send a GET request to "/albums/<album_id>"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response field "userId" should equal "<user_id>"

    Examples:
      | album_id | user_id |
      | 1        | 1       |
      | 11       | 2       |
      | 21       | 3       |
      | 31       | 4       |
      | 41       | 5       |
