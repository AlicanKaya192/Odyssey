def resolve(registry, name, alias):
    if name not in registry:
        return None
    entry = registry[name]
    if alias not in entry["aliases"]:
        return None
    version = entry["aliases"][alias]
    for info in entry["versions"]:
        if info["version"] == version:
            return info["file"]
    return None


registry = {
    "churn": {
        "versions": [
            {"version": 1, "file": "models/churn-v1.pkl"},
            {"version": 2, "file": "models/churn-v2.pkl"},
        ],
        "aliases": {"production": 2, "staging": 1},
    }
}
print(resolve(registry, "churn", "production"))
print(resolve(registry, "churn", "staging"))
print(resolve(registry, "churn", "canary"))
print(resolve(registry, "fraud", "production"))
