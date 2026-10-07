import requests

BASE = "http://api.odyssey.test"


def read_body(path):
    response = requests.get(BASE + path)
    content_type = response.headers.get("Content-Type", "")
    if content_type.startswith("application/json"):
        return response.json()
    return response.text


for path in ["/status", "/authors/2", "/authors"]:
    body = read_body(path)
    kind = type(body).__name__
    if isinstance(body, dict) and "data" in body:
        body = str(len(body["data"])) + " authors"
    print(path, kind, body)
