**What to do:**

1. A `require_key` dependency: `401` (`"Invalid API key"`) unless the
   `X-Api-Key` header is `letmein`.
2. `GET /health` → `{"status": "ok"}`: open to everyone.
3. `GET /admin/stats` → `{"users": 42}` and `GET /admin/logs` →
   `["started", "ready"]`: both require the key with `dependencies=[...]`.

- `GET /admin/stats` (no header) → `401`
- `GET /admin/stats`, `X-Api-Key: letmein` → `{"users": 42}`
- `GET /health` → `200`
