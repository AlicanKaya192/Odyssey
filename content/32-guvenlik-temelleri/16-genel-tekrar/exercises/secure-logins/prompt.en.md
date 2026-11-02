Combine the Password Storage and Authentication sections. `users` is
user → `{"salt": hex, "hash": hex}`, `attempts` are `[user, password]`
tries. `hash_password` is ready.

`run_logins(users, attempts, max_fail)` should return a list with one
result per attempt:

- `"unknown user"` if the user does not exist,
- `"locked"` if the account is locked,
- `"ok"` if the hash matches (with `hmac.compare_digest`), and that user's
  failure count is reset,
- `"bad password"` otherwise; after `max_fail` failures in a row the
  account is locked and every later attempt is `"locked"`.

**Expected output:**

```
ada bad password
ada ok
bora bad password
bora bad password
bora bad password
bora locked
zeynep unknown user
```
