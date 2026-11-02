## What is stored and what is not

| Method | What happens when it leaks? | Decision |
|---|---|---|
| Plain text | Every password is read | Never |
| Encrypted | If the key leaks too, all are opened | Not for passwords |
| Plain hash (SHA-256) | Same passwords are grouped, found with tables and speed | No |
| Salted hash | Tables stop working but guessing is still fast | Not enough |
| **Salted, slow hash** | Every password is tried separately and expensively | **Yes** |

## Terms

- **Salt:** a random value per user, stored next to the hash, not secret.
  `secrets.token_bytes(16)`.
- **Key stretching:** making the hash slow on purpose.
- **Iterations:** how many times PBKDF2 takes the hash; for
  PBKDF2-HMAC-SHA256 the current recommendation is 600,000.
- **Precomputed table / rainbow table:** a ready-made table from the
  hashes of common passwords to the passwords; salt makes it useless.
- **Pepper:** a secret value shared by all users and kept **not** in the
  database but somewhere separate (a settings file, a hardware security
  module). It only adds protection if the database alone leaks.

## Python

```python
import hashlib
import hmac
import secrets

salt = secrets.token_bytes(16)
key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000)
record = f"pbkdf2_sha256$600000${salt.hex()}${key.hex()}"
same = hmac.compare_digest(key, other_key)
```

## Verification steps

1. Split the record at the `$` signs: algorithm, iterations, salt, hash.
2. If the algorithm is not recognised or the record is broken, `False`
   (fail securely).
3. Compute again with the typed password, the same salt and the same
   iterations.
4. Compare with `hmac.compare_digest`.
5. If it is correct and the iteration count is old, save it again with the
   new count.
