import json
import os
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

CACHE = "books_raw.json"


def load_books(session):
    if os.path.exists(CACHE):
        with open(CACHE, encoding="utf-8") as handle:
            print("from cache")
            return json.load(handle)
    books = fetch_all(session)
    with open(CACHE, "w", encoding="utf-8") as handle:
        json.dump(books, handle, ensure_ascii=False)
    print("from api")
    return books


session = requests.Session()
for _ in range(2):
    books = load_books(session)
    print("books:", len(books))
