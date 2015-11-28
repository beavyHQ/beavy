from flask.ext.script import Command, Option
from flask.ext import migrate as ext_migrate

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def patched_migrate(fn):
    def wrapped(*args, **kwargs):
        paths = list(filter(lambda x: os.path.isdir(x),
                        map(lambda x: os.path.join(BASE_DIR, \
                                   'beavy_modules', x, "migrations"),
                            app.config.get("MODULES", []))))
        print("Adding module migrations:\n - {}".format("\n - ".join(paths)))
        app_migrations_path = os.path.join(BASE_DIR,
                                           'beavy_apps',
                                           app.config.get("APP"),
                                           'migrations')
        if os.path.isdir(app_migrations_path):
            paths.append(app_migrations_path)
            print('Adding App migration: \n - {}'.format(app_migrations_path))
        cfg = fn(*args, **kwargs)
        cfg.set_main_option('version_locations', "{} {}".format(os.path.join('migrations', 'versions'), " ".join(paths)))
        return cfg
    return wrapped


ext_migrate._get_config = patched_migrate(ext_migrate._get_config)

from beavy.app import app, manager


from behave.__main__ import main as behave_main
from behave.configuration import options as behave_options

def reformat_options(opts):
    res = []
    for args, kwargs in opts:
        if not args: continue
        if "config_help" in kwargs:
            del kwargs['config_help']
        res.append(Option(*args, **kwargs))
    return res

class Behave(Command):

    def get_options(self):
        return reformat_options(behave_options)

    def run(self, *args, **kwargs):
        frontend = os.environ.get("APP", app.config.get("APP", None))
        if not frontend:
            print("You need to configure the APP to be used!")
            exit(1)

        exit(behave_main(sys.argv[2:] + ['--no-capture', "beavy_apps/{}/tests/features".format(frontend)]))


manager.add_command("behave", Behave())

class PyTest(Command):
    def run(self):
        import pytest

        arguments = ["--cov-config", ".coveragerc", "--cov=beavy", "beavy"]

        for module in app.config.get("MODULES", []):
            arguments.append("--cov=beavy_modules/{}".format(module))
            arguments.append("beavy_modules/{}".format(module))

        arguments.append("--cov=beavy_apps/{}".format(app.config["APP"]))
        arguments.append("beavy_apps/{}".format(app.config["APP"]))

        exit(pytest.main(arguments))

manager.add_command("pytest", PyTest())


# Setup app
@manager.command
def create_app(name):
    """
    Setup beavy template and infrastructure for a new app
    given the @name.
    """
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    APP_DIR = os.path.join(ROOT_DIR, "beavy_apps", name)

    if os.path.exists(APP_DIR):
        print("{} directory already exists. Exiting.".format(name))
        exit(1)

    # minimal setup
    os.mkdir(APP_DIR)
    open(os.path.join(APP_DIR, "__init__.py"), 'w').close()

    # create minimal frontend
    os.mkdir(os.path.join(APP_DIR, "frontend"))

    with open(os.path.join(APP_DIR, "frontend", "application.jsx"), 'w') as jsx:
        jsx.write("""
import React from "react";
import { MainMenu } from "components/MainMenu";
import UserModal from "containers/UserModal";
import UserMenuWidget from "containers/UserMenuWidget";

import { getExtensions } from "config/extensions";

// This is your app entry point
export default class Application extends React.Component {
    render() {
        return <div>
                  <UserModal />
                  <MainMenu
                    logo='http://beavy.xyz/logos/logo.svg'
                    navigationTools={<UserMenuWidget />}
                  >
                    {getExtensions('MainMenuItem').map(x=>x.call(this))}
                  </MainMenu>
                  {this.props.children}
                </div>;
    }
}

""")

    # create testing infrastructure
    os.mkdir(os.path.join(APP_DIR, "tests"))

    with open(os.path.join(APP_DIR, "tests", "environment.py"), 'w') as env:
        env.write("from beavy.testing.environment import *\n")

    os.mkdir(os.path.join(APP_DIR, "tests", "steps"))

    with open(os.path.join(APP_DIR, "tests", "steps", "steps.py"), 'w') as stp:
        stp.write("from beavy.testing.steps import *\n")


    print("{} successfully created!".format(name))




if __name__ == '__main__':
    manager.run()
