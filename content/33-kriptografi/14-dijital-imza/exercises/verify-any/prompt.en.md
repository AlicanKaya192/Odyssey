`digest` is ready. `keys` is a list of trusted public keys `[e, n]`.
`verify_any(message, signature, keys)` should return the index of the
**first** key that verifies the signature; if none does, `-1`. The starter
code only tries the first key.

**Expected output:**

```
1
0
-1
```
