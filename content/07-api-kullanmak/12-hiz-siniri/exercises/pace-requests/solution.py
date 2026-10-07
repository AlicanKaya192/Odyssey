import time

import requests

BASE = "http://api.odyssey.test"
GAP = 0.4

codes = []
for i in range(6):
    r = requests.get(BASE + "/limited", timeout=5)
    codes.append(r.status_code)
    time.sleep(GAP)

print(codes)
if 429 not in codes:
    print("no 429")
