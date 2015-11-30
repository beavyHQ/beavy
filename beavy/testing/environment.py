# import os
from behaving import environment as benv
from splinter.browser import Browser
from beavy.app import app
from .database import ensure_personas, mixer
from pprint import pprint

import os
import logging

log = logging.Logger(__name__)

BEHAVE_DEBUG_ON_ERROR = not os.getenv("CI", False)
BEHAVE_ERROR_ON_BROWSER_WARNINGS = False # os.getenv("BEHAVE_ERROR_ON_BROWSER_WARNINGS", not BEHAVE_DEBUG_ON_ERROR)

def before_all(context):

    # Unless we tell our test runner otherwise, set our default browser to PhantomJS
    # if context.config.get("browser"):
    #     context.browser = Browser(context.config.get("browser"))
    # else:

    # When we're running with PhantomJS we need to specify the window size.
    # This is a workaround for an issue where PhantomJS cannot find elements
    # by text - see: https://github.com/angular/protractor/issues/585
    context.default_browser = os.getenv("BEHAVE_DEFAULT_BROWSER", 'firefox')

    context.default_browser_size = (1280, 1024)
    context.base_url = os.getenv("BEHAVE_BASE_URL",  "http://localhost:{}".format(app.config.get("DEBUG", False) and "2992" or "5000"))


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

    if getattr(context, "browser", None):
        has_warnings = False
        for entry in context.browser.driver.get_log('browser'):
            if entry["level"] in ["WARNING", "ERROR"]:
                has_warnings = True
                log.warning("Browser {level}: {timestamp}: {message}".format(**entry))

        if BEHAVE_ERROR_ON_BROWSER_WARNINGS and has_warnings:
            print("Exciting – Browser Warnings/Errors!")
            exit(1)

    benv.after_scenario(context, scenario)


def after_step(context, step):
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        # -- ENTER DEBUGGER: Zoom in on failure location.
        # NOTE: Use IPython debugger, same for pdb (basic python debugger).
        try:
            import ipdb as pdb
        except ImportError:
            import pdb

        if getattr(context, "browser", None):
            pprint(context.browser.driver.get_log('browser')[-10:])
            print("Current Screen: {}".format(context.browser.screenshot()))

        pdb.post_mortem(step.exc_traceback)
