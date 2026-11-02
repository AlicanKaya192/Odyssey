`pbkdf2_hex` is ready. `make_record(password, salt_hex, iterations)`
should return a single text in this format; the parts are separated by `$`
signs:

`pbkdf2_sha256` · iteration count · salt (hex) · hash (hex)

For example `pbkdf2_sha256$1000$8f2a...$1c0e...`.

**Expected output:**

```
pbkdf2_sha256
1000
8f2a1c9e5b7d3f60a4c2e8b1d6f09a37
67af6c9fbd0e983a5d9de90813f30d2fd211
```
