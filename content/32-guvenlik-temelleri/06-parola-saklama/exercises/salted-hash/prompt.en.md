`salted_hash(password, salt_hex)` should return a salted SHA-256 hash:

- The salt comes as hexadecimal text; turn it into bytes with
  `bytes.fromhex(salt_hex)`.
- The hash is the SHA-256 of the bytes `salt + password`, as
  `hexdigest()`.

The starter code does not use the salt at all: it gives the same hash for
two different salts.

**Expected output:**

```
1a960a97b9446e0bdfb9
b0e2d6a339b1c7f7e619
```
