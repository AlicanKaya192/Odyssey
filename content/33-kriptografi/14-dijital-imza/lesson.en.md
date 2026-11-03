# Digital Signatures

In the Message Authentication: HMAC section we saw that a tag shows a
message has not changed. But HMAC has a limit: verifying the tag needs
**the same secret key**, so anyone who can verify a tag can also make one.
A **digital signature** removes that limit: only the owner of the **private
key** signs, and anyone with the **public key** verifies.

## Hash first, then sign

We use the key pair from the RSA section in the opposite direction: in
encryption the public key locked and the private key opened; in a signature
**the private key signs and the public key verifies**. What gets signed is
not the message itself but its **hash**: the hash is short and fixed in
length, however long the message is.

```python
import hashlib

p, q = 104723, 104729
n = p * q
e = 65537
d = pow(e, -1, (p - 1) * (q - 1))


def digest(message):
    h = hashlib.sha256(message).digest()
    return int.from_bytes(h, "big") % n


def sign(message):
    return pow(digest(message), d, n)


def verify(message, signature):
    return pow(signature, e, n) == digest(message)


signature = sign(b"release 2.4.1")
print(verify(b"release 2.4.1", signature))
```

```text
True
```

The signature was made only with `d`, the verification only with `e` and
`n`. `e` and `n` are the public key: anyone can hold them and verify.

## A changed message, another key

```python
print(verify(b"release 2.4.2", signature))
print(verify(b"release 2.4.1", signature + 1))
print(verify(b"x" * 100000, sign(b"x" * 100000)))
```

```text
False
False
True
```

When one character of the message changed, the signature did not match;
when the signature itself changed, it did not match either. A 100,000-byte
message was signed the same way, because what is signed is always the
32-byte hash. (Since the toy `n` is 34 bits, we reduce the hash modulo `n`
here; in a real signature the hash fits inside the key and is signed with
padding.)

A signature cannot be verified with another key pair either:

```python
p2, q2 = 104717, 104743
n2 = p2 * q2
other = pow(digest(b"release 2.4.1"), pow(e, -1, (p2 - 1) * (q2 - 1)), n2)
print(verify(b"release 2.4.1", other))
```

```text
False
```

A signature made with another private key does not match our public key.
A signature says both "the message has not changed" and "the owner of this
private key signed it".

## HMAC versus a signature

| | HMAC | Digital signature |
|---|---|---|
| Key | One shared secret key | The private key signs, the public key verifies |
| Who verifies? | Only those who know the key | Anyone with the public key |
| Who can make one? | Anyone who can verify | Only the private key's owner |
| Non-repudiation | No | Yes |
| Speed | Very fast | Slower |
| Typical use | Server-side tokens, API requests | Software updates, certificates, email |

**Non-repudiation**: with HMAC both sides can make the tag, so someone can
say "I did not send this message"; with a signature only the owner of the
private key can sign, so they cannot (unless the private key was stolen).

## Real signature algorithms

| Algorithm | Based on | Note |
|---|---|---|
| RSA-PSS | RSA | PSS with random padding instead of the textbook RSA signature |
| ECDSA | Elliptic curve | Needs a **unique, secret** random number for every signature |
| Ed25519 | Elliptic curve (Edwards) | Derives that number itself, deterministically from the message; less room for mistakes |

ECDSA's rule is strict: if the secret number used for a signature repeats
or can be predicted, **the private key is revealed**. That is why new
systems mostly choose Ed25519. Whichever is used, signatures are made and
verified with a well-tested library.

## Where signatures are used

- **Software updates:** the program downloads the new version, verifies its
  signature with the maker's public key, and does not install it if the
  signature does not match.
- **Identity tokens:** the identity provider's signature on the token from
  the Identity Management and Single Sign-On section; signature first,
  then the claims.
- **Certificates:** an authority's signature says whom a public key belongs
  to (the next section, Certificates and PKI).

## Summary

- The **private key** signs, the **public key** verifies; anyone can
  verify, only the owner can sign.
- What gets signed is the message's **hash**, not the message itself.
- If the message or the signature changes by one bit, verification fails.
- The difference from HMAC: **non-repudiation** and public verification.
- In practice RSA-PSS, ECDSA or Ed25519; in ECDSA the per-signature number
  is never repeated.
