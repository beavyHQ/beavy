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
    assert context.browser.is_element_present_by_css("form[name={}]".format(name)), u'Form {} not found'.format(name)


@then('I should see the form "{name}" within {timeout:d} seconds')
def should_see_form_with_timeout(context, name, timeout):
    assert context.browser.is_element_present_by_css("form[name={}]".format(name), wait_time=timeout), u'Form {} not found'.format(name)


@step(u'The form "{name}" should be gone')
def should_not_see_form(context, name, timeout):
    assert context.browser.is_element_not_present_by_css("form[name={}]".format(name)), u'Form {} was found'.format(name)


@step(u'The form "{name}" should be gone within {timeout:d} seconds')
def should_not_see_form_with_timeout(context, name, timeout):
    assert context.browser.is_element_not_present_by_css("form[name={}]".format(name), wait_time=timeout), u'Form {} was found'.format(name)

@given("I am logged in")
def do_login(context):
    assert context.persona
    user = context.persona
    USER_LOGIN_FORM = "form[name=login_user_form]"
    if hasattr(context, 'loginButton') and context.loginButton:
        first_step = 'Click {}"'.format(context.loginButton)
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
               form=USER_LOGIN_FORM,
               password="password"))
