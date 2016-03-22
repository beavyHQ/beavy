
if __name__ == '__main__':
    import pip
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FILES = []

    def collect(fn):
        FILES.append("-r")
        FILES.append(fn)

    try:
        import yaml
    except ImportError:
        pip.main(["install", "PyYAML"])
        import yaml

    with open("config.yml") as reader:
        config = yaml.safe_load(reader)

    if os.environ.get("BEAVY_ENV", None):
        print("----- Adding basic requirements")
        collect(os.path.join(BASE_DIR, "beavy", "requirements", "base.txt"))

        if os.environ.get("BEAVY_ENV", None) == "PRODUCTION":
            print("----- Adding production requirements")
            collect(os.path.join(BASE_DIR, "beavy", "requirements",
                                 "production.txt"))
        elif os.environ.get("BEAVY_ENV", None) in ["TEST", "DEV", "DEBUG"]:
            print("----- Adding dev requirements")
            collect(os.path.join(BASE_DIR, "beavy", "requirements", "dev.txt"))
    else:
        print("----- Adding dev requirements")
        collect(os.path.join(BASE_DIR, "beavy", "requirements", "base.txt"))
        collect(os.path.join(BASE_DIR, "beavy", "requirements", "dev.txt"))

    for module in config["MODULES"]:
        filename = os.path.join(BASE_DIR,
                                "beavy_modules", module, "requirements.txt")
        if os.path.exists(filename):
            print("----- Adding Requirements for {}".format(module))
            collect(filename)

    exit(pip.main(["install"] + FILES))
