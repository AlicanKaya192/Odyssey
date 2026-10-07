import requests

BASE = "http://api.odyssey.test"

session = requests.Session()
session.headers.update({
    "Authorization": "Bearer letmein",
    "X-API-Key": "demo-key-123",
    "User-Agent": "library-cli/1.0",
})

for path in ["/me", "/stats", "/books/2"]:
    r = session.get(BASE + path)
    print(path, r.status_code)

print("user agent:", r.request.headers["User-Agent"])
