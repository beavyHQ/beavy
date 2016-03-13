import os
import json


def save_translations(inpt, fn):
    with open(fn, 'w') as w:
        json.dump(inpt, w, indent=2, sort_keys=True)


def deep_map_translations_in(path, ignore={}):
    all_translations = {}
    for root, dirs, files in os.walk(path):
        for name in files:
            with open(os.path.join(root, name)) as f:
                for entry in json.load(f):
                    if entry["id"] in ignore:
                        continue
                    all_translations[entry["id"]] = entry["defaultMessage"]

    return all_translations


def deep_map_each(folder, suffix, ignore={}):
    fullpath = os.path.join("var", "react-intl-messages", folder)
    for package in os.listdir(fullpath):
        fullname = os.path.join(fullpath, package)
        target = os.path.join("var", "react-intl-messages",
                              "beavy-{}-{}.json".format(package, suffix))
        save_translations(deep_map_translations_in(fullname), target)


core = deep_map_translations_in("var/react-intl-messages/beavy/jsbeavy")

save_translations(core, "var/react-intl-messages/beavy-core.json")

deep_map_each("beavy_modules", "module", ignore=core)
deep_map_each("beavy_apps", "app", ignore=core)
