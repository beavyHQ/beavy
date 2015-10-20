from behave import when, given
from behaving.web.steps import *
from behaving.sms.steps import *
from behaving.mail.steps import *
from behaving.notifications.gcm.steps import *
from behaving.personas.steps import *


@when('I go to HOME')
def go_to_home(context):
    context.browser.visit('/')


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
            Then I should see an element with the css selector "{form}" within 5 seconds
            Then I should see an element with id "email"
            Then I should see an element with id "password"
        When I fill in "email" with "{email}"
        And I fill in "password" with "password"
        And I press "submit"
        Then I should not see an element with the css selector "{form}" within 5 seconds
    """.format(first_step=first_step,
               email=user.email,
               form=USER_LOGIN_FORM,
               password="password"))
