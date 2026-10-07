docs = {
    "/weather": {"required": ["city"], "optional": ["units"]},
    "/forecast": {"required": ["city", "days"], "optional": []},
    "/cities": {"required": [], "optional": ["country"]},
}


def check(path, params):
    if path not in docs:
        return "404 unknown endpoint"
    rules = docs[path]
    for name in rules["required"]:
        if name not in params:
            return "missing: " + name
    allowed = rules["required"] + rules["optional"]
    for name in params:
        if name not in allowed:
            return "unknown: " + name
    return "ok"


requests_to_check = [
    ("/weather", ["city"]),
    ("/news", []),
    ("/forecast", ["city"]),
    ("/weather", ["city", "color"]),
    ("/cities", []),
]
for path, params in requests_to_check:
    print(path, params, "->", check(path, params))
