from behave import when
from behaving.web.steps import *
from behaving.sms.steps import *
from behaving.mail.steps import *
from behaving.notifications.gcm.steps import *
from behaving.personas.steps import *


@when('I go to HOME')
def go_to_home(context):
    context.browser.visit('http://localhost:5000/')