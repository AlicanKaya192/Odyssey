`verify_password(password, record)` should say whether the typed
password matches the record. It must fail securely: if the record is
broken, do not raise an error, return `False`.

- Split by `$`, the record must have exactly **4** parts, the first being
  `"pbkdf2_sha256"`.
- The iteration count must consist of digits (`isdigit`).
- The salt must be valid hex: `bytes.fromhex` raises `ValueError` if it is
  not.
- Compute the hash again and compare with `hmac.compare_digest`.

The starter code is the version from the lesson: it crashes on a broken
record.

**Expected output:**

```
True
False
False
False
```
