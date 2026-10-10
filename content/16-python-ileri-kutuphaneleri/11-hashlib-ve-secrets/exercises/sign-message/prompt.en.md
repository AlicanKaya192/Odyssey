Write two functions:

- `sign(key, message)`: return the SHA-256 signature made with `hmac.new` as
  hexadecimal text (`key` and `message` are strings; `encode()` both).
- `verify(key, message, tag)`: recompute the signature and compare it with
  `hmac.compare_digest`.

The starter code does not use the key: anyone can produce the same
"signature".

**Expected output:**

```
e3b44dc2cb859682
True False
```
