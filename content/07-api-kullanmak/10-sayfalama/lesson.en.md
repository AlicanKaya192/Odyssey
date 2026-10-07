# Pagination

The library has 23 books, but `GET /books` returns only 5 of them. That is not
a mistake: most APIs send long lists split into **pages**, the way a search
engine shows results ten at a time.

Why? A list may hold millions of records. Sending them all in one response
tires the server, makes the response take minutes and fills memory.
Pagination splits that load into small, regular pieces. Your job is to ask
for all the pages you need, one after another.

## Inside a page

```python
import requests

BASE = "http://api.odyssey.test"
body = requests.get(BASE + "/books").json()
print(body["meta"])
# {'page': 1, 'per_page': 5, 'total': 23, 'pages': 5}
print(body["links"])
# {'next': '/books?page=2', 'prev': None}
```

The envelope (Section 05) now takes on its full meaning:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>data</code></span><span>The records on this page (at most <code>per_page</code>)</span></div>
    <div class="anat-row"><span><code>meta.page</code></span><span>The current page: <code>1</code></span></div>
    <div class="anat-row"><span><code>meta.per_page</code></span><span>Records per page: <code>5</code></span></div>
    <div class="anat-row"><span><code>meta.total</code></span><span>All records: <code>23</code></span></div>
    <div class="anat-row"><span><code>meta.pages</code></span><span>The number of pages: <code>5</code> (23 ÷ 5, rounded up)</span></div>
    <div class="anat-row"><span><code>links.next</code></span><span>The next page's address; <code>None</code> on the last page</span></div>
  </div>
  <figcaption>Every page carries the data as well as "where you are and where you can go".</figcaption>
</figure>

- `page`: the current page; `per_page`: records per page.
- `total`: the number of all records; `pages`: how many pages there are.
- `links.next`: the address of the next page; `None` when you are on the last
  page.

## Four forms of pagination

APIs paginate in four common forms. The idea is the same in all of them:
send "where did I stop?" with every request.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Page number</span><span><code>?page=2&amp;per_page=5</code>: "give me page 2"</span></div>
    <div class="anat-row"><span>Next link</span><span>Go to the <code>next</code> address in the response: "let the server say"</span></div>
    <div class="anat-row"><span>Offset + limit</span><span><code>?offset=10&amp;limit=10</code>: "skip 10 records, give me 10"</span></div>
    <div class="anat-row"><span>Cursor</span><span><code>?cursor=c4</code>: "carry on from where I stopped"</span></div>
  </div>
  <figcaption>The API chooses which one; the documentation says. The loop is the same in all four: ask, add, decide whether to go on or stop.</figcaption>
</figure>

## 1. By page number

The easiest: ask for `page=1`, `page=2`, ... up to `pages`.

```python
books = []
page = 1
while True:
    body = requests.get(BASE + "/books", params={"page": page}).json()
    books.extend(body["data"])
    if page >= body["meta"]["pages"]:
        break
    page += 1

print(len(books), page)   # 23 5
```

The `while True` + `break` pattern: since you do not know the number of pages
before the first response, the loop checks its own stopping condition inside.
`extend` adds the items of one list to the end of another (`append` would add
the list as a single item).

Ask for a page that does not exist and you get an empty list, not an error:

```python
print(requests.get(BASE + "/books", params={"page": 9}).json()["data"])   # []
```

That is why, with APIs that do not give `pages`, the loop stops **when an
empty page arrives**: `if not body["data"]: break`.

## 2. By the "next" link

If the API gives the address of the next page, following it is the safest
way: you do not compute page numbers, the server tells you.

```python
books = []
url = BASE + "/books?per_page=10"
while url:
    body = requests.get(url).json()
    books.extend(body["data"])
    nxt = body["links"]["next"]
    url = BASE + nxt if nxt else None

print(len(books))   # 23
```

`while url:` stops when the address becomes `None`. The server gives the
`next` link together with the filtering and sorting parameters
(`/books?per_page=10&page=2`); you do not lose them.

Some APIs give the link as a full address (`https://api.../books?page=2`),
others only as a path, as here. With a full address you do not add `BASE` in
front. Some send the links in a `Link` header rather than the body; requests
makes those readable through `r.links`.

## 3. By offset and limit

A form close to database language: "skip this many records, give me that
many".

```python
items = []
offset = 0
while True:
    params = {"offset": offset, "limit": 10}
    body = requests.get(BASE + "/offset/books", params=params).json()
    items.extend(body["items"])
    offset += body["limit"]
    if offset >= body["total"]:
        break

print(len(items))   # 23
```

`offset=0` is the first 10 records, `offset=10` the next 10, `offset=20` the
last 3.

## 4. By cursor

In large lists that keep changing (like a social media feed) page numbers
drift: if a new record is added at the top while you ask for page 2, you see a
record twice. A **cursor** prevents this: the server gives an opaque marker
for "where you stopped", and you send it back.

```python
results = []
cursor = None
while True:
    params = {"cursor": cursor} if cursor else {}
    body = requests.get(BASE + "/cursor/books", params=params).json()
    results.extend(body["results"])
    cursor = body["next_cursor"]
    if cursor is None:
        break

print(len(results))   # 23
```

Do not try to interpret the cursor (even if it looks like `c4`); send it back
as it is. That is exactly what "opaque" means: its inside is not for you.

## How many records to ask for: `per_page`

```python
print(requests.get(BASE + "/books", params={"per_page": 100}).json()["meta"])
# {'page': 1, 'per_page': 20, 'total': 23, 'pages': 2}
```

You asked for 100 and got 20: the server has an **upper limit**. Almost every
API has such a limit and the documentation states it. A bigger page means
fewer requests, but you cannot go over the limit; always read the result from
`meta`.

## A good pagination loop

- **Have a stopping condition.** No `next`, an empty page, or `pages`
  reached. A loop with a wrong stopping condition sends requests for ever.
- **Add a safety limit.** So that an error cannot cause an endless loop: an
  upper bound such as `for page in range(1, 1000):`.
- **Do not ask for more than you need.** If you need the first 10 books, do
  not fetch all 23; stop once you have enough records.
- **Leave filtering to the server.** Paging with `author=Austen` means far
  fewer requests than fetching every page and filtering in Python.

## Summary

- APIs split long lists into pages; to get all of it you ask for the pages
  one after another.
- `meta` (page, page size, total, number of pages) and `links.next` say where
  you are.
- Four forms: **page number** (`page`), **next link** (`next`), **offset +
  limit** (`offset`, `limit`), **cursor** (`cursor`).
- The loop is built with `while True` + `break` or `while url:`; the stopping
  condition must be clear.
- `per_page` has an upper limit; read the actual count from `meta`.
- Do not interpret a cursor; send it back as it is.
