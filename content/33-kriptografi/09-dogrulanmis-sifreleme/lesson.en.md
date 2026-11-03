# Authenticated Encryption

The Symmetric Encryption and Block Cipher Modes sections ended with the
same warning: encryption **hides** a message but does **not prevent** it
from being changed. In the Message Authentication: HMAC section we saw the
tag that catches a change. This section combines the two: **authenticated
encryption**, which both hides and authenticates.

## Why encryption alone is not enough

In the XOR and the One-Time Pad section we saw that flipping a bit of a
stream cipher's ciphertext flips the same bit of the plaintext. Let us see
it once more on our own toy cipher; the point is to show that the receiver
**notices nothing**.

```python
import hashlib


def keystream(key, nonce, length):
    out, counter = b"", 0
    while len(out) < length:
        out += hashlib.sha256(key + nonce + counter.to_bytes(4, "big")).digest()
        counter += 1
    return out[:length]


def toy_cipher(key, nonce, data):
    return bytes(d ^ s for d, s in zip(data, keystream(key, nonce, len(data))))


enc_key = b"enc-key-0123456789abcdef"
nonce = b"nonce-001"
cipher = toy_cipher(enc_key, nonce, b"pay 100 to ada")
changed = bytearray(cipher)
changed[4] ^= ord("1") ^ ord("9")
print(toy_cipher(enc_key, nonce, bytes(changed)))
```

```text
b'pay 900 to ada'
```

A single byte of the ciphertext changed and the decrypted message said
`900` instead of `100`. Decryption raised no error: the cipher does not
know whether the message was changed. There is confidentiality but no
**integrity** (the second letter of the What Is Security? The CIA Triad
section).

## Encrypt, then MAC

The fix is to add an HMAC tag to the ciphertext. The right order is
**encrypt-then-MAC**: the tag is computed over **the nonce and the
ciphertext**. **Two separate keys** are used for encryption and the MAC.

```python
import hmac

mac_key = b"mac-key-fedcba9876543210"


def seal(enc_key, mac_key, nonce, message):
    cipher = toy_cipher(enc_key, nonce, message)
    tag = hmac.new(mac_key, nonce + cipher, hashlib.sha256).digest()
    return nonce + cipher + tag


def open_box(enc_key, mac_key, box):
    nonce, cipher, tag = box[:9], box[9:-32], box[-32:]
    expected = hmac.new(mac_key, nonce + cipher, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expected):
        return None
    return toy_cipher(enc_key, nonce, cipher)


box = seal(enc_key, mac_key, nonce, b"pay 100 to ada")
print(len(box))
print(open_box(enc_key, mac_key, box))
```

```text
55
b'pay 100 to ada'
```

The package has three parts: a 9-byte nonce, a 14-byte ciphertext and a
32-byte tag. `open_box` first checks the tag and decrypts **only if the tag
matches**. The HMAC section's "verify first, then use" rule became "verify
first, then decrypt" here.

## A changed package is rejected

Let us make the same byte change on the protected package:

```python
broken = bytearray(box)
broken[13] ^= ord("1") ^ ord("9")
print(open_box(enc_key, mac_key, bytes(broken)))
```

```text
None
```

The tag did not match and `open_box` returned `None` without decrypting at
all. The receiver never even sees the changed message; this makes sure
nothing is done with changed data (**fail securely** from the Security
Principles section).

## Why the order matters

There are three ways to combine encryption and a MAC, and only one is
considered safe in every case:

| Way | Tag over what? | Result |
|---|---|---|
| Encrypt-then-MAC | The ciphertext | **Recommended**: rejected without decrypting |
| MAC-then-encrypt | The plaintext (both encrypted together) | Must decrypt before verifying |
| Encrypt-and-MAC | The plaintext (tag in the clear) | The tag can leak information about the plaintext |

With encrypt-then-MAC the receiver **never decrypts** changed data. In the
other two, verifying requires decrypting, and code that handles changed
data can leak information through its errors.

## Additional authenticated data (AAD)

Sometimes a piece of information **does not need to be hidden but must not
be changed**: the message's recipient, a version number, the packet's
header. This is called **additional authenticated data** (**AAD**): it
stays in the clear but goes into the tag.

```python
def seal_aad(enc_key, mac_key, nonce, header, message):
    cipher = toy_cipher(enc_key, nonce, message)
    data = len(header).to_bytes(4, "big") + header + nonce + cipher
    tag = hmac.new(mac_key, data, hashlib.sha256).digest()
    return cipher, tag


def check_aad(mac_key, nonce, header, cipher, tag):
    data = len(header).to_bytes(4, "big") + header + nonce + cipher
    expected = hmac.new(mac_key, data, hashlib.sha256).digest()
    return hmac.compare_digest(tag, expected)


cipher, tag = seal_aad(enc_key, mac_key, nonce, b"to:ada", b"pay 100")
print(check_aad(mac_key, nonce, b"to:ada", cipher, tag))
print(check_aad(mac_key, nonce, b"to:bob", cipher, tag))
```

```text
True
False
```

The header was not encrypted; anyone can see it says `to:ada`. But when it
became `to:bob`, the tag did not match. The header's **length** is written
in front of it: otherwise the boundary between the end of the header and
the start of the nonce is ambiguous, and two different (header, data)
pairs could give the same bytes.

## In real systems: AEAD

Real applications do not combine these parts by hand. They use **AEAD**
(Authenticated Encryption with Associated Data) algorithms that do the
encryption, the tag and the AAD in one operation:

<figure class="fig">
<div class="versus">
<div>
<h4>AES-GCM</h4>
AES in CTR mode + a tag. 12-byte nonce, 16-byte tag. Very fast on
processors with hardware support for AES.
</div>
<div>
<h4>ChaCha20-Poly1305</h4>
The ChaCha20 stream cipher + a Poly1305 tag. 32-byte key, 12-byte nonce,
16-byte tag. Fast even without hardware support.
</div>
</div>
<figcaption>Two common AEAD algorithms. Neither is in the standard library; they are used from a well-tested library.</figcaption>
</figure>

Two rules are the same for both: **a nonce is never repeated with the same
key** (in GCM a repeated nonce breaks both confidentiality and
authentication), and if the tag does not match, the output is **never
used**. The library raises an error when the tag does not match; catching
that error and trying to use the data anyway throws away all the
protection.

## Summary

- Encryption alone gives **confidentiality**; a changed ciphertext
  decrypts without an error.
- **Encrypt-then-MAC:** the tag is over the nonce + ciphertext, with
  separate keys for encryption and the MAC.
- The receiver **checks the tag first** and does not decrypt at all if it
  does not match.
- **AAD** is data that is not hidden but must not be changed; it goes into
  the tag.
- In practice **AEAD** is used: AES-GCM or ChaCha20-Poly1305; the nonce is
  never repeated.
