# Hash Functions

In the What Is Cryptography? section we met the hash briefly: a
fixed-length, non-reversible fingerprint from data of any length. We used
it to store passwords in the Storing Passwords section and to sign a token
in the Identity Management and Single Sign-On section. This section covers
which properties hash functions provide, where they are used and where they
are most often misused.

A **cryptographic hash function** takes a byte or a gigabyte, produces a
fixed-length **digest** (hash), and provides four properties:

- **Deterministic:** the same input always gives the same digest.
- **Fast:** it digests large data quickly.
- **One-way (preimage resistance):** finding the input from the digest is
  practically impossible.
- **Collision resistance:** finding two different inputs that give the same
  digest is practically impossible.

## Deterministic and fixed length

```python
import hashlib

for text in ["meet at noon", "meet at noon", "a much longer message than before"]:
    digest = hashlib.sha256(text.encode()).hexdigest()
    print(len(digest), digest[:16])
```

```text
64 50a8d1d0939b05a7
64 50a8d1d0939b05a7
64 3b10a42186bbb87c
```

The first two lines are identical: the same input gave the same digest. The
third input is much longer, but its digest is still 64 hex digits (256
bits). The digest length does not depend on the input.

## The avalanche effect

In a good hash function, when a **single bit** of the input changes, about
**half** the digest changes. This is the **avalanche effect**; it is the
hash's version of the diffusion we expected from a modern cipher in the
Breaking Classical Ciphers section. Let us count how many bits differ
between the digests of two messages:

```python
import hashlib


def bit_diff(a, b):
    x = int.from_bytes(a, "big") ^ int.from_bytes(b, "big")
    return bin(x).count("1")


h1 = hashlib.sha256(b"message 1").digest()
h2 = hashlib.sha256(b"message 2").digest()
print("total bits:", len(h1) * 8)
print("differing bits:", bit_diff(h1, h2))
```

```text
total bits: 256
differing bits: 117
```

A single character changed (`1` → `2`), but about half of the 256 bits
changed. Someone looking at the two digests cannot tell that the inputs are
"close"; the digest leaks no pattern about the input.

## Algorithms: which one, how many bits?

```python
import hashlib

for name in ["md5", "sha1", "sha256", "sha512", "sha3_256", "blake2b"]:
    size = hashlib.new(name).digest_size * 8
    print(f"{name:<9} {size} bits")
```

```text
md5       128 bits
sha1      160 bits
sha256    256 bits
sha512    512 bits
sha3_256  256 bits
blake2b   512 bits
```

All are in the standard library. But not all are secure:

| Algorithm | Status |
|---|---|
| **MD5** | Broken: collisions are easy to make. Do not use in new designs. |
| **SHA-1** | Broken: a real collision was shown in 2017. Do not use. |
| **SHA-256 / SHA-512** | Secure; the most common choice (the SHA-2 family). |
| **SHA-3** | Secure; a different internal design (a backup family). |
| **BLAKE2** | Secure and fast. |

"Broken" means collision resistance no longer holds: two different inputs
with the same digest can be produced. MD5 and SHA-1 still appear in jobs
that **do not need security**, like a fingerprint, but they are not used
for security work such as signatures or integrity checks.

## What is it used for?

The most common job of a hash is an **integrity check**: if the expected
digest of a file is known, the digest is recomputed and compared to see if
the file has changed. The SHA-256 value published next to a downloaded file
is exactly this.

```python
import hashlib

KNOWN = {
    "report.pdf": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
}


def verify(name, data):
    digest = hashlib.sha256(data).hexdigest()
    return digest == KNOWN.get(name)


print(verify("report.pdf", b""))
print(verify("report.pdf", b"tampered"))
```

```text
True
False
```

The first line is `True`: the digest of the empty content matched the
stored value (that value is the SHA-256 of the empty byte string). On the
second line a single byte changed and the digest did not match. The same
idea is used in file verification over a network, deduplication and version
control (Git's object ids).

## Two common mistakes

**1. Storing a password as a plain hash.** A hash is fast; that is good for
integrity but bad for passwords. An attacker can try billions of passwords
per second. That is why passwords are stored with a **slow, salted**
password hash (the Storing Passwords section), not a plain SHA-256.

**2. Thinking a hash is proof of integrity.** A plain hash protects data
against **accidental** corruption but not against a **deliberate** change:
an attacker can change the data and recompute the hash. For integrity that
also proves the sender's identity, a keyed construction is needed: HMAC
(the Message Authentication: HMAC section).

## Why are collisions unavoidable but not findable in a secure algorithm?

The number of inputs is infinite and the number of digests is finite
(`2²⁵⁶` for a 256-bit digest); so inputs with the same digest **do exist**.
What matters is being able to **find** them. The number of random tries
needed to find a collision is proportional to the power of half the digest
length (`2^(n/2)`); this is called the **birthday bound**. Let us compute
it:

```python
for bits in [64, 128, 256]:
    tries = 2 ** (bits / 2)
    print(f"{bits:>3} bits: ~2^{bits // 2} = {tries:.2e} tries")
```

```text
 64 bits: ~2^32 = 4.29e+09 tries
128 bits: ~2^64 = 1.84e+19 tries
256 bits: ~2^128 = 3.40e+38 tries
```

For a 64-bit digest about four billion tries are enough (which is why short
digests are not used for security); for 256 bits the number needed compares
to the number of atoms in the universe. That is why today's digests are at
least 256 bits, and the problem with the "broken" MD5/SHA-1 is that
collisions can be found with far less than the mathematical bound.

## Summary

- A cryptographic hash is **deterministic**, **one-way** and **collision
  resistant**; its output is fixed length.
- **The avalanche effect:** changing one bit changes about half the digest.
- **MD5 and SHA-1 are broken**; today SHA-256, SHA-3 or BLAKE2 is used.
- A hash is for an **integrity check**; a password needs a slow salted
  hash, proof of sender needs HMAC.
- **The birthday bound:** a collision is found in `2^(n/2)` tries; that is
  why digests are at least 256 bits.
