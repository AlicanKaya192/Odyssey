import requests

BASE = "http://api.odyssey.test"

too_many = 0
for i in range(1, 6):
    r = requests.get(BASE + "/limited")
    print(i, r.status_code, "remaining", r.headers["X-RateLimit-Remaining"])
    if r.status_code == 429:
        too_many += 1
print("too many:", too_many)
