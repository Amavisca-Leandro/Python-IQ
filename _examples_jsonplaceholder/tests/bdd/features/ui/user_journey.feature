@frontend @ui @regression
Feature: User Journey Flows
  As a user
  I want to navigate through different sections of the application
  So that I can manage my profile and use application features

  Background:
    Given I am logged in

  @profile @smoke
  Scenario: Edit user profile information
    When I navigate to the "profile" page
    And I fill the "phone" field with "+5511988887777"
    And I fill the "bio" field with "Updated bio for automated testing"
    And I click the "Save" button
    Then I should see the element ".success-message"

  @profile
  Scenario: Edit profile and cancel changes
    When I navigate to the "profile" page
    And I fill the "bio" field with "This should not be saved"
    And I click the "Cancel" button
    Then the page URL should contain "/profile"

  @navigation @smoke
  Scenario: Navigate through main application sections
    When I navigate to the "profile" page
    Then the page URL should contain "/profile"
    When I navigate to the "dashboard" page
    Then I should see the dashboard
    And the page URL should contain "/dashboard"

  @profile
  Scenario: View profile information
    When I navigate to the "profile" page
    Then the page URL should contain "/profile"
    And I should see the element ".profile-container"

  @navigation
  Scenario: User dropdown menu interactions
    When I navigate to the "dashboard" page
    Then I should see the element ".user-dropdown"

  @navigation @regression
  Scenario Outline: Navigate to different pages from dashboard
    When I navigate to the "<page_name>" page
    Then the page URL should contain "/<page_url>"

    Examples:
      | page_name | page_url  |
      | profile   | profile   |
      | dashboard | dashboard |

  @profile @slow
  Scenario: Complete profile setup journey
    When I navigate to the "profile" page
    And I fill the "full_name" field with "Test User Complete"
    And I fill the "phone" field with "+5511999999999"
    And I fill the "bio" field with "Complete profile setup test"
    And I fill the "company" field with "Test Company"
    And I fill the "location" field with "São Paulo, Brazil"
    And I click the "Save" button
    Then I should see the element ".success-message"

  @navigation
  Scenario: Dashboard displays correctly after login
    Then I should be on the dashboard
    And I should be authenticated
    And the page URL should contain "/dashboard"

  @profile
  Scenario: Profile page displays user information
    When I navigate to the "profile" page
    Then the page URL should contain "/profile"
    And I should see the element ".profile-container"
