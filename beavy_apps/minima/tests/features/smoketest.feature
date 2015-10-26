Feature: Text presence

    Background:
        Given a browser
        And "malcolm" as the persona
        And I am logged in

    Scenario: Smoketest for Home Header
        Then I should see "home" within 2 seconds
