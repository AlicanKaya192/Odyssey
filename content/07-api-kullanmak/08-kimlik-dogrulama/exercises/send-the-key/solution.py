import requests

BASE = "http://api.odyssey.test"

r = requests.get(BASE + "/stats")
print("without key:", r.status_code)

r = requests.get(BASE + "/stats", headers={"X-API-Key": "demo-key-123"})
stats = r.json()
print("with key:", r.status_code)
print("books:", stats["books"])
print("newest:", stats["newest"])
