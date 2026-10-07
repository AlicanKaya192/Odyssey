record = {
    "id": 7,
    "title": "Emma",
    "author": {
        "name": "Austen",
        "address": {"city": "Bath", "country": "UK"},
    },
    "tags": ["classic", "novel"],
}


def flatten(obj, prefix=""):
    flat = {}
    for key, value in obj.items():
        name = prefix + key
        if isinstance(value, dict):
            flat.update(flatten(value, name + "_"))
        else:
            flat[name] = value
    return flat


for name, value in flatten(record).items():
    print(name, "=", value)
