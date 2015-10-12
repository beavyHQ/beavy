# import os
from behaving import environment as benv
from splinter.browser import Browser

PERSONAS = {}

def before_all(context):

    # Unless we tell our test runner otherwise, set our default browser to PhantomJS
    # if context.config.get("browser"):
    #     context.browser = Browser(context.config.get("browser"))
    # else:

    # When we're running with PhantomJS we need to specify the window size.
    # This is a workaround for an issue where PhantomJS cannot find elements
    # by text - see: https://github.com/angular/protractor/issues/585
    context.default_browser = 'phantomjs'
    context.default_browser_size = (1280, 1024)


    # import mypackage
    # context.attachment_dir = os.path.join(os.path.dirname(mypackage.__file__), 'tests/data')
    # context.sms_path = os.path.join(os.path.dirname(mypackage.__file__), '../../var/sms/')
    # context.gcm_path = os.path.join(os.path.dirname(mypackage.__file__), '../../var/gcm/')
    # context.mail_path = os.path.join(os.path.dirname(mypackage.__file__), '../../var/mail/')
    benv.before_all(context)


def after_all(context):
    benv.after_all(context)


def before_feature(context, feature):
    benv.before_feature(context, feature)


def after_feature(context, feature):
    benv.after_feature(context, feature)


def before_scenario(context, scenario):
    benv.before_scenario(context, scenario)
    context.personas = PERSONAS

def after_scenario(context, scenario):
    benv.after_scenario(context, scenario)
