In a real application the salt, the digest and the iteration count are stored
in the database as **one string**. The format also carries the algorithm's
name and setting, so old records can still be verified even when the setting
changes over the years. (Frameworks like Django use a similar format.)

```python
import hashlib
import hmac
import secrets

ITERATIONS = 200_000


def make_record(password, iterations=ITERATIONS):
    salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${key.hex()}"


def verify(password, record):
    _, rounds, salt_hex, key_hex = record.split("$")
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(rounds))
    return hmac.compare_digest(key.hex(), key_hex)


def needs_upgrade(record):
    return int(record.split("$")[1]) < ITERATIONS


record = make_record("correct horse")
print(record.split("$")[:2], len(record))
print(verify("correct horse", record), verify("correct horse!", record))
old = make_record("correct horse", 100_000)
print(verify("correct horse", old), needs_upgrade(old))
```

```text
['pbkdf2_sha256', '200000'] 118
True False
True True
```

## The parts of the record

`pbkdf2_sha256$200000$<salt>$<digest>`:

- **Algorithm name:** if you move to `scrypt` later, this tells which record
  is verified which way.
- **Iteration count:** raised as computers get faster. An old record carries
  its own count, so it still verifies (`old` → `True`).
- **Salt and digest** as hexadecimal text: they fit in a plain text column in
  the database.

## Upgrading the setting

You cannot recompute a digest without knowing the user's password. But the
moment the user **logs in**, the password is in your hands: if verification
succeeds and `needs_upgrade(record)` is true, a new record is written with
`make_record(password)`. That way records quietly get stronger as people log
in.

## Do not

- Write a password or its digest to a log file.
- Email the old password on "forgot password": if it cannot be reversed, it
  cannot be sent either. The right way is a one-time, expiring link made with
  `secrets.token_urlsafe`.
- Invent your own hashing algorithm.
