# Storing Passwords

To be able to check a user's password, a system has to store something.
What it stores and how decides how bad things are on the day the database
leaks. This section's question is: **what should you store so that the
passwords stay safe even if your database is stolen?**

## Plain text and encryption: both wrong

- **Plain text:** storing the password as it is. Everyone who sees the
  database (an attacker, a curious employee, someone who finds a backup)
  reads all the passwords. Because users use the same password elsewhere,
  the damage is not limited to that site either.
- **Encryption:** encrypting the password with a key. It looks better, but
  the ciphertext can be opened again with the key. The key is often on the
  same server as the database; if both leak together, it is no better than
  plain text.

There is **no need at all** to open the password again. The system only
has to answer the question "is the typed password correct?". A one-way
operation is used for that: a **hash**.

## Why a plain hash is not enough

A hash function produces a fixed-length value from a text, and you cannot
go back from that value to the text. The password's hash is stored; at
login the hash of the typed password is taken and compared. But a plain
hash has two problems:

```python
import hashlib

users = [("ada", "sunshine1"), ("alan", "sunshine1"), ("grace", "Sunshine1")]
for user, password in users:
    digest = hashlib.sha256(password.encode()).hexdigest()
    print(f"{user:<6} {digest[:20]}")
```

```text
ada    284fff3bd254b48cca05
alan   284fff3bd254b48cca05
grace  4fe3c8595d0054272ecf
```

1. **Same password, same hash.** Ada's and Alan's hashes are exactly the
   same. Someone who sees the database groups the people using the same
   password at once, and finding one means finding the other. Worse: the
   hashes of common passwords have been computed in advance and put into
   tables (a **precomputed table**; a space-saving kind of it is called a
   **rainbow table**). The table names the password the moment it sees
   the hash.
2. **Speed.** SHA-256 was designed to be fast, so that big files can be
   hashed quickly too. For passwords that is a flaw: an attacker offline
   tries billions of passwords a second (the "offline" speed from the
   Passwords section).

## Salt: separate for every user

The answer to the first problem is **salt**: a value generated at random
for every user that goes into the hash together with the password. The salt
is not secret; it is stored next to the hash. Its job is to make the same
password give a different hash for every user:

```python
import secrets

salts = {}
for user in ["ada", "alan"]:
    salts[user] = secrets.token_bytes(16)
    print(user, len(salts[user]), "salt bytes")
ada = hashlib.sha256(salts["ada"] + b"sunshine1").digest()
alan = hashlib.sha256(salts["alan"] + b"sunshine1").digest()
print("same hash:", ada == alan)
```

```text
ada 16 salt bytes
alan 16 salt bytes
same hash: False
```

Now the two users' hashes differ even though their passwords are the same.
Precomputed tables stop working too: the attacker would have to compute
the table again for every salt, which wipes out the table's whole
advantage. Every user's password has to be tried **separately**.

## A slow hash: key stretching

The answer to the second problem is to make the hash **slow on purpose**.
Making the user wait a small fraction of a second for one hash at login
bothers nobody; but for an attacker who wants billions of tries, the same
slowness repeats on every try. This is called **key stretching**.

`hashlib.pbkdf2_hmac` from Python's standard library does this: it takes
the hash thousands of times in a row. How many times is the **iteration
count**. For PBKDF2-HMAC-SHA256 the current recommendation is 600,000
iterations.

```python
salt = bytes.fromhex("8f2a1c9e5b7d3f60a4c2e8b1d6f09a37")
key = hashlib.pbkdf2_hmac("sha256", b"sunshine1", salt, 600_000)
print(len(key), key.hex()[:32])
```

```text
32 95ac3727b4efa2fe0c28c480179ffa87
```

In this example the salt is written as a constant, so that the output is
the same on every run. In real use the salt is made for every user with
`secrets.token_bytes(16)`.

How slow is it? Let us measure on this computer, printing only the
comparison, not the times:

```python
import time

start = time.perf_counter()
for _ in range(10_000):
    hashlib.sha256(salt + b"sunshine1").digest()
fast = (time.perf_counter() - start) / 10_000
start = time.perf_counter()
hashlib.pbkdf2_hmac("sha256", b"sunshine1", salt, 600_000)
slow = time.perf_counter() - start
print("at least 10000 times slower:", slow > fast * 10_000)
```

```text
at least 10000 times slower: True
```

A single SHA-256 is too short to measure, so the average of ten thousand
was taken. The number of tries an attacker can make per second drops by at least the
same factor: ten billion tries a second become at most a million. That is why the
"offline" line from the Passwords section no longer holds for well-stored
passwords.

## What is stored?

To verify, the **name of the algorithm**, the **iteration count** and the
**salt** are needed next to the hash. A common way is to keep them all in
one piece of text, separated by `$` signs:

```python
import hmac


def make_record(password, salt, iterations):
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${key.hex()}"


def verify(password, record):
    algorithm, iterations, salt_hex, key_hex = record.split("$")
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(iterations))
    return hmac.compare_digest(key.hex(), key_hex)


record = make_record("sunshine1", salt, 1000)
print(record[:46] + "...")
print(verify("sunshine1", record), verify("sunshine2", record))
```

```text
pbkdf2_sha256$1000$8f2a1c9e5b7d3f60a4c2e8b1d6f...
True False
```

Verification does the same calculation again with the salt and iteration
count from the record and compares the result. The comparison is done with
`hmac.compare_digest`, not `==`: `==` stops at the first different
character and the time taken can give a hint.

Having the iteration count in the record has another benefit: when the
recommendation goes up later, old records do not break. The next time the
user types the correct password at login, the password is hashed again with
the new count and saved.

## Other algorithms

We use PBKDF2 in this lesson because it is in the standard library. There
are other algorithms designed for storing passwords: **bcrypt**, **scrypt**
(`hashlib.scrypt`) and **Argon2**. scrypt and Argon2 spend not only time
but also **memory**; this also makes attacks with hardware that has many
parallel cores expensive. For a new system the current recommendation is
usually Argon2id. Whichever is chosen, the rules are the same: salted,
slow, parameters in the record.

## Summary

- Passwords are stored not as plain text or encrypted, but as a **salted,
  slow hash**.
- The problems of a plain hash: the same password gives the same hash
  (precomputed tables) and it is very fast.
- **Salt** is separate for every user, random and not secret.
- **Key stretching** (PBKDF2, bcrypt, scrypt, Argon2) makes every try
  expensive.
- The record holds the algorithm, the iteration count, the salt and the
  hash together; verification uses `hmac.compare_digest`.
