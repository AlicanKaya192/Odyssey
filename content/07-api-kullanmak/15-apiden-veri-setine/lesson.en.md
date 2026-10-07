# From an API to a Dataset

Along the path you learnt the pieces one by one: the request, parameters,
identity, pagination, errors, rate limits, flattening a nested response. In
this section we put them all together and do the job a data scientist really
does: **turning an API into a dataset you can analyse.**

The goal: pull every book from the library and pour them into a tidy table
called `books.csv`, in a way that is reliable, can be run again and respects
the server.

## The steps of the pipeline

This kind of work is usually called a **data pipeline**: steps that run in
order, taking data from a source, cleaning it and writing it to a target.

<figure class="fig">
  <div class="flow">
    <span class="node">1. Fetch<br><small>pages, retry</small></span><span class="arrow">→</span>
    <span class="node">2. Store<br><small>raw JSON</small></span><span class="arrow">→</span>
    <span class="node">3. Flatten<br><small>rows, types</small></span><span class="arrow">→</span>
    <span class="node">4. Check<br><small>dupes, gaps</small></span><span class="arrow">→</span>
    <span class="node acc">5. Write<br><small>books.csv</small></span>
  </div>
  <figcaption>Each step is a separate function. Because the raw data is written to disk, you can try the later steps again and again without going back to the API.</figcaption>
</figure>

Making each step a separate function makes the job easier: when a step
breaks you know where, and changing one step does not touch the others.

## 1. Fetch: every page, with safe requests

All the habits from earlier sections are here:

```python
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
```

- A `timeout` on every request (Section 11).
- On `429` wait for `Retry-After` (Section 12); on connection problems retry
  after waiting.
- If a `4xx` comes, `raise_for_status()` stops: something needs fixing; do
  not skip it quietly.
- A big page (`per_page=20`): fewer requests (Section 10).
- One `Session`: headers once, the connection reused (Section 08).

## 2. Store: write the raw response to disk

After fetching the data, write it to a file **as it is** before processing
it. We can call this a **cache**:

```python
import json
import os

CACHE = "books_raw.json"

def load_books(session):
    if os.path.exists(CACHE):
        with open(CACHE, encoding="utf-8") as handle:
            return json.load(handle)
    books = fetch_all(session)
    with open(CACHE, "w", encoding="utf-8") as handle:
        json.dump(books, handle, ensure_ascii=False)
    return books
```

Why does this matter so much?

- **You can try the cleaning a hundred times** and go to the API once. When
  you find a bug in the flattening code, there is no need to fetch again.
- **You do not hit the rate limit.**
- **You can show what you got:** it is clear which data the analysis used.

When you want to refresh the cache, deleting the file is enough.

## 3. Flatten and fix the types

The recipe from Section 05:

```python
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

rows = [to_row(book) for book in books]
```

## 4. Check

A few simple questions before writing save you from analysing a broken
dataset:

```python
ids = [row["id"] for row in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
assert len(rows) == expected_total, "some pages are missing"
```

- **Are there duplicate records?** If the list changes while paging, the same
  record can come twice (Section 10).
- **Does the count match?** Is the number of records you collected the same
  as `meta.total`?
- **Are there empty or odd values?** A negative price, a year in the
  future...

`assert condition, message` stops the program with the message if the
condition is false. In a data pipeline, "quietly wrong results" is the worst
outcome; stopping is better.

## 5. Write

```python
import csv

with open("books.csv", "w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
```

The file now opens in Excel, loads into pandas with
`pd.read_csv("books.csv")`, and can be charted.

## Fetching only what is new: incremental updates

The next day you want to update the dataset. Instead of fetching everything
again, fetching only **what changed** is both quicker and politer. Many APIs
allow it: "give me what changed since this date". On the practice server:

```python
r = requests.get(BASE + "/changes", params={"since": "2024-03-05"})
print([(b["id"], b["updated"]) for b in r.json()["data"]])
# [(6, '2024-03-05'), (10, '2024-03-08'), (13, '2024-03-10'),
#  (20, '2024-03-12'), (23, '2024-03-14')]
```

You keep the dataset you have in a dictionary keyed by identifier and write
the incoming records over it: existing ones are updated, new ones added. You
save the last update date in a file and carry on from there on the next run.
This is called an **incremental** update.

## Being able to run it again

A good data pipeline **gives the same result when run twice**, and does not
force you to start over if it stops half-way:

- The cache and the last update date are in files.
- Writing rewrites the file from scratch (it does not append): a second run
  produces no duplicate rows.
- Errors are reported clearly; a half-written file does not look "done".

## Summary

- A data pipeline: **fetch → store → flatten → check → write**; each step a
  separate function.
- Every habit while fetching: `Session`, `timeout`, retries, `Retry-After`,
  big pages, `raise_for_status`.
- Write the raw response to a **cache**: try the cleaning again and again, go
  to the API once.
- Check before writing: duplicate identifiers, missing pages, odd values.
  Stop clearly with `assert`.
- Update **incrementally**: fetch only what changed and merge by identifier.
- Running the pipeline twice must give the same result.
