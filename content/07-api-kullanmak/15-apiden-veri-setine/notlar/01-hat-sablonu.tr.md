Kendi projelerine uyarlayabileceğin bir veri hattı iskeleti. Alan adlarını ve
uç noktaları kendi API'nin belgesine göre değiştir.

```python
import csv
import json
import os
import time

import requests

BASE = "http://api.odyssey.test"
CACHE = "books_raw.json"
OUTPUT = "books.csv"


def make_session():
    session = requests.Session()
    session.headers.update({"User-Agent": "my-pipeline/1.0"})
    return session


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
    items, page = [], 1
    while True:
        body = get_json(session, "/books", {"page": page, "per_page": 20})
        items.extend(body["data"])
        if page >= body["meta"]["pages"]:
            return items
        page += 1


def load(session):
    if os.path.exists(CACHE):
        with open(CACHE, encoding="utf-8") as handle:
            return json.load(handle)
    items = fetch_all(session)
    with open(CACHE, "w", encoding="utf-8") as handle:
        json.dump(items, handle, ensure_ascii=False)
    return items


def to_row(item):
    author = item.get("author") or {}
    return {"id": item["id"], "title": item["title"], "author": author.get("name", ""),
            "year": int(item["year"]), "price": float(item["price"])}


def check(rows):
    ids = [row["id"] for row in rows]
    assert len(ids) == len(set(ids)), "duplicate ids"
    assert all(row["price"] > 0 for row in rows), "non-positive price"


def write(rows):
    with open(OUTPUT, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = [to_row(item) for item in load(make_session())]
    check(rows)
    write(rows)
    print("wrote", len(rows), "rows to", OUTPUT)


main()
```

## Neyi nerede değiştirirsin

| Değişen | Yer |
|---|---|
| API adresi, kimlik | `BASE`, `make_session` |
| Uç nokta, sayfalama biçimi | `fetch_all` |
| Hangi sütunlar | `to_row` |
| Kurallar | `check` |
| Çıktı biçimi | `write` |
