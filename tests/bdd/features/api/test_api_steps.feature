@smoke @backend @api
Feature: API Steps Validation
  As a QA engineer
  I want to validate that API step definitions work correctly
  So that I can use them in BDD scenarios

  Background:
    Given the API client is configured

  Scenario: GET request with response validation
    When I send a GET request to "/posts/1"
    Then the response status code should be 200
    And the response should be a dictionary
    And the response should contain field "id"
    And the response should contain field "title"
    And the response field "id" should equal "1"

  Scenario: POST request with data preparation
    Given I have post data:
      | field  | value                    |
      | userId | 1                        |
      | title  | Test Post from BDD       |
      | body   | This is a test post body |
    When I send a POST request to "/posts" with the post data
    Then the response status code should be 201
    And the response should contain field "id"
    And the response field "title" should equal "Test Post from BDD"

  Scenario: GET list with validation
    When I send a GET request to "/posts"
    Then the response status code should be 200
    And the response should be a non-empty list
    And the response list should have at least 1 items
    And each post should have required fields:
      | userId |
      | id     |
      | title  |
      | body   |
