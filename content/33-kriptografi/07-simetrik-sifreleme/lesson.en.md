# Symmetric Encryption

In the What Is Cryptography? section we introduced two families:
**symmetric** (the one who encrypts and the one who decrypts use the same
key) and asymmetric. In the XOR and the One-Time Pad section we saw the
purest form of symmetric encryption: XORing the message with a random key.
Its only problem was that the key had to be as long as the message and used
once. This section covers the modern symmetric encryption that makes that
idea practical: making a long key stream from a short key.

## Two kinds: stream and block

- **Stream cipher:** makes a random-looking **keystream** as long as the
  message from the key and XORs it with the message. The practical form of
  the one-time pad.
- **Block cipher:** splits the message into fixed-size blocks and mixes
  each block with the key. The most common example is **AES**.

## A toy stream cipher

In the one-time pad the key was as long as the message. In a stream cipher
we **make** a long stream from a short key. Here we build a harmless toy
that does this with a hash function: for each block, `hash(key + nonce +
counter)` gives a piece of keystream, the pieces are joined and XORed with
the message. A **nonce** (number used once) is a number that changes with
every message and is never repeated.

```python
import hashlib


def keystream(key, nonce, length):
    out = b""
    counter = 0
    while len(out) < length:
        block = hashlib.sha256(key + nonce + counter.to_bytes(4, "big")).digest()
        out += block
        counter += 1
    return out[:length]


def toy_cipher(key, nonce, data):
    stream = keystream(key, nonce, len(data))
    return bytes(d ^ s for d, s in zip(data, stream))


key = b"a 16-byte key!!!"
nonce = b"nonce-1234"
message = b"the treasure is buried under the old oak"
cipher = toy_cipher(key, nonce, message)
print(cipher.hex()[:32])
print(toy_cipher(key, nonce, cipher))
```

```text
52f20fb9990a1ce25094870ed53e0a67
b'the treasure is buried under the old oak'
```

Encryption and decryption are the same operation (XOR), just as in the
one-time pad. But the key is only 16 bytes; the long stream was made by the
hash function. **This toy is not used in a real system** (real stream
ciphers such as ChaCha20 are special designs); here we only see the idea.

## Why is a nonce needed?

In the XOR section we saw that reusing the key for two messages is a
disaster: `c1 ^ c2 = m1 ^ m2`. In a stream cipher we want to use the same
key for many messages; the nonce makes this safe. **The same key but a
different nonce** makes a different keystream for each message:

```python
m = b"attack at dawn"
c1 = toy_cipher(key, b"nonce-0001", m)
c2 = toy_cipher(key, b"nonce-0002", m)
print(c1.hex()[:20])
print(c2.hex()[:20])
print(c1 == c2)
```

```text
b1e25dad0364bc6e3b29
1d913ab6ef1249fcdeed
False
```

The same message, the same key, but two different ciphertexts. This way the
attacker cannot even learn "these two messages are the same" (the "same
message, different ciphertext" expectation from the Breaking Classical
Ciphers section). **The rule: a nonce is never used twice with the same
key;** if it is, the stream cipher falls into the key-reuse mistake of the
one-time pad. The nonce need not be secret, only **unique**; it is sent in
the clear next to the ciphertext.

## A block cipher and padding

Block ciphers split the message into fixed-size blocks (16 bytes in AES).
If the message is not a multiple of the block size, the last block is
completed with **padding**. The most common method is **PKCS#7**: however
many bytes are missing, that many bytes, each equal to that number, are
added. When decrypting, the last byte says how many padding bytes were
added:

```python
def pad(data, block=16):
    need = block - (len(data) % block)
    return data + bytes([need]) * need


def unpad(data):
    return data[:-data[-1]]


for text in [b"short", b"exactly 16 bytes"]:
    padded = pad(text)
    print(len(text), "->", len(padded), "last:", padded[-1])
    print(unpad(padded) == text)
```

```text
5 -> 16 last: 11
True
16 -> 32 last: 16
True
```

Note that even a message of exactly 16 bytes gets **a whole new block** (16
bytes, all 16) added: otherwise, when decrypting, the real data and the
padding could not be told apart. Stream ciphers need no padding (they make
keystream as long as the message); padding is specific to block ciphers.

## AES: the standard symmetric cipher

**AES** (Advanced Encryption Standard) is today's standard for symmetric
encryption. It works on 128-bit blocks and has three key sizes:

```python
for bits in [128, 192, 256]:
    print(f"AES-{bits}: key {bits // 8} bytes, block 16 bytes")
```

```text
AES-128: key 16 bytes, block 16 bytes
AES-192: key 24 bytes, block 16 bytes
AES-256: key 32 bytes, block 16 bytes
```

Inside, AES applies the two basic moves from the Classical Ciphers section
(substitution and transposition) one over the other for many rounds; the
result is a ciphertext indistinguishable from random. **AES is not in
Python's standard library**; in a real application it is used through the
high-level function of a separate library (such as authenticated AES-GCM).
That is why we describe AES's idea in the lesson rather than running it. How
a block cipher chains its blocks (the modes) and the role of the nonce/IV
there is the subject of the next section, Block Cipher Modes and IVs.

## Don't write your own cipher

The toy stream cipher above is there to show the idea. In reality you **do
not write your own symmetric cipher**: you use the **authenticated
encryption** function of a well-tested library, which gives both
confidentiality and integrity (the Authenticated Encryption section).
Because encryption alone, as we saw in the XOR section, does not stop the
message being changed; it needs a MAC alongside it.

## Summary

- **Symmetric encryption** uses one key; two kinds: **stream** (XOR with a
  keystream) and **block** (like AES, fixed blocks).
- A stream cipher makes the one-time pad idea practical by making a **long
  keystream** from a short key.
- A **nonce** lets the same key be used safely for many messages; it must
  be unique, need not be secret, and is **never repeated.**
- **Block ciphers need padding** (PKCS#7); stream ciphers do not.
- **AES** is the standard (128/192/256-bit key, 128-bit block) but is not
  in the standard library; in reality it is used through a library, in an
  authenticated mode.
- Do not write your own symmetric cipher; use authenticated encryption.
