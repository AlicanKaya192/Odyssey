Ready-made loops for the four forms of pagination. They work on the practice
server; for another API, change the field names according to its
documentation.

## Page number

```python
items, page = [], 1
while True:
    body = requests.get(BASE + "/books", params={"page": page, "per_page": 20}).json()
    items.extend(body["data"])
    if page >= body["meta"]["pages"]:
        break
    page += 1
```

Without `pages`: `if not body["data"]: break`.

## Next link

```python
items, url = [], BASE + "/books"
while url:
    body = requests.get(url).json()
    items.extend(body["data"])
    nxt = body["links"]["next"]
    url = BASE + nxt if nxt else None
```

## Offset + limit

```python
items, offset = [], 0
while True:
    params = {"offset": offset, "limit": 20}
    body = requests.get(BASE + "/offset/books", params=params).json()
    items.extend(body["items"])
    offset += body["limit"]
    if offset >= body["total"]:
        break
```

## Cursor

```python
items, cursor = [], None
while True:
    params = {"cursor": cursor} if cursor else {}
    body = requests.get(BASE + "/cursor/books", params=params).json()
    items.extend(body["results"])
    cursor = body["next_cursor"]
    if cursor is None:
        break
```

## Which one when

| Form | Strength | Weakness |
|---|---|---|
| Page number | Easy; you can jump to any page | Records drift while the list changes |
| Next link | No arithmetic; the server tells you | You cannot jump straight to a page |
| Offset + limit | Close to the database, flexible | Very large offsets can be slow |
| Cursor | Consistent on a changing list | Hard to go back or skip ahead |

## A safety limit

```python
for page in range(1, 500):      # at most 499 pages
    ...
    if last_page:
        break
```

Using a bounded `for` instead of `while True` stops you from sending endless
requests if the stopping condition ever breaks.
