import json

DEFAULTS = {"theme": "dark", "font_size": 12, "language": "en"}


def load_settings(path):
    settings = DEFAULTS.copy()
    try:
        with open(path, encoding="utf-8") as file:
            loaded = json.load(file)
    except FileNotFoundError:
        return settings
    except json.JSONDecodeError:
        return settings
    for key in loaded:
        settings[key] = loaded[key]
    return settings


for path in ["good.json", "missing.json", "broken.json"]:
    settings = load_settings(path)
    print(settings["theme"], settings["font_size"], settings["language"])
