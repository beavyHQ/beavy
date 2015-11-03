
if __name__ == '__main__':
    import pip
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def install(fn):
        pip.main(["install", "-r", fn])

    try:
        import yaml
    except ImportError:
        pip.main(["install", "PyYAML"])
        import yaml

    with open("config.yml") as reader:
        config = yaml.safe_load(reader)


    if os.environ.get("BEAVY_ENV", None):
        print("----- Install basic requirements")
        install(os.path.join(BASE_DIR, "beavy", "requirements", "base.txt"))
        if os.environ.get("BEAVY_ENV", None) in ["TEST", "DEV", "DEBUG"]:
            print("----- Install dev requirements")
            install(os.path.join(BASE_DIR, "beavy", "requirements", "dev.txt"))
    else:
        install(os.path.join(BASE_DIR, "beavy", "requirements", "base.txt"))
        install(os.path.join(BASE_DIR, "beavy", "requirements", "dev.txt"))

    for module in config["MODULES"]:
        filename = os.path.join(BASE_DIR, "beavy_modules", module, "requirements.txt")
        if os.path.exists(filename):
            print("----- Installing Requirements for {}".format(module))
            install(filename)
