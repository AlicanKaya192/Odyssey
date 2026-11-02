# What Is Cryptography?

**Cryptography** is the science of protecting information with
**mathematics** against people who should not see or change it. In the
Security Fundamentals module we used some of its tools: we stored passwords
as salted hashes (Storing Passwords) and signed a token with HMAC (Identity
Management and Single Sign-On). This module opens those tools up: what they
do, how they work and where they are most often misused.

## Basic words

| Term | Meaning |
|---|---|
| **Plaintext** | The real message to protect |
| **Ciphertext** | The unreadable text that comes out of encryption |
| **Encryption** | Turning plaintext into ciphertext with a key |
| **Decryption** | Turning ciphertext back with a key |
| **Key** | The secret value that makes the operation personal |
| **Cipher** | The rule for encryption and decryption |

<figure class="fig"><div class="flow">
  <span class="node">Plaintext</span><span class="arrow">→</span>
  <span class="node acc">Encrypt (key)</span><span class="arrow">→</span>
  <span class="node">Ciphertext</span><span class="arrow">→</span>
  <span class="node acc">Decrypt (key)</span><span class="arrow">→</span>
  <span class="node ok">Plaintext</span>
</div><figcaption>The cipher is known to everyone; only the key is secret.</figcaption></figure>

## Encoding, hashing, encryption: three different things

These three words are often mixed up, and mixing them up leads to real
vulnerabilities.

**Encoding** is writing data in another form; there is no key and anyone
can reverse it. Base64 is the most common example:

```python
import base64

message = "meet at noon"
encoded = base64.b64encode(message.encode()).decode()
print(encoded)
print(base64.b64decode(encoded).decode())
```

```text
bWVldCBhdCBub29u
meet at noon
```

No secret was needed to produce the second line. We read the body of the
token in the Identity Management section the same way, without a key.
Base64 looks "encrypted" but gives no confidentiality.

A **hash** makes a fixed-length fingerprint from data of any length and
**cannot be reversed**:

```python
import hashlib

for text in ["meet at noon", "meet at noon!"]:
    digest = hashlib.sha256(text.encode()).hexdigest()
    print(digest[:16], len(digest))
```

```text
50a8d1d0939b05a7 64
994f34a2a5f4b73d 64
```

A single exclamation mark changed the whole hash, while the length stayed
64 hex digits (256 bits). There is no way to get the message back from the
hash; that is why passwords are stored as hashes, not encrypted.

**Encryption** can be reversed **with a key**: whoever knows the key can
read it, whoever does not cannot.

| | Key? | Reversible? | What for? |
|---|---|---|---|
| Encoding | None | For everyone | Carrying data (e-mail, URLs) |
| Hash | None | No | Fingerprints, storing passwords |
| Encryption | Yes | Only with the key | Confidentiality |

## What does cryptography provide?

The CIA triad and the concepts next to it from What Is Security? The CIA
Triad map to tools here:

| Goal | Tool | In this module |
|---|---|---|
| **Confidentiality** | Encryption | Symmetric Encryption, RSA |
| **Integrity** | Hash, HMAC | Hash Functions, HMAC |
| **Authenticity** | HMAC, digital signature | HMAC, Digital Signatures |
| **Non-repudiation** | Digital signature | Digital Signatures |

Cryptography does not provide **availability**: on the contrary, whoever
loses the key cannot reach their own data either.

## Two families: symmetric and asymmetric

- **Symmetric**: the one who encrypts and the one who decrypts use the
  **same** key. It is fast; the problem is getting the key to the other
  side safely.
- **Asymmetric**, or public-key: there is a **public key** (given to
  everyone) and a **private key** (only with its owner). It is slow but it
  solves the problem of sharing the key.

Real systems use both together: they agree on a symmetric key with an
asymmetric method and encrypt the data with that key. The TLS Handshake
section at the end of the module describes exactly this.

## Kerckhoffs's principle

In the 19th century Auguste Kerckhoffs wrote: a cipher system must stay
secure even if everything except the key falls into the enemy's hands. This
is the **open design** principle from the Security Principles section
itself. If the algorithm is kept secret, one day it leaks and that day the
whole system collapses; if a key leaks, only that key is changed.

That is why the trusted algorithms are the published ones that have been
open to everyone's attacks for years. Security rests only on the secrecy of
the **key** and on how many keys there are.

## How long should a key be?

An `n`-bit key has `2ⁿ` possible values. If an attacker tries each one
(**brute force**), how long does it take? Assume a trillion guesses per
second:

```python
SECONDS_PER_YEAR = 365 * 24 * 3600
rate = 10**12  # a trillion guesses per second

for bits in [40, 56, 80, 128]:
    years = 2**bits / rate / SECONDS_PER_YEAR
    print(f"{bits:>3} bits: {years:.2e} years")
```

```text
 40 bits: 3.49e-08 years
 56 bits: 2.28e-03 years
 80 bits: 3.83e+04 years
128 bits: 1.08e+19 years
```

40 bits takes about a second, 56 bits less than a day; 128 bits is hundreds
of millions of times the age of the universe (about 1.4 × 10¹⁰ years). Every
extra bit doubles the time. Today 128 bits is accepted as the lower limit
for symmetric keys.

## Don't write your own crypto

In this module we will write many things from scratch with small toy
examples, because seeing the inside is the best way to understand misuse.
But in a real application **you do not write your own cipher or protocol**:
you use the high-level function of a well-tested library. Vulnerabilities
are found years later even in algorithms written by experts; in
cryptography mistakes are silent, the program keeps working and nobody
notices.

## Summary

- Cryptography provides confidentiality, integrity, authenticity and
  non-repudiation; it does not provide availability.
- **Encoding** has no key and is reversible, a **hash** is not reversible,
  **encryption** is reversible only with the key. Base64 is not encryption.
- **Symmetric** means one key, **asymmetric** a public and a private key;
  real systems use both.
- **Kerckhoffs's principle:** the algorithm is open, only the key is secret.
- Every extra bit doubles the brute-force time; 128 bits is today's lower
  limit.
- In a real application you do not write your own crypto.
