Login (`POST /token`), `current_user` and `GET /me` are ready.

**What to do:** `POST /logout`: remove the incoming token from `tokens` and
return `204`. After that, `GET /me` with the same token → `401`.

- log in → a token; `GET /me` → `200`
- `POST /logout` (the same token) → `204`
- `GET /me` (the same token) → `401`
