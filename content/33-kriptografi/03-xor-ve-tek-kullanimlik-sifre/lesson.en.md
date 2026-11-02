# XOR and the One-Time Pad

The Breaking Classical Ciphers section ended with a goal: the ciphertext
must be indistinguishable from random for someone who does not know the
key. There is a method that reaches this goal **exactly**: the **one-time
pad** (OTP), and in a mathematically proven way. But only if all four of
its conditions are met. This section covers that method, the **XOR**
operation beneath it, and what happens when one of the conditions is
broken.

## XOR

**XOR** (exclusive or) compares two bits: 1 if they differ, 0 if they are
the same. In Python its sign is `^`. For numbers each bit is XORed
separately:

| a | b | a ^ b |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

```python
a, b = 0b1100, 0b1010
print(f"{a:04b} ^ {b:04b} = {a ^ b:04b}")
print(a ^ b ^ b == a, a ^ a, a ^ 0)
```

```text
1100 ^ 1010 = 0110
True 0 12
```

The three properties on the second line carry this whole section:

- `a ^ b ^ b == a`: XORing twice with the same value brings it back.
  Encryption and decryption are **the same operation**.
- `a ^ a == 0`: something XORed with itself disappears.
- `a ^ 0 == a`: XOR with zero changes nothing.

## The one-time pad

Each byte of the message is XORed with the byte of the key at the same
position. The key is as long as the message and completely random:

```python
def xor_bytes(data, key):
    return bytes(d ^ k for d, k in zip(data, key))


message = b"PAY BOB 100"
key = bytes.fromhex("3a91c47e0b5d22f6a8137e")
cipher = xor_bytes(message, key)
print(cipher.hex())
print(xor_bytes(cipher, key))
```

```text
6ad09d5e491260d699234e
b'PAY BOB 100'
```

In the example we wrote the key as a constant so that the output is the
same on every run. In reality the key is made with
`secrets.token_bytes(len(message))` (the Randomness section). `bytes.hex()`
turns bytes into hex text and `bytes.fromhex` turns it back.

## Why can it not be broken?

While breaking classical ciphers we asked every time "is this solution
meaningful?". With the one-time pad that question is useless, because the
same ciphertext can be decrypted to **every message of the same length**
with a suitable key:

```python
other = b"PAY EVE 900"
fake_key = xor_bytes(cipher, other)
print(xor_bytes(cipher, fake_key))
```

```text
b'PAY EVE 900'
```

Even if the attacker tries every key, they find `PAY BOB 100`, and
`PAY EVE 900`, and every sentence of the same length, and cannot tell which
is right. Shannon, the founder of information theory, proved this in 1949
and called it **perfect secrecy**: the ciphertext says nothing about the
message **except its length**.

## Four conditions

The proof holds only if all of these conditions hold:

1. The key must be **truly random**.
2. The key must be at least **as long as the message**.
3. The key must be used **only once**.
4. The key must stay **secret**.

These conditions make the one-time pad almost unusable in practice: to send
1 GB of data you first have to get a 1 GB key to the other side safely. If
you can get that key there safely, you could have sent the message the same
way. Still, modern **stream ciphers** use the same idea: they make a long,
random-looking stream from a short key and XOR it with the message. We will
see this in the Symmetric Encryption section.

## If condition 3 is broken: reusing the key

If two messages are encrypted with the same key, XORing the two ciphertexts
**cancels** the key (`k ^ k = 0`) and leaves the XOR of the two messages:

```python
m1 = b"ATTACK AT DAWN"
m2 = b"RETREAT AT TEN"
key = bytes.fromhex("5f0e2b9ac4d17733e1a6082cb94d")
c1 = xor_bytes(m1, key)
c2 = xor_bytes(m2, key)

leak = xor_bytes(c1, c2)
print(leak == xor_bytes(m1, m2))
print(xor_bytes(leak, m1))
```

```text
True
b'RETREAT AT TEN'
```

The attacker never saw the key. Yet the moment they knew (or guessed) the
first message, they read the second. Even without knowing the first
message, the XOR of two plaintexts carries enough traces to be solved with
the statistical methods of the Breaking Classical Ciphers section. In the
1940s a state reusing pages of its one-time pads let the other side read
thousands of its messages years later.

This mistake still happens today: in stream ciphers, using the same key and
the same starting value (nonce) twice leads to exactly this (the Common
Cryptography Mistakes section).

## Confidentiality is not integrity

The one-time pad hides the message but **does not stop it being changed**.
If the attacker knows the message's format, they can change the ciphertext
as they like without knowing the key. Flipping a bit flips the same bit in
the plaintext:

```python
cipher = xor_bytes(b"PAY BOB 100", key)
patch = xor_bytes(b"PAY BOB 100", b"PAY BOB 900")
tampered = xor_bytes(cipher, patch)
print(xor_bytes(tampered, key))
```

```text
b'PAY BOB 900'
```

The attacker only used the knowledge "this message is `PAY BOB 100`"; they
never saw the key, and the receiver got a perfectly decrypted message
asking to pay 900. This is called **malleability**. The fix is to put an
integrity check next to the encryption: HMAC (the Message Authentication:
HMAC section) or
authenticated encryption, which does both (the Authenticated Encryption
section). Remember the table in the What Is Cryptography? section:
confidentiality and integrity are separate goals and need separate tools.

## Summary

- **XOR** gives 1 for differing bits; `a ^ b ^ b == a`, so encryption and
  decryption are the same operation.
- **One-time pad:** the message is XORed with a random key as long as the
  message. By Shannon it gives **perfect secrecy**: the same ciphertext
  decrypts to every message of the same length.
- Four conditions: truly random, as long as the message, **used once**,
  secret. In practice carrying the key is as hard as carrying the message.
- If the key is reused, `c1 ^ c2 = m1 ^ m2`: a leak without the key.
- Encryption does not give integrity: XORed text can be changed bit by bit.
