## The Python standard library

| Job | Code |
|---|---|
| Random key / token | `secrets.token_bytes(32)`, `secrets.token_hex(16)` |
| Hash | `hashlib.sha256(data).hexdigest()` |
| HMAC | `hmac.new(key, message, hashlib.sha256).digest()` |
| Safe comparison | `hmac.compare_digest(a, b)` |
| Key from a password | `hashlib.pbkdf2_hmac("sha256", password, salt, iterations, dklen=32)` |
| Memory-hard KDF | `hashlib.scrypt(password, salt=salt, n=2**14, r=8, p=1, dklen=32)` |
| Big power, inverse | `pow(a, e, n)`, `pow(a, -1, n)` |
| Bytes ↔ number | `int.from_bytes(b, "big")`, `n.to_bytes(length, "big")` |
| Bytes ↔ hex | `b.hex()`, `bytes.fromhex(text)` |

**Not** in the standard library: AES, ChaCha20, RSA, ECDH, Ed25519. These
are used from a well-tested cryptography library.

## The right choices

| Need | Choice |
|---|---|
| Encrypt data | AES-256-GCM or ChaCha20-Poly1305 (AEAD) |
| Message integrity (shared key) | HMAC-SHA256 |
| File hash | SHA-256 |
| Storing passwords / key from a password | Argon2id; otherwise scrypt or PBKDF2 (600,000+) |
| Many keys from one secret | HKDF, an `info` per purpose |
| Key exchange | X25519 (ephemeral, forward secrecy) |
| Signature | Ed25519; or ECDSA, RSA-PSS (2048+) |
| Connection | TLS 1.3, certificate verification on |

## Never

- `random` for a secret value.
- ECB; reusing a nonce with the same key; encryption without
  authentication.
- MD5 / SHA-1 for integrity; an unsalted, fast password hash.
- Unpadded RSA; RSA shorter than 2048 bits.
- Secrets built into code; `verify=False`.
- Writing your own cipher algorithm.
