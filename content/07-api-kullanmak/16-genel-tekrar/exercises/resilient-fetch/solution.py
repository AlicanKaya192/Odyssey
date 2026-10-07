import time

import requests

BASE = "http://api.odyssey.test"


def get(path):
    for attempt in range(5):
        r = requests.get(BASE + path, timeout=5)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 1)))
            continue
        if r.status_code >= 500:
            time.sleep(1)
            continue
        return r
    return None


print("/flaky", get("/flaky").status_code)
for i in range(5):
    print("/limited", get("/limited").status_code)
