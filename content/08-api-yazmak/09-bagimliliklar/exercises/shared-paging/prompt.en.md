The `books` and `movies` lists are ready.

**What to do:**

1. A `paging` dependency: `limit` (1–5, default `2`), `offset` (0 or more,
   default `0`); it returns `{"limit": ..., "offset": ...}`.
2. `GET /books` and `GET /movies` both use `paging` and return a slice of
   their list. The rules are written **only** in `paging`.

- `GET /books` → `["Dune", "Emma"]`
- `GET /books?limit=2&offset=3` → `["Kindred", "Beloved"]`
- `GET /movies?offset=1` → `["Heat", "Up"]`
- `GET /movies?limit=9` → `422`
