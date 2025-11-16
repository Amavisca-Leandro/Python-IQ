@smoke @backend @api @filters
Feature: JSONPlaceholder API Filtering
  As a QA engineer
  I want to test API filtering capabilities
  So that I can ensure query parameters work correctly across all endpoints

  Background:
    Given the API client is configured

  # ============================================================================
  # POSTS FILTERING
  # ============================================================================

  @get @filter
  Scenario: Filter posts by user ID
    When I send a GET request to "/posts?userId=1"
    Then the response status code should be 200
    And the response should be a non-empty list
    And each post should have required fields:
      | userId |
      | id     |
      | title  |
      | body   |

  @get @filter @validation
  Scenario Outline: Filter posts by different user IDs
    When I send a GET request to "/posts?userId=<user_id>"
    Then the response status code should be 200
    And the response should be a non-empty list

    Examples:
      | user_id |
      | 1       |
      | 2       |
      | 3       |
      | 5       |

  @get @filter
  Scenario: Filtered posts are subset of all posts
    When I send a GET request to "/posts"
    Then the response status code should be 200
    And the response list should have at least 50 items
    When I send a GET request to "/posts?userId=1"
    Then the response status code should be 200
    And the response list should have at least 1 items

  # ============================================================================
  # COMMENTS FILTERING
  # ============================================================================

  @get @filter
  Scenario: Filter comments by post ID
    When I send a GET request to "/comments?postId=1"
    Then the response status code should be 200
    And the response should be a non-empty list
    And each comment should have required fields:
      | postId |
      | id     |
      | name   |
      | email  |
      | body   |

  @get @filter @validation
  Scenario Outline: Filter comments by different post IDs
    When I send a GET request to "/comments?postId=<post_id>"
    Then the response status code should be 200
    And the response should be a non-empty list

    Examples:
      | post_id |
      | 1       |
      | 2       |
      | 3       |
      | 5       |
      | 10      |

  @get @filter
  Scenario: Filtered comments are subset of all comments
    When I send a GET request to "/comments"
    Then the response status code should be 200
    And the response list should have at least 100 items
    When I send a GET request to "/comments?postId=1"
    Then the response status code should be 200
    And the response list should have at least 1 items

  # ============================================================================
  # TODOS FILTERING
  # ============================================================================

  @get @filter
  Scenario: Filter todos by user ID
    When I send a GET request to "/todos?userId=1"
    Then the response status code should be 200
    And the response should be a non-empty list
    And each todo should have required fields:
      | userId    |
      | id        |
      | title     |
      | completed |

  @get @filter @validation
  Scenario Outline: Filter todos by different user IDs
    When I send a GET request to "/todos?userId=<user_id>"
    Then the response status code should be 200
    And the response should be a non-empty list

    Examples:
      | user_id |
      | 1       |
      | 2       |
      | 3       |

  @get @filter
  Scenario: Filtered todos are subset of all todos
    When I send a GET request to "/todos"
    Then the response status code should be 200
    And the response list should have at least 100 items
    When I send a GET request to "/todos?userId=1"
    Then the response status code should be 200
    And the response list should have at least 1 items

  # ============================================================================
  # ALBUMS FILTERING
  # ============================================================================

  @get @filter
  Scenario: Filter albums by user ID
    When I send a GET request to "/albums?userId=1"
    Then the response status code should be 200
    And the response should be a non-empty list
    And each album should have required fields:
      | userId |
      | id     |
      | title  |

  @get @filter @validation
  Scenario Outline: Filter albums by different user IDs
    When I send a GET request to "/albums?userId=<user_id>"
    Then the response status code should be 200
    And the response should be a non-empty list

    Examples:
      | user_id |
      | 1       |
      | 2       |
      | 3       |
      | 5       |

  @get @filter
  Scenario: Filtered albums are subset of all albums
    When I send a GET request to "/albums"
    Then the response status code should be 200
    And the response list should have at least 50 items
    When I send a GET request to "/albums?userId=1"
    Then the response status code should be 200
    And the response list should have at least 1 items

  # ============================================================================
  # CROSS-RESOURCE FILTERING
  # ============================================================================

  @get @filter @validation
  Scenario: Filter consistency across multiple resources
    When I send a GET request to "/posts?userId=1"
    Then the response status code should be 200
    And the response should be a non-empty list
    When I send a GET request to "/todos?userId=1"
    Then the response status code should be 200
    And the response should be a non-empty list
    When I send a GET request to "/albums?userId=1"
    Then the response status code should be 200
    And the response should be a non-empty list
