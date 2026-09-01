def load_settings(path):
    values = {}
    try:
        with open(path, encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                key, value = line.split("=", 1)
                values[key] = value
    except FileNotFoundError:
        return {}
    return values


found = load_settings("settings.txt")
missing = load_settings("profile.txt")

print(found)
print(missing)
