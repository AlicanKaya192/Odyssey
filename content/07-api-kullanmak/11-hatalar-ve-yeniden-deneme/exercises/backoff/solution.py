import time

import requests

BASE = "http://api.odyssey.test"


def get_with_retry(url, attempts):
    delay = 0.5
    for attempt in range(attempts):
        try:
            r = requests.get(url, timeout=5)
            if r.status_code < 500:
                return r
        except (requests.Timeout, requests.ConnectionError):
            pass
        if attempt < attempts - 1:
            time.sleep(delay)
            delay *= 2
    return None


for path, attempts in [("/flaky", 4), ("/books/99", 4), ("/broken", 3)]:
    r = get_with_retry(BASE + path, attempts)
    print(path, "->", r.status_code if r is not None else "gave up")
