# flake8: noqa
from behave import *
from behaving.web.steps import *
from behaving.sms.steps import *
from behaving.mail.steps import *
from behaving.notifications.gcm.steps import *
from behaving.personas.steps import *


@when('I go to HOME')
def go_to_home(context):
    context.browser.visit(context.base_url + '/')


@then('I should see the form "{name}"')
def should_see_form(context, name):
    assert context.browser.is_element_present_by_css("form[name={}]".format(name)), 'Form {} not found'.format(name)


@then('I should see the form "{name}" within {timeout:d} seconds')
def should_see_form_with_timeout(context, name, timeout):
    assert context.browser.is_element_present_by_css("form[name={}]".format(name), wait_time=timeout), 'Form {} not found'.format(name)


@step('The form "{name}" should be gone')
def should_not_see_form(context, name, timeout):
    assert context.browser.is_element_not_present_by_css("form[name={}]".format(name)), 'Form {} was found'.format(name)


@step('I click the submit button')
def click_the_submit_button(context, name):
    el  = context.browser.driver.find_element_by_css_selector("button[type=submit]".format(name))
    assert el, "Submit button not found"
    assert el.is_enabled(), "Submit button is disabled"
    el.click()

@step('I click the submit button of form "{name}"')
def click_the_submit_button(context, name):
    el = context.browser.driver.find_element_by_css_selector("form[name={}] button[type=submit]".format(name))

    assert el, "Submit button not found"
    assert el.is_enabled(), "Submit button is disabled"
    el.click()


@step('The form "{name}" should be gone within {timeout:d} seconds')
def should_not_see_form_with_timeout(context, name, timeout):
    assert context.browser.is_element_not_present_by_css("form[name={}]".format(name), wait_time=timeout), 'Form {} was found'.format(name)

@given("I am logged in")
def do_login(context):
    assert context.persona
    user = context.persona
    if hasattr(context, 'loginButton') and context.loginButton:
        first_step = 'I click {}"'.format(context.loginButton)
    else:
        first_step = 'I visit "/login"'
    context.execute_steps("""
        When I delete the cookie "session"
        And {first_step}
            Then I should see the form "login_user_form" within 5 seconds
            And I should see an element with id "email"
            And I should see an element with id "password"
        When I fill in "email" with "{email}"
        And I fill in "password" with "password"
        And I press "submit"
        Then the form "login_user_form" should be gone within 5 seconds
    """.format(first_step=first_step,
               email=user.email,
               password="password"))
