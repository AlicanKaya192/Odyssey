import csv
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


def to_row(book):
    author = book.get("author") or {}
    return {
        "id": book["id"],
        "title": book["title"],
        "author": author.get("name", ""),
        "country": author.get("country", ""),
        "year": int(book["year"]),
        "price": float(book["price"]),
        "tags": "|".join(book.get("tags", [])),
    }


rows = [to_row(book) for book in fetch_all(requests.Session())]

ids = [row["id"] for row in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
assert len(rows) == 23, "some pages are missing"

with open("books.csv", "w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

with open("books.csv", encoding="utf-8") as handle:
    lines = handle.read().splitlines()
for line in lines[:3]:
    print(line)
print("rows:", len(lines) - 1)
