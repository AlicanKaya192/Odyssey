The `users` dictionary holds not passwords but their **hashes** (salt
`SALT`).

**What to do:**

1. `hash_password(password, salt)`:
   `hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()`.
2. `POST /login` (`username`, `password`): if the incoming password's hash
   equals the stored one, `{"ok": true, "user": ...}`; otherwise, or if the
   user doesn't exist, `401`, `"Wrong username or password"`. Compare with
   `hmac.compare_digest`.

- `{"username": "ada", "password": "lovelace"}` → `{"ok": true, "user": "ada"}`
- `{"username": "ada", "password": "enigma"}` → `401`
- `{"username": "bob", "password": "x"}` → `401`, the same message
