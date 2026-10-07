`users` sözlüğü hazır: `ada` yönetici (`admin`), `alan` üye (`member`).

**Yapman gerekenler:**

1. `get_user`: `X-User` başlığındaki ad `users`'ta yoksa `401`
   (`"Unknown user"`); varsa `{"name": ..., "role": ...}`.
2. `require_admin`: **`get_user`'a bağımlı**; rol `admin` değilse `403`
   (`"Admins only"`); kullanıcıyı döndürsün.
3. `GET /me` → kullanıcı; `GET /admin` → `{"welcome": ad}`.

- `GET /me`, `X-User: alan` → `{"name": "alan", "role": "member"}`
- `GET /admin`, `X-User: alan` → `403`
- `GET /admin`, `X-User: ada` → `{"welcome": "ada"}`
- `GET /admin` (başlıksız) → `401`
