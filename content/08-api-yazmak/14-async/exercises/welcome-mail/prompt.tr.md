`send_welcome(email)` hazır: `outbox` listesine bir e-posta ekliyor.

**Yapman gerekenler:**

1. `POST /signup?email=...`: `send_welcome`'ı **arka plan işi** olarak
   ekle, `{"queued": true}` döndür.
2. `GET /outbox` → `outbox`.

- `POST /signup?email=ada@x.org` → `{"queued": true}`
- `GET /outbox` → `["Welcome, ada@x.org!"]`
