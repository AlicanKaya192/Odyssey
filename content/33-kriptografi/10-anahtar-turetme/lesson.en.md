# Key Derivation

In the earlier sections the keys were always ready: fixed bytes such as
`b"enc-key-..."`. In a real program a key **comes** from somewhere: from the
user's password or from a single master secret the two sides share. A key
derivation function (**KDF**) turns that source into strong keys of the
right length.

## Why a password is not used as a key directly

A password differs from an encryption key in three ways:

- **Its length varies.** AES-256 needs exactly 32 bytes; `"sunflower"` is 9.
- **It is not random.** People pick predictable passwords; they come nowhere
  near the uncertainty of a 32-byte random key.
- **A fast hash is not enough.** `sha256(password)` fixes the length but can
  be computed millions of times a second; it is just as fast for someone
  trying to find the password by guessing.

In the Storing Passwords section we saw the same problem when storing
passwords: the answer was a **salted and deliberately slow** function.
Deriving a key from a password uses the same tools.

## PBKDF2: salt and iteration count

`hashlib.pbkdf2_hmac` passes the password together with a salt through
HMAC **thousands of times** and gives a key of the requested length.

```python
import hashlib

password = b"correct horse battery staple"
salt1 = bytes.fromhex("a1b2c3d4e5f60718293a4b5c6d7e8f90")
salt2 = bytes.fromhex("00112233445566778899aabbccddeeff")

key1 = hashlib.pbkdf2_hmac("sha256", password, salt1, 100_000, dklen=32)
again = hashlib.pbkdf2_hmac("sha256", password, salt1, 100_000, dklen=32)
key2 = hashlib.pbkdf2_hmac("sha256", password, salt2, 100_000, dklen=32)
print(len(key1))
print(key1 == again)
print(key1 == key2)
```

```text
32
True
False
```

Three things show:

- The key is exactly the requested length (`dklen=32`).
- The same password + the same salt **always gives the same key**; that is
  why the decrypting side can derive the key again.
- When the salt changes, the key changes. The salt **is not secret**; it is
  stored next to the encrypted data. Its job is to keep two people with the
  same password from having the same key.

The **iteration count** (100,000 here) deliberately slows the function
down. The legitimate user derives the key once and does not feel the
difference; someone searching for the password by guessing pays that
price for every guess. Current recommendations for PBKDF2 with SHA-256 are
hundreds of thousands of iterations (for example 600,000); the numbers in
this lesson are small to keep the examples fast.

## scrypt: costing memory too

PBKDF2 only costs time and can be run very fast in parallel on special
hardware. **scrypt** adds a memory requirement: each derivation needs a
certain amount of memory.

```python
import hashlib

password = b"correct horse battery staple"
salt = bytes.fromhex("a1b2c3d4e5f60718293a4b5c6d7e8f90")
key = hashlib.scrypt(password, salt=salt, n=2**14, r=8, p=1, dklen=32)
print(len(key))
print(128 * 8 * 2**14 // 2**20, "MB")
```

```text
32
16 MB
```

`n` is the cost factor, `r` the block size, `p` the parallelism. The memory
used is about `128 × r × n` bytes: 16 MB with these settings. Today the most
recommended KDF for passwords is **Argon2id**; it is not in the standard
library and is used through a separate library. The idea is the same:
salt, time and memory.

## HKDF: many keys from one secret

In the Authenticated Encryption section we saw that encryption and the MAC
need **two separate keys**. If there is a single strong master secret
(derived from a password or coming from a key exchange), both are derived
from it. The standard way is **HKDF**: it first extracts the secret with a
salt into an **intermediate key** (PRK), then expands it with a different
**label** (`info`) for each purpose.

```python
import hashlib
import hmac


def hkdf_extract(salt, secret):
    return hmac.new(salt, secret, hashlib.sha256).digest()


def hkdf_expand(prk, info, length):
    out, block, counter = b"", b"", 1
    while len(out) < length:
        block = hmac.new(prk, block + info + bytes([counter]), hashlib.sha256).digest()
        out += block
        counter += 1
    return out[:length]


master = bytes.fromhex("9f" * 32)
prk = hkdf_extract(b"app-salt-v1", master)
enc_key = hkdf_expand(prk, b"encryption", 32)
mac_key = hkdf_expand(prk, b"mac", 32)
print(enc_key == mac_key)
print(len(hkdf_expand(prk, b"long", 80)))
```

```text
False
80
```

Two **independent** keys came from the same master secret; when the `info`
label changes, the key changes. The expansion goes on, joining blocks,
until it reaches the requested length (three blocks for 80 bytes). HKDF is
**fast**: its input must already be a strong secret. For a weak input such
as a password, PBKDF2, scrypt or Argon2 comes first.

## Which KDF when

| Input | Use | Why |
|---|---|---|
| A user password | Argon2id, scrypt or PBKDF2 | Must be slow and salted |
| A strong master secret | HKDF | Fast; a separate key per purpose |
| A random key is needed | `secrets.token_bytes(32)` | No derivation needed |

## Summary

- A password is **not used directly as a key**: its length varies and it
  is not random.
- A key is derived from a password with a **slow, salted** KDF: PBKDF2,
  scrypt or Argon2id.
- The **salt** is not secret and is stored next to the data; the
  **iteration count** makes guessing expensive.
- **HKDF** derives independent keys from one strong secret with different
  `info` labels.
- The encryption and MAC keys come from the same secret but with
  **different labels**.
