import requests

BASE = "http://api.odyssey.test"

try:
    requests.get(BASE + "/slow", timeout=1)
except requests.Timeout:
    print("too slow: gave up after 1 second")

r = requests.get(BASE + "/slow", timeout=5)
print("status:", r.status_code)
print("ok:", r.json()["ok"])
