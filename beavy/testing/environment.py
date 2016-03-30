# import os
from behaving import environment as benv
from beavy.app import app
from .database import ensure_personas, mixer
from pprint import pprint

import logging
import json
import os


log = logging.Logger(__name__)

BEHAVE_DEBUG_ON_ERROR = not os.getenv("CI", False)
BEHAVE_ERROR_ON_BROWSER_WARNINGS = os.getenv("BEHAVE_ERROR_ON_BROWSER_WARNINGS", not BEHAVE_DEBUG_ON_ERROR)  # noqa


def before_all(context):
    context.default_browser = os.getenv("BEHAVE_DEFAULT_BROWSER", 'chrome')

    context.default_browser_size = (1280, 1024)
    port = "2992" if app.config.get("DEBUG", False) else "5000"
    default_url = "http://localhost:{}".format(port)
    context.base_url = os.getenv("BEHAVE_BASE_URL", default_url)

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

            if entry["level"] not in ["WARNING", "ERROR"]:
                continue

            try:
                msg = json.loads(entry["message"])["message"]
            except (ValueError, KeyError):
                pass
            else:
                # in chrome we can extract much more info!
                if msg["level"] in ["warn", "error"] and \
                   msg.get("source") == "console-api":
                    entry = dict(level=msg["level"],
                                 timestamp=entry["timestamp"],
                                 message=msg["text"])
                else:
                    continue

            has_warnings = True

            log.warning("Browser {level}: {timestamp}: {message}".format(
                        **entry))

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
