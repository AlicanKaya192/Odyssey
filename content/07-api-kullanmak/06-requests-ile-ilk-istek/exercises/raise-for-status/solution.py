import requests

BASE = "http://api.odyssey.test"
paths = ["/books/5", "/books/0", "/authors/3", "/authors/42"]

for path in paths:
    response = requests.get(BASE + path)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        print("failed", path, response.status_code)
        continue
    body = response.json()
    print("ok", path, body.get("title", body.get("name")))
