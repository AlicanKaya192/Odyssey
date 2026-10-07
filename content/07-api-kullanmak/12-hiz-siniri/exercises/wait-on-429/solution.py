import time

import requests

BASE = "http://api.odyssey.test"

successful = 0
sent = 0
while successful < 6:
    r = requests.get(BASE + "/limited", timeout=5)
    sent += 1
    if r.status_code == 429:
        time.sleep(int(r.headers["Retry-After"]))
        print("waited")
        continue
    successful += 1

print("successful:", successful)
print("requests:", sent)
