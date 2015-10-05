import os
from flask.ext import migrate as ext_migrate

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


if __name__ == '__main__':
    manager.run()
