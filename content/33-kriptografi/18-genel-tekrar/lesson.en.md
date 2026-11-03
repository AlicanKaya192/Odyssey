# Overall Review

This module built the toolbox of cryptography step by step: starting from
why classical ciphers break, through hashes, HMAC, symmetric and
authenticated encryption, key derivation, public-key cryptography,
signatures and certificates, all the way to TLS. This section sees them all
together; at the end there are 40 mixed questions and five exercises that
combine several sections.

## Map of the module

| Topic | Main idea |
|---|---|
| **What cryptography is** | Encoding, hashing and encryption are different things; Kerckhoffs: security is in the key, the algorithm is public. |
| **Classical ciphers** | Caesar, substitution, Vigenère; two basic moves: substitution and transposition. |
| **Breaking classical ciphers** | Brute force and letter frequency; a modern cipher must not leak patterns. |
| **XOR and the one-time pad** | Perfect secrecy under four conditions; it collapses if the key is reused; confidentiality is not integrity. |
| **Hash functions** | Deterministic, fixed length, avalanche effect; MD5 and SHA-1 are retired for integrity. |
| **HMAC** | A keyed tag; `compare_digest`; verify first, then use. |
| **Symmetric encryption** | Stream and block ciphers, a nonce is never repeated, PKCS#7 padding, AES. |
| **Block cipher modes** | ECB leaks; CBC needs a random IV; CTR turns it into a stream cipher. |
| **Authenticated encryption** | Encrypt-then-MAC; AAD; in practice AES-GCM, ChaCha20-Poly1305. |
| **Key derivation** | A slow, salted KDF from a password; separate keys from a strong secret with HKDF. |
| **Modular arithmetic** | `pow(a, e, n)`, inverse, extended Euclid, Fermat; one-way operations. |
| **RSA** | `n = p * q`, `d = e⁻¹ mod phi`; unpadded RSA is deterministic: OAEP, hybrid encryption. |
| **Diffie-Hellman and curves** | A shared secret without sending a key; no authentication; forward secrecy; ECDH. |
| **Digital signatures** | The private key signs, the public key verifies; non-repudiation; Ed25519. |
| **Certificates and PKI** | Bind a public key to a name; chain of trust, date, name, revocation, transparency. |
| **TLS** | Key share, HKDF, CertificateVerify, Finished; TLS 1.3. |
| **Common mistakes** | Encoding is not encryption; `secrets`; no secrets in code; settings are audited. |

## The path of a message

An application stores a message protected by a password, then reads it
back. Four sections of the module connect:

<figure class="fig">
<div class="flow">
<span class="node">Password + salt</span>
<span class="arrow">→</span>
<span class="node acc">PBKDF2: master key</span>
<span class="arrow">→</span>
<span class="node acc">Separate enc and mac keys</span>
<span class="arrow">→</span>
<span class="node">Encrypt, then MAC</span>
<span class="arrow">→</span>
<span class="node ok">Verify first, then decrypt</span>
</div>
<figcaption>The Key Derivation, Symmetric Encryption, HMAC and Authenticated Encryption sections in one flow.</figcaption>
</figure>

```python
import hashlib
import hmac

password = b"correct horse battery staple"
salt = bytes.fromhex("a1b2c3d4e5f60718293a4b5c6d7e8f90")
master = hashlib.pbkdf2_hmac("sha256", password, salt, 100_000, dklen=32)
enc_key = hmac.new(master, b"encryption" + bytes([1]), hashlib.sha256).digest()
mac_key = hmac.new(master, b"mac" + bytes([1]), hashlib.sha256).digest()


def keystream(key, nonce, length):
    out, counter = b"", 0
    while len(out) < length:
        out += hashlib.sha256(key + nonce + counter.to_bytes(4, "big")).digest()
        counter += 1
    return out[:length]


def seal(nonce, message):
    stream = keystream(enc_key, nonce, len(message))
    cipher = bytes(m ^ s for m, s in zip(message, stream))
    tag = hmac.new(mac_key, nonce + cipher, hashlib.sha256).digest()
    return nonce + cipher + tag


def open_box(box):
    nonce, cipher, tag = box[:8], box[8:-32], box[-32:]
    expected = hmac.new(mac_key, nonce + cipher, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expected):
        return None
    stream = keystream(enc_key, nonce, len(cipher))
    return bytes(c ^ s for c, s in zip(cipher, stream))


box = seal(b"nonce-01", b"meet at noon")
print(len(box))
print(open_box(box))
broken = box[:9] + bytes([box[9] ^ 1]) + box[10:]
print(open_box(broken))
print(enc_key != mac_key)
```

```text
52
b'meet at noon'
None
True
```

The package was an 8-byte nonce, a 12-byte ciphertext and a 32-byte tag.
When a single bit changed, the package was rejected without being
decrypted at all. The encryption and MAC keys came from the same master key
but with different labels (HKDF's single-block expansion). In a real
program this whole flow is a single AEAD call; we opened up the parts here
only to see them.

## Commonly confused pairs

| The two | The difference |
|---|---|
| Encoding / encryption | Encoding has no key; anyone can turn it back |
| Hash / encryption | A hash cannot be reversed; a cipher is decrypted with a key |
| HMAC / signature | HMAC has one shared key; in a signature the private key signs, the public key verifies |
| Nonce / salt | A nonce is unique per message in encryption; a salt is per record in a KDF |
| IV (CBC) / nonce (CTR, GCM) | An IV must be unpredictable; a nonce only unique |
| PBKDF2 / HKDF | PBKDF2 slows down a weak input (a password); HKDF derives fast from a strong secret |
| RSA encryption / RSA signature | In encryption the public key locks; in a signature the private key signs |
| Diffie-Hellman / RSA key transport | With DH the key is never sent, and there is forward secrecy |
| Certificate / private key | The certificate is public; the private key is secret |

## Summary

- Security comes from the **key**, not from keeping the algorithm secret;
  the key must be long enough and truly random.
- **Confidentiality** (encryption) and **integrity** (HMAC, signature) are
  separate jobs; together they are AEAD.
- A key from a password with a **slow, salted** KDF; separate keys from a
  strong secret with **HKDF**.
- Public-key cryptography rests on **one-way** mathematical operations; a
  **certificate** says who owns a public key.
- TLS combines all of them; the rules of correct use are in one catalog
  (Common Cryptography Mistakes).
