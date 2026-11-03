`keystream` is ready. `items` is a list where each item is `[nonce_hex,
data_hex]`; all are encrypted with the same `key_hex`. `encrypt_all(key_hex,
items)` should return one result per item:

- `"nonce reused"` if the nonce was **already used in this call**,
- otherwise encrypt the data with the stream cipher, give the ciphertext as
  hex, and mark the nonce as used.

An item that repeats a nonce is not encrypted; we are preventing the
key-reuse mistake of the previous section.

**Expected output:**

```
65
14
nonce reused
```
