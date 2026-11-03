`sign` is ready. `verify(secret, ts, now, body, signature)` should look
at time first: if `abs(now - ts) > 300`, `"expired"`. Then it recomputes
the signature itself and compares with `hmac.compare_digest`: if it does
not hold, `"bad signature"`, otherwise `"ok"`.

**Expected output:**

```
ok
bad signature
expired
```
