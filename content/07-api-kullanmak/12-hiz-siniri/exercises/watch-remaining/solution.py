import time

import requests

BASE = "http://api.odyssey.test"

codes = []
for i in range(7):
    r = requests.get(BASE + "/limited", timeout=5)
    codes.append(r.status_code)
    if int(r.headers["X-RateLimit-Remaining"]) == 0:
        print("pause")
        time.sleep(1)

print(codes)
