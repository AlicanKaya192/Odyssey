`pbkdf2_hex(password, salt_hex, iterations)` should derive a key with
PBKDF2-HMAC-SHA256 and return it as hexadecimal text:
`hashlib.pbkdf2_hmac("sha256", password_bytes, salt_bytes, iterations)`.

So that the exercise finishes quickly, the examples use 1000 iterations; in
real use 600,000.

**Expected output:**

```
67af6c9fbd0e983a5d9de908
64
```
