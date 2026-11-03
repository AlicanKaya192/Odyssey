# Block Cipher Modes and IVs

In the Symmetric Encryption section we saw that a block cipher splits the
message into 16-byte blocks and completes the last block with padding. But
one question was left open: a block cipher encrypts **a single block**; how
are the blocks of a long message tied together? This way of tying them is
called a **mode of operation**, and choosing the wrong mode can make even a
strong cipher useless.

## A toy block cipher

AES is not in the standard library. To see the modes we build a small
**toy** block cipher working on 16-byte blocks. Its structure is a
**Feistel network**, which real block ciphers use too: the block is split
into two halves, in each round one half is XORed with a keyed hash of the
other half, and the halves swap places. Applying the rounds in reverse
brings the block back.

```python
import hashlib


def round_fn(key, i, half):
    return hashlib.sha256(key + bytes([i]) + half).digest()[:8]


def encrypt_block(key, block):
    left, right = block[:8], block[8:]
    for i in range(4):
        mixed = bytes(a ^ b for a, b in zip(left, round_fn(key, i, right)))
        left, right = right, mixed
    return left + right


def decrypt_block(key, block):
    left, right = block[:8], block[8:]
    for i in reversed(range(4)):
        mixed = bytes(a ^ b for a, b in zip(right, round_fn(key, i, left)))
        left, right = mixed, left
    return left + right


key = b"toy-block-key-16"
cipher = encrypt_block(key, b"exactly16bytes!!")
print(cipher.hex()[:16])
print(decrypt_block(key, cipher))
```

```text
6fcb9dd4b0ccbb92
b'exactly16bytes!!'
```

This toy is only for showing the modes; a real system uses AES.

## ECB: each block on its own

The simplest mode is **ECB** (Electronic Codebook): each block is encrypted
separately with the same key. The problem: **the same plaintext block
always becomes the same ciphertext block**.

```python
def ecb_encrypt(key, data):
    out = b""
    for i in range(0, len(data), 16):
        out += encrypt_block(key, data[i:i + 16])
    return out


message = b"YELLOW SUBMARINE" * 2 + b"another block 16"
cipher = ecb_encrypt(key, message)
blocks = [cipher[i:i + 16].hex()[:8] for i in range(0, len(cipher), 16)]
print(blocks)
print(blocks[0] == blocks[1])
```

```text
['48fd288d', '48fd288d', '88cf223f']
True
```

The first two ciphertext blocks are identical: even someone who does not
know the key reads "the first two blocks of the message are the same". This
is the block-level form of the substitution cipher's problem from the
Breaking Classical Ciphers section: repeated plaintext shows up as
repetition in the ciphertext. Encrypting an image with ECB leaves its
outlines visible. **ECB is not used.**

## CBC: chaining the blocks

**CBC** (Cipher Block Chaining) XORs each plaintext block with **the
previous ciphertext block** before encrypting it. The first block has no
previous block; a random **initialization vector** (**IV**) is used instead.

```python
def cbc_encrypt(key, iv, data):
    prev, out = iv, b""
    for i in range(0, len(data), 16):
        block = bytes(a ^ b for a, b in zip(data[i:i + 16], prev))
        prev = encrypt_block(key, block)
        out += prev
    return out


iv1 = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
iv2 = bytes.fromhex("f0e0d0c0b0a090807060504030201000")
c1 = cbc_encrypt(key, iv1, message)
c2 = cbc_encrypt(key, iv2, message)
print(c1[:16] == c1[16:32])
print(c1 == c2)
```

```text
False
False
```

Now the two identical plaintext blocks became different ciphertext blocks
(the chain tied each block to the one before it), and the same message gave
a completely different ciphertext with a different IV. The IV **does not
need to be secret**; it is put in front of the ciphertext and sent along.
But in CBC it must be **unpredictable** (random). CBC needs padding and does
not provide integrity on its own.

## CTR: a stream cipher from a block cipher

**CTR** (Counter) mode turns a block cipher into a stream cipher: it
encrypts not the plaintext but the **nonce + counter** block, and XORs the
output with the message as a keystream. It is the toy stream cipher from
the Symmetric Encryption section, made with a block cipher instead of a
hash.

```python
def ctr_crypt(key, nonce, data):
    out = b""
    for n, i in enumerate(range(0, len(data), 16)):
        stream = encrypt_block(key, nonce + n.to_bytes(8, "big"))
        out += bytes(a ^ b for a, b in zip(data[i:i + 16], stream))
    return out


nonce = bytes(8)
secret = ctr_crypt(key, nonce, b"no padding needed here")
print(len(secret))
print(ctr_crypt(key, nonce, secret))
```

```text
22
b'no padding needed here'
```

A 22-byte message gave a 22-byte ciphertext: **no padding was needed**.
Encryption and decryption are the same operation, and `decrypt_block` was
never used to decrypt. But the rule of stream ciphers holds here too: **a
nonce is never repeated with the same key** (the XOR and the One-Time Pad
section).

## Comparing the modes

| Mode | Same block → same output? | IV / nonce | Padding | Integrity |
|---|---|---|---|---|
| ECB | **Yes** (leaks) | None | Needed | None |
| CBC | No | Random IV | Needed | None |
| CTR | No | Unique nonce | Not needed | None |
| GCM | No | Unique nonce | Not needed | **Yes** |

Note the last column: none of ECB, CBC and CTR prevents the message from
being changed on its own. That is why today's recommendation is a mode such
as **GCM** that does encryption and authentication together. The next
section, Authenticated Encryption, covers it.

## Summary

- A **mode** is how a block cipher ties the blocks of a long message
  together.
- **ECB** turns the same block into the same output and leaks the
  plaintext's pattern; it is not used.
- **CBC** chains each block to the previous one; it needs a random,
  unpredictable **IV** and padding.
- **CTR** turns a block cipher into a stream cipher; no padding, and the
  nonce is never repeated.
- None of them provides integrity on its own; today an **authenticated
  mode** (GCM) is used.
