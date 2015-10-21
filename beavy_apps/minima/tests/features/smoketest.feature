Feature: Text presence

    Background:
        Given a browser

    Scenario: Smoketest for Home Header
        Given "admin" as the persona
        And I am logged in
        Then I should see "home" within 2 seconds
