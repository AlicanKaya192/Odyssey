`pseudonym(value, key)` should first normalise the value with `strip()`
and `lower()` (the same email may be written differently), then hash it
with `hmac.new(key.encode(), value.encode(), hashlib.sha256)` and return
the **first 12 characters** of the hex digest.

**Expected output:**

```
5e979343af4e
5e979343af4e
cfa192be9cd7
```
