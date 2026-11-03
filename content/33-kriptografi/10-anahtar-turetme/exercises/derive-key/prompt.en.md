`derive_key(password, salt_hex, iterations)` should derive a 32-byte key
from the password and return it as hex. The starter code passes the
password through a single SHA-256; the salt and the iteration count are
never used. Use `hashlib.pbkdf2_hmac("sha256", ..., salt, iterations,
dklen=32)` instead. The small iteration counts here are only examples; in
practice they are hundreds of thousands.

**Expected output:**

```
32 bytes
True
False
False
```
