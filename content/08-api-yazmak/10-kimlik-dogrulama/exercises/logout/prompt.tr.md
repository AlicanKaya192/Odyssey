Giriş (`POST /token`), `current_user` ve `GET /me` hazır.

**Yapman gereken:** `POST /logout`: gelen jetonu `tokens`'tan sil, `204`
döndür. Sonra aynı jetonla `GET /me` → `401`.

- giriş → jeton; `GET /me` → `200`
- `POST /logout` (aynı jeton) → `204`
- `GET /me` (aynı jeton) → `401`
