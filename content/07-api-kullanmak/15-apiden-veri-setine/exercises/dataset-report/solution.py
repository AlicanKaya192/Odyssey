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


def fetch_all(session):
    books, page = [], 1
    while True:
        body = get_json(session, "/books", {"page": page, "per_page": 20})
        books.extend(body["data"])
        if page >= body["meta"]["pages"]:
            return books
        page += 1

by_country = {}
for book in fetch_all(requests.Session()):
    country = book["author"]["country"]
    if country not in by_country:
        by_country[country] = [0, 0.0]
    by_country[country][0] += 1
    by_country[country][1] += book["price"]

order = sorted(by_country, key=lambda c: (-by_country[c][0], c))
for country in order:
    count, total = by_country[country]
    print(country, count, "books, average", f"{total / count:.2f}")
