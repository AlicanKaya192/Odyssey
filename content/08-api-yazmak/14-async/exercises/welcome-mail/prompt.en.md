`send_welcome(email)` is ready: it adds an email to the `outbox` list.

**What to do:**

1. `POST /signup?email=...`: add `send_welcome` as a **background task** and
   return `{"queued": true}`.
2. `GET /outbox` → `outbox`.

- `POST /signup?email=ada@x.org` → `{"queued": true}`
- `GET /outbox` → `["Welcome, ada@x.org!"]`
