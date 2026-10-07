The `users` dictionary is ready: `ada` is an admin (`admin`), `alan` a
member (`member`).

**What to do:**

1. `get_user`: `401` (`"Unknown user"`) if the name in the `X-User` header
   isn't in `users`; otherwise `{"name": ..., "role": ...}`.
2. `require_admin`: **depends on `get_user`**; `403` (`"Admins only"`) if
   the role isn't `admin`; it returns the user.
3. `GET /me` → the user; `GET /admin` → `{"welcome": name}`.

- `GET /me`, `X-User: alan` → `{"name": "alan", "role": "member"}`
- `GET /admin`, `X-User: alan` → `403`
- `GET /admin`, `X-User: ada` → `{"welcome": "ada"}`
- `GET /admin` (no header) → `401`
