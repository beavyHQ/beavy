import beavy.modules
import importlib

def load_modules(app):
    for modl in app.config.get("MODULES", []):
        subm = importlib.import_module("beavy.modules.{}".format(modl))
        # print(subm, subm.init_app)
        if hasattr(subm, "init_app"):
            subm.init_app(app)
