All the patterns for writing query parameters in one table.

| Request | In the function | If not sent |
|---|---|---|
| `?q=dune` (required) | `q: str` | `422 missing` |
| `?page=2` | `page: int = 1` | `1` |
| <code>?year_from=1950</code> (a filter) | <code>year_from: int &#124; None = None</code> | <code>None</code> → no filter |
| `?available=true` | `available: bool = False` | `false` |
| `?tag=a&tag=b` | `tag: list[str] = Query(default=[])` | `[]` |
| <code>/authors/Austen/books?year_from=1810</code> | <code>author: str, year_from: int &#124; None = None</code> | — |

## The filter pattern

```python
@app.get("/books")
def list_books(author: str | None = None, year_from: int | None = None):
    found = books
    if author is not None:
        found = [b for b in found if b["author"] == author]
    if year_from is not None:
        found = [b for b in found if b["year"] >= year_from]
    return found
```

Each filter narrows the result of the previous one; the ones not given are
skipped.

## The pagination pattern

```python
@app.get("/books")
def list_books(page: int = 1, per_page: int = 10):
    start = (page - 1) * per_page
    items = books[start:start + per_page]
    return {"page": page, "per_page": per_page, "total": len(books), "items": items}
```

- Pages start at 1 (that is how people count); 1 is subtracted for the
  slice.
- A page past the end of the list is not an error, just empty `items`.
- Without `total`, the client only finds the last page when an empty page
  comes.
- Filter first, then count and slice: `total` is the length of the
  filtered list.

## Common mistakes

| Symptom | Cause |
|---|---|
| Always the default value | The client spells the name differently (`?pgae=2`); unknown ones are ignored |
| `422 missing` in an unexpected place | The default was forgotten; the parameter became required |
| A list parameter asks for a body | `Query(default=[])` is not written |
| The filter never works | `if year_from:` was written; `0` also counts as "none" → `is not None` |
