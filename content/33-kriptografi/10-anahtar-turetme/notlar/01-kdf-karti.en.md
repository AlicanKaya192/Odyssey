## Three kinds of input

| Input | KDF | Slow? | Salt |
|---|---|---|---|
| A password | Argon2id, scrypt, PBKDF2 | **Yes**, deliberately | Random per person |
| A strong master secret | HKDF | No | Can be fixed per application |
| Neither, a new key | `secrets.token_bytes(32)` | — | — |

## PBKDF2

```text
hashlib.pbkdf2_hmac("sha256", password, salt, iterations, dklen=32)
```

- The salt is at least 16 bytes, from `secrets.token_bytes(16)`, separate
  for each record.
- Iteration count: hundreds of thousands with SHA-256 (example: 600,000);
  raised as hardware gets faster.
- Same password + salt + iterations → always the same key.

## scrypt

```text
hashlib.scrypt(password, salt=salt, n=2**14, r=8, p=1, dklen=32)
```

- `n`: cost (a power of 2), `r`: block size, `p`: parallelism.
- Memory is about `128 × r × n` bytes (16 MB with these settings).

## HKDF

1. **Extract:** `prk = HMAC(salt, secret)`.
2. **Expand:** `T(i) = HMAC(prk, T(i-1) + info + i)`, blocks are joined up
   to the requested length.
3. A different `info` for each purpose: `b"encryption"`, `b"mac"`,
   `b"v2-files"`.

## What to store

In a file encrypted with a key derived from a password, these stay in the
clear next to the encrypted data: **the KDF name, its parameters
(iterations, n, r, p), the salt**. The key itself is never written
anywhere; it is derived from the password again every time.
