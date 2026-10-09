# Query Parameters

In the Using APIs module you used **query parameters**, added after a `?` at the end of the
address, to filter and page a list: `/books?page=2`, `/books?author=Austen`.
In `requests` they went with `params=`. Now you write the side that receives
them.

## Every parameter not in the path is a query

```python
@app.get("/books")
def list_books(page: int = 1):
    return {"page": page}
```

There is no `{page}` in the address; so FastAPI treats `page` as a **query
parameter** and takes the value from the `?page=...` part:

```text
GET /books           {"page": 1}    (not sent → the default)
GET /books?page=3    {"page": 3}
GET /books?page=x    422            (loc: ["query", "page"])
```

The rule is simple:

| In the function | What FastAPI understands |
|---|---|
| The address has `{name}` | A path parameter |
| It does not | A query parameter |

Type conversion and `422` are the same as for path parameters; the only
difference is the first item of `loc`: `query` instead of `path`.

## Required or optional?

If you **give** a default value the parameter is optional; if you **do not**,
it is required:

```python
@app.get("/search")
def search(q: str):          # no default → required
    return {"q": q}
```

```text
GET /search          422  type: missing, loc: ["query", "q"], msg: Field required
GET /search?q=dune   200  {"q": "dune"}
```

## "If not given, do not filter": `None`

Sometimes a filter is either given or not; if not, nothing is filtered. For
this, the default is `None` and the type `int | None`:

```python
@app.get("/books")
def list_books(year_from: int | None = None):
    if year_from is None:
        return books
    return [book for book in books if book["year"] >= year_from]
```

`int | None` means "either an integer or nothing". If `?year_from=1950`
comes, `1950`; if not, `None`.

## Pagination

In the Using APIs module you fetched data from an API page by page. The side that pages is
written like this:

```python
@app.get("/books")
def list_books(page: int = 1, per_page: int = 2):
    start = (page - 1) * per_page
    return {"page": page, "total": len(books), "items": books[start:start + per_page]}
```

<figure class="fig">
  <div class="flow">
    <span class="node ok">Page 1<br><small>[0:2] Dune, Emma</small></span>
    <span class="node">Page 2<br><small>[2:4] Ulysses, Kindred</small></span>
    <span class="node">Page 3<br><small>[4:6] Beloved</small></span>
  </div>
  <figcaption>With <code>per_page=2</code> five books split into three pages. For page <code>p</code> the slice starts at <code>(p - 1) * per_page</code>; the last page may be short.</figcaption>
</figure>

Measured with five books:

```text
GET /books                      page 1: Dune, Emma
GET /books?page=2               page 2: Ulysses, Kindred
GET /books?page=3&per_page=2    page 3: Beloved
```

`total` lets the client work out how many pages there are; in the Using APIs module you
looked at exactly this to know the last page.

## Other types

```python
@app.get("/flag")
def flag(available: bool = False):
    return available
```

`?available=true` (or `1`, `yes`, `on`) → `true`; if not sent, `false`.

For a list where the same name is sent several times (`?tag=a&tag=b`) you
need `Query`:

```python
from fastapi import FastAPI, Query


@app.get("/tags")
def tags(tag: list[str] = Query(default=[])):
    return tag
```

`GET /tags?tag=a&tag=b` → `["a", "b"]`. Without `Query`, FastAPI takes the
list for a body.

## An unknown parameter

`GET /books?unknown=1` gives no error: FastAPI **ignores** query parameters
it does not know (measured). A typo (`?pgae=2`) silently falls back to the
default; the client may wonder "why always the first page?". That is why
your docs (`/docs`) matter: that is where people see which parameters exist.

## Path and query together

```python
@app.get("/authors/{author}/books")
def author_books(author: str, year_from: int | None = None):
    ...
```

`GET /authors/Austen/books?year_from=1810`: `author` from the path,
`year_from` from the query. The address decides which comes from where.

## Summary

- A parameter that is not in the address is read from the query
  (`?name=value`).
- No default: required (`422 missing`); a default: optional.
- For "do not filter if not given", `int | None = None`.
- Pagination: `start = (page - 1) * per_page`, slice
  `[start:start + per_page]`, with `total` next to it.
- `Query(default=[])` for a list; unknown parameters are ignored.
