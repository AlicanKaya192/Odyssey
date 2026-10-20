def resolve(registry, name, alias):
    # Name, alias, version: None if any is missing.
    pass


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
