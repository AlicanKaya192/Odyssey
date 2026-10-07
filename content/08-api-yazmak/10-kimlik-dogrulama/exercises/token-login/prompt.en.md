The password check (`check_password`) and `bearer = HTTPBearer()` are ready.

**What to do:**

1. `POST /token`: `401` (`"Wrong username or password"`) if the password
   doesn't match; otherwise make a token with `secrets.token_hex(16)`, save
   it in `tokens`, return `{"access_token": ..., "token_type": "bearer"}`.
2. A `current_user` dependency: `401` (`"Invalid token"`) if the token isn't
   in `tokens`, otherwise it returns the username.
3. `GET /me` → `{"user": ...}`.

- `POST /token` `{"username": "ada", "password": "lovelace"}` → a token
- `GET /me`, `Authorization: Bearer <token>` → `{"user": "ada"}`
- `GET /me`, `Authorization: Bearer xyz` → `401`
