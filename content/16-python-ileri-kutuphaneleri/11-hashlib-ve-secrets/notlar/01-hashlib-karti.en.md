## hashlib

| Code | What it does |
|---|---|
| `hashlib.sha256(b"...").hexdigest()` | a 64-character digest |
| `.digest()` | a 32-byte digest |
| `h = hashlib.sha256(); h.update(piece)` | a digest piece by piece |
| `hashlib.file_digest(f, "sha256")` | a file's digest (`"rb"`) |
| `hashlib.pbkdf2_hmac("sha256", password, salt, 200_000)` | a password digest |
| `hashlib.scrypt(password, salt=salt, n=2**14, r=8, p=1)` | a password digest (also spends memory) |
| `hashlib.blake2b(data, digest_size=8)` | a fast digest with a chosen size |

## hmac

| Code | What it does |
|---|---|
| `hmac.new(key, message, hashlib.sha256).hexdigest()` | a signature |
| `hmac.compare_digest(a, b)` | a constant-time comparison |

## secrets

| Code | What it gives |
|---|---|
| `secrets.token_bytes(16)` | 16 random bytes (a salt) |
| `secrets.token_hex(16)` | 32 hexadecimal characters |
| `secrets.token_urlsafe(32)` | 43 URL-safe characters |
| `secrets.choice(seq)` | a secure pick |
| `secrets.randbelow(n)` | `0 … n-1` |

## Errors

| Error | Cause |
|---|---|
| `TypeError: Strings must be encoded before hashing` | the text was not `encode()`d |
| A password stored with `sha256` | too fast, no salt: the wrong tool |
| A code produced with `random` | predictable: use `secrets` |
| Digests compared with `==` | use `hmac.compare_digest` |
