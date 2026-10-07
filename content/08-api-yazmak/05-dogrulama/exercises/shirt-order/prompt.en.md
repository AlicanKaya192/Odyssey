The `prices` dictionary is ready: `small` 10, `medium` 12, `large` 15.

**What to do:** an `Order` model and `POST /orders`.

- `size`: only `"small"`, `"medium"`, `"large"`
- `qty`: 1–10, default `1`
- Answer: `{"size": ..., "qty": ..., "total": price × qty}`

- `{"size": "large", "qty": 2}` → `{"size": "large", "qty": 2, "total": 30}`
- `{"size": "small"}` → `{"size": "small", "qty": 1, "total": 10}`
- `{"size": "huge"}` → `422`
- `{"size": "medium", "qty": 11}` → `422`
