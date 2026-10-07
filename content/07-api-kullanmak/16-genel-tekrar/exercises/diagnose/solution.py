import requests

BASE = "http://api.odyssey.test"


def diagnose(path):
    try:
        r = requests.get(BASE + path, timeout=1)
    except requests.Timeout:
        return "too slow"
    code = r.status_code
    if 200 <= code < 300:
        return "ok"
    if code in (401, 403):
        return "need permission"
    if code == 404:
        return "not found"
    if code >= 500:
        return "server error"
    return "other"


paths = ["/books/1", "/books/0", "/stats", "/broken", "/slow", "/me"]
for path in paths:
    print(path, "->", diagnose(path))
