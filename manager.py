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

behave = Behave()
manager.add_command("behave", behave)

if __name__ == '__main__':
    manager.run()
