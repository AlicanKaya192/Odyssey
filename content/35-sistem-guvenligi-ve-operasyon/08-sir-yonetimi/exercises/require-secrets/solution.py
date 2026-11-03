def require_secrets(env, names):
    return sorted(name for name in names if not env.get(name))

ENV = {"DB_HOST": "db.internal", "DB_PASSWORD": "x9!", "API_TOKEN": ""}
print(require_secrets(ENV, ["DB_PASSWORD", "API_TOKEN", "SIGNING_KEY"]))
print(require_secrets(ENV, ["DB_PASSWORD"]))
