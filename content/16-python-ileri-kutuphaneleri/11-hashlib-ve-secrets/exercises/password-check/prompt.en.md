Write two functions:

- `hash_password(password, salt_hex)`: turn `salt_hex` into bytes with
  `bytes.fromhex`, take the digest with `hashlib.pbkdf2_hmac("sha256", ...)`
  with **100,000** iterations and return hexadecimal text.
- `check_password(password, salt_hex, key_hex)`: recompute with the same salt
  and compare with `hmac.compare_digest`.

**Expected output:**

```
ed2bacebbe4b33a2 64
True False
```
