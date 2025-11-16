@frontend @ui @smoke
Feature: User Authentication - Login
  As a user
  I want to log in to the application
  So that I can access my account and use the platform features

  Background:
    Given I am on the login page

  @authentication @critical
  Scenario: Successful login with valid credentials
    When I fill the login form with valid credentials
    And I click the login button
    Then I should be redirected to the dashboard
    And I should be authenticated

  @authentication @negative
  Scenario: Login with invalid credentials
    When I fill the login form with username "invalid_user@example.com" and password "wrong_password"
    And I click the login button
    Then I should see an error message
    And the login form should be visible

  @authentication @critical
  Scenario: Logout functionality
    Given I am logged in
    When I logout
    Then I should be redirected to the login page
    And the login form should be visible

  @authentication @validation
  Scenario: Login form validation with empty credentials
    When I click the login button
    Then the login form should be visible

  @authentication
  Scenario: Login with remember me option
    When I fill the login form with valid credentials
    And I check the remember me checkbox
    And I click the login button
    Then I should be redirected to the dashboard
    And I should be authenticated

  @authentication @negative
  Scenario Outline: Login with invalid credentials variations
    When I fill the login form with username "<username>" and password "<password>"
    And I click the login button
    Then I should see an error message
    And the login form should be visible

    Examples:
      | username                | password        |
      | invalid@example.com     | wrongpass123    |
      | test@test.com           | short           |
      |                         | password123     |
      | user@example.com        |                 |

  @authentication @security
  Scenario: Cannot access protected pages without authentication
    Given I am on the login page
    When I navigate to the "dashboard" page
    Then I should be redirected to the login page

  @authentication
  Scenario: Successful login redirects to dashboard
    When I perform login
    Then I should be redirected to the dashboard
    And the page URL should contain "/dashboard"
    And I should see the element "user-dropdown"
