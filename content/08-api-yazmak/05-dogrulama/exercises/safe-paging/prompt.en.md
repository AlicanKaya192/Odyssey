The `items` list is ready (8 items).

**What to do:** `GET /items` takes two query parameters and returns a slice
of the list:

- `limit`: 1–5, default `3`
- `offset`: 0 or more, default `0`

- `GET /items` → `["apple", "bread", "cheese"]`
- `GET /items?limit=2&offset=6` → `["grapes", "honey"]`
- `GET /items?limit=6` → `422`
- `GET /items?offset=-1` → `422`
