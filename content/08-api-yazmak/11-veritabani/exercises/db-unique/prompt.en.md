In the `users` table the `email` column is `UNIQUE`.

**What to do:**

1. `POST /users`: add it, `201`, `{"id": ..., "email": ..., "name": ...}`.
   If the email already exists, `409` (`"Email already registered"`).
2. `GET /users`: all of them, ordered by `id`.

- `{"email": "ada@x.org", "name": "Ada"}` → `201`, id `1`
- the same email, `{"name": "Ada L"}` → `409`
- `{"email": "alan@x.org", "name": "Alan"}` → `201`, id `3`
