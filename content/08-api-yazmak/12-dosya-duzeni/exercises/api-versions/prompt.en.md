`/books` returns a dictionary (`{"1": "Dune", ...}`). New clients want a
list, and old ones mustn't break.

**What to do:**

1. `routers/books_v2.py`: a router returning the same `books` data
   (`from routers.books import books`) as a list:
   `[{"id": 1, "title": "Dune"}, ...]`.
2. `main.py`: the old router with the `/v1` prefix, the new one with `/v2`.

- `GET /v1/books` → `{"1": "Dune", "2": "Emma"}`
- `GET /v2/books` → `[{"id": 1, "title": "Dune"}, {"id": 2, "title": "Emma"}]`
- `GET /v1/books/1` → `{"id": 1, "title": "Dune"}`
- `GET /books` → `404`
