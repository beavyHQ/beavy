Feature: Submitting a story

    Background:
        Given a browser
        And "malcolm" as the persona
        And I am logged in

    @wip
    Scenario: Submit a URL Story
        When I go to HOME
        And I click the link to "/submit/"
          Then the browser's URL should be "/submit/"
          And I should see the form "submit_story_form"
        When I fill in "title" with "Beavy is awesome"
          And I fill in "url" with "http://beavy.xyz"
          And I click the submit button of form "submit_story_form"
        Then the form "submit_story_form" should be gone within 5 seconds
          And I should see "Beavy is awesome"
