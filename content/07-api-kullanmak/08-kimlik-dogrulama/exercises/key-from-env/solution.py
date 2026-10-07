import os

import requests

BASE = "http://api.odyssey.test"


def get_key():
    return os.environ.get("LIBRARY_KEY", "demo-key-123")


print("LIBRARY_KEY defined:", "LIBRARY_KEY" in os.environ)

r = requests.get(BASE + "/stats", headers={"X-API-Key": get_key()})
print("status:", r.status_code)
print("books:", r.json()["books"])
