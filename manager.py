import os
from flask.ext import migrate as ext_migrate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def patched_migrate(fn):
    def wrapped(*args, **kwargs):
        paths = list(filter(lambda x: os.path.isdir(x),
                        map(lambda x: os.path.join(BASE_DIR, \
                                   'beavy_modules', x, "migrations"),
                            app.config.get("MODULES", []))))
        print("Adding plugin migrations:\n - {}".format("\n - ".join(paths)))
        cfg = fn(*args, **kwargs)
        cfg.set_main_option('version_locations', "{} {}".format(os.path.join('migrations', 'versions'), " ".join(paths)))
        return cfg
    return wrapped


ext_migrate._get_config = patched_migrate(ext_migrate._get_config)

from beavy.app import app, manager


if __name__ == '__main__':
    manager.run()
