Feature: Text presence

    Background:
        Given a browser

    Scenario: Smoketest for Home Header
        When I go to HOME
        Then I should see "Login" within 5 seconds