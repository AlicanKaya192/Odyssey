`/admin/stats` requires a secret key; you don't know the key.

**What to do:** two tests:

1. A request without a key returns `401`.
2. Turn `require_key` into "always passes" with `app.dependency_overrides`
   and `GET /admin/stats` → `200`, `{"books": 3}`. Clean up afterwards
   (`finally`).
