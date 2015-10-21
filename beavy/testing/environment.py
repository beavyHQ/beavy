# import os
from behaving import environment as benv
from splinter.browser import Browser
from beavy.app import app
from .database import ensure_personas, mixer

import os

BEHAVE_DEBUG_ON_ERROR = not os.getenv("CI", False)

def before_all(context):

    # Unless we tell our test runner otherwise, set our default browser to PhantomJS
    # if context.config.get("browser"):
    #     context.browser = Browser(context.config.get("browser"))
    # else:

    # When we're running with PhantomJS we need to specify the window size.
    # This is a workaround for an issue where PhantomJS cannot find elements
    # by text - see: https://github.com/angular/protractor/issues/585
    context.default_browser = os.getenv("BEHAVE_DEFAULT_BROWSER", 'phantomjs')

    context.default_browser_size = (1280, 1024)
    context.base_url = os.getenv("BEHAVE_BASE_URL", "http://localhost:5000")


    # import mypackage
    # context.attachment_dir = os.path.join(os.path.dirname(mypackage.__file__), 'tests/data')
    # context.sms_path = os.path.join(os.path.dirname(mypackage.__file__), '../../var/sms/')
    # context.gcm_path = os.path.join(os.path.dirname(mypackage.__file__), '../../var/gcm/')
    # context.mail_path = os.path.join(os.path.dirname(mypackage.__file__), '../../var/mail/')
    benv.before_all(context)

    mixer.init_app(app)


def after_all(context):
    benv.after_all(context)


def before_feature(context, feature):
    benv.before_feature(context, feature)


def after_feature(context, feature):
    benv.after_feature(context, feature)


def before_scenario(context, scenario):
    benv.before_scenario(context, scenario)
    context.personas = ensure_personas()

def after_scenario(context, scenario):
    benv.after_scenario(context, scenario)

def after_step(context, step):
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        # -- ENTER DEBUGGER: Zoom in on failure location.
        # NOTE: Use IPython debugger, same for pdb (basic python debugger).
        import ipdb
        ipdb.post_mortem(step.exc_traceback)
