`users` sözlüğü hazır.

**Yapman gerekenler:**

1. `GET /users/{user_id}`: kullanıcıyı döndür; yoksa `404`,
   `{"detail": "User not found"}`.
2. `DELETE /users/{user_id}`: sil, `204`; yoksa aynı `404`.

- `GET /users/1` → `{"name": "Ada"}`
- `GET /users/7` → `404`, `{"detail": "User not found"}`
- `DELETE /users/2` → `204`, ikinci kez → `404`
