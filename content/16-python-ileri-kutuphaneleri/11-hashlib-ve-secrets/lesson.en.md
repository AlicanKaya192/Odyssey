# hashlib and secrets

You downloaded a file; how do you know it was not damaged on the way? How do
you store users' passwords so that they cannot be read even if the database
is stolen? How is the random code in a password reset link produced? The
answers to all three are in the standard library: **`hashlib`** (digests /
hashes), **`hmac`** (keyed signatures) and **`secrets`** (secure randomness).

## What is a digest (hash)?

```python
import hashlib

text = "hello"
digest = hashlib.sha256(text.encode()).hexdigest()
print(digest)
print(hashlib.sha256(b"hello.").hexdigest())
print(len(digest), len(hashlib.sha256(b"hello").digest()))
try:
    hashlib.sha256(text)
except TypeError as error:
    print("TypeError:", error)
```

```text
2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
1589999b0ca6ef8814283026a9f166d51c70a910671c3d44049755f07f2eb910
64 32
TypeError: Strings must be encoded before hashing
```

- A **hash function** turns data of any length into a fixed-length
  fingerprint. SHA-256's fingerprint is 32 bytes; `hexdigest()` gives it as
  64 hexadecimal characters, `digest()` gives the bytes themselves.
- **The same input always gives the same digest**; adding a single dot
  changes the whole digest. There is no way back from the digest to the input
  (one-way).
- `hashlib` wants **bytes**: text is first turned into bytes with `encode()`.

## A file's fingerprint

```python
import hashlib
from pathlib import Path

rows = "".join(f"{i},{i * 3}\n" for i in range(10_000))
path = Path("report.csv")
path.write_bytes(("id,total\n" + rows).encode())
with path.open("rb") as file:
    whole = hashlib.file_digest(file, "sha256").hexdigest()
h = hashlib.sha256()
with path.open("rb") as file:
    while True:
        chunk = file.read(65_536)
        if not chunk:
            break
        h.update(chunk)
print(whole[:16], h.hexdigest() == whole)
print(path.stat().st_size)
```

```text
63eb0f6a51b36fa9 True
105193
```

- **`hashlib.file_digest(file, "sha256")`** reads a file opened in binary
  mode piece by piece and computes its digest; however large the file, it is
  not loaded into memory at once.
- Doing the same by hand: open a hash object and feed it each piece with
  **`update`**. Feeding it in pieces gives the same digest as feeding it all
  at once.
- The "SHA-256" line on download pages is exactly for this: you compute the
  digest of the file you downloaded and compare it with that line; if even a
  single byte differs, the digests do not match.

## Storing passwords: salt and a slow hash

```python
import hashlib
import hmac
import secrets

print(hashlib.sha256(b"secret123").hexdigest()[:16])
print(hashlib.sha256(b"secret123").hexdigest()[:16])


def hash_password(password, salt=None):
    salt = salt or secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return salt, key


def check_password(password, salt, key):
    _, candidate = hash_password(password, salt)
    return hmac.compare_digest(candidate, key)


salt, key = hash_password("secret123")
print(len(salt), len(key))
right = check_password("secret123", salt, key)
wrong = check_password("Secret123", salt, key)
print(right, wrong)
other_salt, other_key = hash_password("secret123")
print(key == other_key)
```

```text
fcf730b6d95236ec
fcf730b6d95236ec
16 32
True False
False
```

- A password is **never** stored as plain text. Plain SHA-256 is not enough
  either: the same password always gives the same digest (the first two
  lines), so in a stolen table everyone using the same password shows up at
  once, and the digests of common passwords can be looked up in precomputed
  lists.
- **Salt**: 16 random bytes per user. The password is hashed together with
  the salt; the same password with a different salt gives a different digest
  (the last line is `False`). The salt is not secret; it is stored next to
  the digest.
- **`pbkdf2_hmac`** repeats the hash 200,000 times to be **slow** on purpose.
  A user logging in does not notice, but for an attacker trying millions of
  passwords every attempt becomes expensive. (`hashlib.scrypt` serves the
  same purpose and also spends memory.)
- To check, the digest is recomputed with the same salt and compared with
  **`hmac.compare_digest`**. `==` stops at the first differing byte; by
  measuring the time taken, one could guess how many bytes of the digest
  match. `compare_digest` always takes the same time.

## Signatures: hmac

```python
import hashlib
import hmac

KEY = b"server-side-secret"


def sign(message):
    return hmac.new(KEY, message.encode(), hashlib.sha256).hexdigest()


cookie = "user=ada;role=user"
tag = sign(cookie)
forged = "user=ada;role=admin"
print(hmac.compare_digest(tag, sign(cookie)))
print(hmac.compare_digest(tag, sign(forged)))
print(len(tag))
```

```text
True
False
64
```

- To prove a message **was not changed** and **came from us**, a plain digest
  is not enough: whoever changes the message can compute the new digest
  themselves.
- **HMAC** computes the digest together with a secret **key**. Someone who
  does not know the key cannot produce a valid signature for the message they
  changed (`role=admin`).
- Cookies, password reset links, messages between servers and webhooks are
  signed this way. "Checking that your own file was not changed" from the
  pickle section is this too: the file's bytes are signed with HMAC and the
  signature is checked before loading.

## secrets: unpredictable randomness

```python
import random
import secrets
import string

random.seed(7)
first = [random.randint(0, 9) for _ in range(6)]
random.seed(7)
print(first == [random.randint(0, 9) for _ in range(6)])
token = secrets.token_urlsafe(32)
print(len(token), secrets.token_hex(16).isalnum())
alphabet = string.ascii_letters + string.digits
password = "".join(secrets.choice(alphabet) for _ in range(16))
print(len(password), all(c in alphabet for c in password))
```

```text
True
43 True
16 True
```

- **`random`** is for simulations and games: it is produced from a seed, and
  the same seed gives the same sequence (the first line is `True`). Someone
  who sees a few outputs can predict the next ones; **it is not used for
  security**.
- **`secrets`** uses the operating system's secure source; it has no seed and
  cannot be reproduced.
  - `token_hex(16)`: 16 random bytes, 32 hexadecimal characters.
  - `token_urlsafe(32)`: 32 bytes in characters usable in a web address (43
    characters).
  - `choice(seq)`, `randbelow(n)`: secure picks and numbers.
- Password reset codes, session keys, API keys, salts: all are produced with
  `secrets`.

## Which algorithm?

| Algorithm | Use for | Not for |
|---|---|---|
| SHA-256, SHA-512, BLAKE2 | file integrity, fingerprints, HMAC | storing passwords (too fast) |
| `pbkdf2_hmac`, `scrypt` | storing passwords | file digests (slow on purpose) |
| MD5, SHA-1 | duplicate-file scans with no security need | security (collisions can be produced) |
| `hmac` | signatures, proving a message was not changed | hiding (it does not encrypt the message) |

A digest is **not encryption**: it cannot be reversed and hides nothing. To
hide data (and open it again later) you need an encryption library; the
standard library has none, and the `cryptography` package is used for this.

## Summary

- `hashlib.sha256(data).hexdigest()`; text first with `encode()`.
- A large file with `file_digest` or piece by piece with `update`.
- Passwords: a random salt + `pbkdf2_hmac` (or `scrypt`); check with
  `hmac.compare_digest`.
- Signatures: `hmac.new(key, message, hashlib.sha256)`.
- Every security-related random value with `secrets`; not `random`.
