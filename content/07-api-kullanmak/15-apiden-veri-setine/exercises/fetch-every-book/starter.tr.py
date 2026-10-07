import time

import requests

BASE = "http://api.odyssey.test"


def get_json(session, path, params=None, attempts=3):
    for attempt in range(attempts):
        try:
            r = session.get(BASE + path, params=params, timeout=10)
            if r.status_code == 429:
                time.sleep(int(r.headers.get("Retry-After", 1)))
                continue
            r.raise_for_status()
            return r.json()
        except (requests.Timeout, requests.ConnectionError):
            time.sleep(2 ** attempt)
    raise RuntimeError("giving up on " + path)


# fetch_all(session): per_page=20 ile butun sayfalar


# session = requests.Session(); books = fetch_all(session)
# "books: 23", "first: ...", "last: ..."
