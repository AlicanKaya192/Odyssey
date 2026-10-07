The `users` dictionary is ready.

**What to do:**

1. `GET /users/{user_id}`: return the user; if missing, `404`,
   `{"detail": "User not found"}`.
2. `DELETE /users/{user_id}`: delete, `204`; the same `404` if missing.

- `GET /users/1` → `{"name": "Ada"}`
- `GET /users/7` → `404`, `{"detail": "User not found"}`
- `DELETE /users/2` → `204`, a second time → `404`
