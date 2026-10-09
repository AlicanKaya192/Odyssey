import os


def port_from_env(default=8000):
    value = os.environ.get("APP_PORT")
    if value is None or not value.isdigit():
        return default
    return int(value)

os.environ.pop("APP_PORT", None)
print(port_from_env())
os.environ["APP_PORT"] = "9090"
print(port_from_env(), type(port_from_env()).__name__)
os.environ["APP_PORT"] = "abc"
print(port_from_env())
