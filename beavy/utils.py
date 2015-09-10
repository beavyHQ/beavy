import importlib

def load_modules(app):
    for modl in app.config.get("MODULES", []):
        subm = importlib.import_module("beavy_modules.{}".format(modl))
        if hasattr(subm, "init_app"):
            print(subm, subm.init_app)
            subm.init_app(app)
