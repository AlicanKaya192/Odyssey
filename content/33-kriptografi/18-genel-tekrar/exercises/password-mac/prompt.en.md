**HMAC + key derivation.** `verify_with_password(password, salt_hex,
iterations, message, tag_hex)` should verify the message's tag. The MAC key
is derived from the password with PBKDF2-SHA256 (`salt`, `iterations`,
`dklen=32`); the tag is HMAC-SHA256 (`hexdigest()`), compared with
`hmac.compare_digest`. The starter code uses the password's bytes directly
as the key.

**Expected output:**

```
True
False
False
```
