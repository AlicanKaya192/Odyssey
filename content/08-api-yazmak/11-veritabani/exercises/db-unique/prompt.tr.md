`users` tablosunda `email` sütunu `UNIQUE`.

**Yapman gerekenler:**

1. `POST /users`: ekle, `201`, `{"id": ..., "email": ..., "name": ...}`.
   E-posta zaten varsa `409` (`"Email already registered"`).
2. `GET /users`: hepsi, `id` sırasıyla.

- `{"email": "ada@x.org", "name": "Ada"}` → `201`, id `1`
- aynı e-posta, `{"name": "Ada L"}` → `409`
- `{"email": "alan@x.org", "name": "Alan"}` → `201`, id `3`
