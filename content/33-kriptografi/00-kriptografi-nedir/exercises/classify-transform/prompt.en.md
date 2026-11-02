`classify_transform(name)` should take the name of a transformation
and return its kind (case does not matter):

- `base64`, `hex`, `url` → `"encoding"`
- `md5`, `sha1`, `sha256`, `sha3-256` → `"hashing"`
- `aes`, `chacha20`, `rsa` → `"encryption"`
- anything else → `"unknown"

**Expected output:**

```
Base64 encoding
sha256 hashing
AES encryption
hex encoding
rot13 unknown
```
