The `require_key` dependency is ready in `deps.py` (`X-Api-Key: letmein`).

**What to do:** make **every** endpoint of the router in `routers/admin.py`
require the key. Not on each endpoint separately, once on the router.

- `GET /admin/stats` (no key) → `401`
- `GET /admin/stats`, `X-Api-Key: letmein` → `{"books": 2}`
- `POST /admin/reset` (no key) → `401`
- `GET /books` keeps working without a key
