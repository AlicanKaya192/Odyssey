import time

import requests

BASE = "http://api.odyssey.test"

for attempt in range(1, 6):
    r = requests.get(BASE + "/flaky", timeout=5)
    print("attempt", attempt, r.status_code)
    if r.status_code == 200:
        break
    time.sleep(1)

body = r.json()
print("report:", body["report"])
print("after attempt:", body["attempt"])
