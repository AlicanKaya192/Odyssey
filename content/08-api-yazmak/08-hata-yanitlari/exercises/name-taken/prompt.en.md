The `names` set holds taken names (`"ada"`).

**What to do:** `POST /signup` lower-cases the name.

- If the name is taken, `409` with a dictionary in `detail`:
  `{"code": "name_taken", "name": ...}`
- Otherwise add it, `201`, `{"name": ...}`

- `{"name": "Grace"}` → `201`, `{"name": "grace"}`
- `{"name": "ADA"}` → `409`, `{"detail": {"code": "name_taken", "name": "ada"}}`
- `{"name": "grace"}` → `409`
