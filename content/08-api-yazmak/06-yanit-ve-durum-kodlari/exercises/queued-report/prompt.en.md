Small reports are made right away, big ones are queued.

**What to do:** `POST /reports`:

- `rows` at most 1000 → `200`, `{"rows": ..., "status": "done"}`
- `rows` over 1000 → append `rows` to the `jobs` list, `202`,
  `{"queued": true, "position": its place in the queue}`

- `{"rows": 50}` → `200`, `{"rows": 50, "status": "done"}`
- `{"rows": 5000}` → `202`, `{"queued": true, "position": 1}`
- `{"rows": 2000}` → `202`, `{"queued": true, "position": 2}`
- `{"rows": 0}` → `422`
