def require_secrets(env, names):
    return [name for name in names if name not in env]

ENV = {"DB_HOST": "db.internal", "DB_PASSWORD": "x9!", "API_TOKEN": ""}
print(require_secrets(ENV, ["DB_PASSWORD", "API_TOKEN", "SIGNING_KEY"]))
print(require_secrets(ENV, ["DB_PASSWORD"]))
