@smoke @backend @api
Feature: JSONPlaceholder Posts API
  As a QA engineer
  I want to test the Posts API endpoints
  So that I can ensure the API works correctly for post management operations

  Background:
    Given the API client is configured

  @crud @get
  Scenario: Get all posts
    When I send a GET request to "/posts"
    Then the response status code should be 200
    And the response should be a non-empty list
    And the response list should have at least 1 items
    And each post should have required fields:
      | userId |
      | id     |
      | title  |
      | body   |

  @crud @post
  Scenario: Create a new post
    Given I have post data:
      | field  | value                    |
      | userId | 1                        |
      | title  | Test Post from BDD       |
      | body   | This is a test post body |
    When I send a POST request to "/posts" with the post data
    Then the response status code should be 201
    And the response should be a dictionary
    And the response should contain field "id"
    And the response field "title" should equal "Test Post from BDD"
    And the response field "body" should equal "This is a test post body"
    And the response field "userId" should equal "1"

  @crud @get @validation
  Scenario Outline: Get post by ID
    When I send a GET request to "/posts/<post_id>"
    Then the response status code should be <status_code>
    
    Examples:
      | post_id | status_code |
      | 1       | 200         |
      | 50      | 200         |
      | 100     | 200         |

  @crud @get
  Scenario: Get specific post and validate structure
    When I send a GET request to "/posts/1"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "userId"
    And the response should contain field "id"
    And the response should contain field "title"
    And the response should contain field "body"
    And the response field "id" should equal "1"

  @crud @put
  Scenario: Update an existing post
    Given I have post data:
      | field  | value                      |
      | userId | 1                          |
      | id     | 1                          |
      | title  | Updated Post Title         |
      | body   | This post has been updated |
    When I send a PUT request to "/posts/1" with the post data
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "id"
    And the response field "title" should equal "Updated Post Title"
    And the response field "body" should equal "This post has been updated"

  @crud @delete
  Scenario: Delete a post
    When I send a DELETE request to "/posts/1"
    Then the response status code should be 200

  @filter @get
  Scenario: Get posts by user ID
    When I send a GET request to "/posts?userId=1"
    Then the response status code should be 200
    And the response should be a non-empty list
    And each post should have required fields:
      | userId |
      | id     |
      | title  |
      | body   |

  @validation @get
  Scenario Outline: Validate post fields for different posts
    When I send a GET request to "/posts/<post_id>"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response field "userId" should equal "<user_id>"
    And the response field "id" should equal "<post_id>"
    
    Examples:
      | post_id | user_id |
      | 1       | 1       |
      | 11      | 2       |
      | 21      | 3       |
      | 31      | 4       |
      | 41      | 5       |

  @crud @post @validation
  Scenario: Create post with all fields and validate response
    Given I have post data:
      | field  | value                                    |
      | userId | 5                                        |
      | title  | Complete Test Post                       |
      | body   | This post contains all required fields   |
    When I send a POST request to "/posts" with the post data
    Then the response status code should be 201
    And the response should be a dictionary
    And the response should contain field "id"
    And the response should contain field "userId"
    And the response should contain field "title"
    And the response should contain field "body"
    And the response field "userId" should equal "5"
    And the response field "title" should equal "Complete Test Post"

  @get @list
  Scenario: Verify posts list contains multiple items
    When I send a GET request to "/posts"
    Then the response status code should be 200
    And the response should be a list
    And the response list should have at least 10 items
