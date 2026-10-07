**What to do:**

1. `UserIn` (`name`, `password`) and `UserOut` (`id`, `name`) models.
2. `POST /users`: store the record in the `users` dictionary **with its
   password**, return it with `201`; the answer must not contain the
   password.
3. `GET /users`: the list of all users, again without passwords.

- `POST /users`, `{"name": "Ada", "password": "s3cret"}` → `201`, `{"id": 1, "name": "Ada"}`
- `GET /users` → `[{"id": 1, "name": "Ada"}]`
