import requests

BASE = "http://api.odyssey.test"


def access(key):
    r = requests.get(BASE + "/admin/report", headers={"X-API-Key": key})
    if r.status_code == 200:
        return "ok"
    if r.status_code == 401:
        return "unknown key"
    if r.status_code == 403:
        return "not allowed"
    return "unexpected " + str(r.status_code)


keys = ["admin-key-999", "demo-key-123", "my-guess"]
for key in keys:
    print(key, "->", access(key))
