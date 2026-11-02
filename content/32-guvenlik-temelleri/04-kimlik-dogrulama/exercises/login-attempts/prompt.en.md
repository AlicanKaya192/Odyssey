The login attempts on an account are in the `events` list in order:
`"right"` (correct password) or `"wrong"` (wrong password).

`login_attempts(events, limit)` should return a list with one result per
attempt:

- correct password → `"ok"` and the count of wrong tries in a row goes
  back to zero,
- wrong password → `"fail"`; when the number of wrong tries in a row
  reaches `limit`, the account is **locked**,
- every attempt after locking, even with the correct password →
  `"locked"`.

**Expected output:**

```
fail ok fail fail fail locked locked
fail locked
```
