# Dependencies

As an API grows, the same lines start getting copied from endpoint to
endpoint: paging parameters, "find the record or 404", a key check, opening
and closing a database connection. FastAPI has a tool for this: the
**dependency**. You attach a function written once to endpoints, saying
"run this first and give me its result".

## The first dependency: paging

Let `/books` and `/authors` both take `limit` and `offset`. Instead of
writing the rules twice:

```python
from typing import Annotated
from fastapi import Depends, FastAPI, Query

app = FastAPI()


def paging(limit: Annotated[int, Query(ge=1, le=50)] = 10,
           offset: Annotated[int, Query(ge=0)] = 0):
    return {"limit": limit, "offset": offset}


@app.get("/books")
def list_books(page: Annotated[dict, Depends(paging)]):
    items = list(books.values())
    return items[page["offset"]:page["offset"] + page["limit"]]


@app.get("/authors")
def list_authors(page: Annotated[dict, Depends(paging)]):
    return {"page": page}
```

- `paging` is an ordinary function. Its parameters are read like an
  endpoint's: here, from the query.
- `Depends(paging)`: "this parameter's value is whatever `paging` returns".
- The rules in `paging` apply to both endpoints.

```text
GET /books?limit=2      200 [{"title": "Dune"}, {"title": "Emma"}]
GET /books?limit=99     422 less_than_equal, loc ["query", "limit"]
GET /authors?offset=5   200 {"page": {"limit": 10, "offset": 5}}
```

`/docs` also shows `limit` and `offset` on both endpoints, with their
rules: a dependency's parameters count as the endpoint's parameters.

## A shortcut: naming the type

`Annotated[dict, Depends(paging)]` is long. You can name it once and use it
everywhere:

```python
Paging = Annotated[dict, Depends(paging)]


@app.get("/books")
def list_books(page: Paging):
    ...
```

<figure class="fig">
  <div class="flow">
    <span class="node">GET /books?limit=2</span><span class="arrow">→</span>
    <span class="node acc">paging()<br><small>limit, offset checked</small></span><span class="arrow">→</span>
    <span class="node">page = {"limit": 2, "offset": 0}</span><span class="arrow">→</span>
    <span class="node ok">list_books(page)</span>
  </div>
  <figcaption>FastAPI runs the dependency first and hands its result to the endpoint as a parameter. If the dependency raises an error, the endpoint never runs.</figcaption>
</figure>

## 404 if not found, as a dependency

The `find_book` helper from the CRUD section can be a dependency too:

```python
def get_book(book_id: int) -> dict:
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]


@app.get("/books/{book_id}")
def read_book(book: Annotated[dict, Depends(get_book)]):
    return book
```

`get_book`'s `book_id` parameter was filled from `{book_id}` in the address.
If the book is missing, the dependency raises `HTTPException` and the
endpoint **never runs**: `GET /books/9` → `404`. The endpoint itself can now
be written as "the book certainly exists".

## A dependency's dependency

A dependency can ask for another dependency; FastAPI resolves the chain by
itself. Even when the same dependency is requested in several places in one
request, it runs **once** and the result is shared. We measured: we asked
for a counter dependency both directly and from inside another dependency,
and the counter went up once (`{"a": 1, "b": 1, "calls": 1}`).

## A dependency without a result: a check

Sometimes you don't need the dependency's value; you only need it to
**run**. For example, a key check:

```python
from fastapi import Header


def require_key(x_key: Annotated[str | None, Header()] = None):
    if x_key != "secret":
        raise HTTPException(status_code=401, detail="Bad key")


@app.get("/admin", dependencies=[Depends(require_key)])
def admin():
    return {"ok": True}
```

- `Header()`: the value is read from a header. The parameter is called
  `x_key`, the header `X-Key` (underscore to hyphen, case doesn't matter).
- `dependencies=[...]` in the decorator: the function doesn't take it as a
  parameter, but the dependency runs.

```text
GET /admin                   401 {"detail": "Bad key"}
GET /admin  (X-Key: secret)  200 {"ok": true}
```

Authentication as a whole comes in the next section.

## Open and close: `yield`

Some resources must be opened before the request and closed after it: a
database connection, a file. A dependency using `yield` instead of
`return`:

```python
def get_session():
    session = open_session()       # before the request
    try:
        yield session              # the endpoint gets this
    finally:
        session.close()            # after the answer, even on an error
```

We measured: the part before `yield` ran before the endpoint, and the part
in `finally` ran **after** the answer was sent. Thanks to `try/finally` the
closing happens even when the endpoint fails. You'll use it with a real
SQLite connection in the database section.

## Swapping it in tests

Dependencies have one more benefit: in a test you can replace them with
another function.

```python
app.dependency_overrides[paging] = lambda: {"limit": 1, "offset": 0}
```

After this, `GET /books` returned one book (we measured). It's used to give
a fake database instead of the real one, or "always passes" instead of the
real key check; the Testing section has the details.

## Summary

- A dependency is an ordinary function; `Depends(function)` attaches it to a
  parameter.
- Its parameters (query, path, header) are read like an endpoint's and go
  into the docs.
- If it raises `HTTPException`, the endpoint doesn't run.
- If you don't need its result, `dependencies=[Depends(...)]`.
- A `yield` dependency: open first, close after the answer (`try/finally`).
- In one request the same dependency runs once; in tests it's swapped with
  `app.dependency_overrides`.
