# RSA

The Modular Arithmetic section ended with operations that are easy one way
and hard the other: multiplying two primes is easy, splitting the product
back into its primes is hard. **RSA** turns this difference into a **key
pair**: a **public key** given to everyone and a **private key** that
stays with its owner. A message encrypted with the public key is decrypted
only by the private key. In this section we build RSA step by step with
small, toy numbers.

## Building the key pair

1. Pick two primes: `p`, `q`.
2. The modulus: `n = p * q`. Part of the public key.
3. `phi = (p - 1) * (q - 1)`. Kept secret.
4. The public exponent `e`: a number whose gcd with `phi` is 1 (usually 65537).
5. The private exponent `d`: the inverse of `e` mod `phi`.

```python
import math

p, q = 61, 53
n = p * q
phi = (p - 1) * (q - 1)
e = 17
print(n, phi)
print(math.gcd(e, phi))
d = pow(e, -1, phi)
print(d)
print(e * d % phi)
```

```text
3233 3120
1
2753
1
```

The public key is `(e, n) = (17, 3233)`, the private key `(d, n) = (2753,
3233)`. `d` is the inverse from the Modular Arithmetic section: `e * d % phi
== 1`. Computing `phi` needs `p` and `q`; someone who knows `n` but not its
primes cannot find `d`.

## Encrypting and decrypting

The message must be a number smaller than `n`. Encryption is `c = m ** e
mod n`, decryption `m = c ** d mod n`.

```python
m = 65
c = pow(m, e, n)
print(c)
print(pow(c, d, n))
```

```text
2790
65
```

65 became 2790 when encrypted, and decrypting 2790 brought back 65. The
generalized form of Fermat's little theorem (Euler's theorem) explains why
this works: since `e * d` is 1 more than a multiple of `phi`, `m ** (e * d)
mod n` comes back to `m` itself.

## Turning text into a number

RSA works with numbers; text is first turned into bytes and the bytes into
a number. The number must be smaller than `n`, so in this example we use
slightly larger toy primes.

```python
p, q = 104723, 104729
n = p * q
phi = (p - 1) * (q - 1)
e = 65537
d = pow(e, -1, phi)

m = int.from_bytes(b"hi!", "big")
print(m, m < n)
c = pow(m, e, n)
back = pow(c, d, n)
print(back.to_bytes(3, "big"))
```

```text
6842657 True
b'hi!'
```

`int.from_bytes` turned the bytes into a single number, and after
decryption `to_bytes` turned it back. In real RSA `n` is 2048 bits or more;
our `n` is only 34 bits, and a number this small is easily split into its
primes. The toy numbers are only for seeing the steps.

## Why textbook RSA is not enough

One property of the "textbook" RSA so far creates a security problem: **the
same message always gives the same ciphertext.**

```python
c1 = pow(int.from_bytes(b"yes", "big"), e, n)
c2 = pow(int.from_bytes(b"yes", "big"), e, n)
c3 = pow(int.from_bytes(b"no", "big"), e, n)
print(c1 == c2)
print(c1 == c3)
```

```text
True
False
```

Since everyone has the public key, when the possible answers are few
("yes", "no") anyone can encrypt each one themselves and compare it with
the ciphertext. This is the public-key form of the ECB problem from the
Block Cipher Modes section. That is why real RSA adds **random padding** to
the message before encrypting: today's standard is **OAEP**. The padding
makes the same message give a different ciphertext every time.

## Where RSA is used in practice

RSA is slow and can only encrypt a message smaller than `n`. So it is not
used to encrypt large data directly:

<figure class="fig">
<div class="flow">
<span class="node">Random symmetric key</span>
<span class="arrow">→</span>
<span class="node acc">Encrypted with RSA</span>
<span class="arrow">→</span>
<span class="node">Data with AES-GCM</span>
<span class="arrow">→</span>
<span class="node ok">Receiver decrypts the key</span>
</div>
<figcaption>Hybrid encryption: RSA only carries the short symmetric key; authenticated encryption encrypts the data.</figcaption>
</figure>

RSA's second use is the **digital signature**: a message signed with the
private key can be verified by anyone with the public key. The Digital
Signatures section covers this. For key exchange, Diffie-Hellman and
elliptic curves are mostly used today (the next section).

## Summary

- In RSA the **public key** `(e, n)` is given to everyone; the **private
  key** `(d, n)` stays with its owner.
- `n = p * q`; `d` is the inverse of `e` mod `(p - 1)(q - 1)`.
- Encryption is `pow(m, e, n)`, decryption `pow(c, d, n)`; the message must
  be smaller than `n`.
- Security rests on how hard it is to split a big `n` into its primes; a
  real `n` is at least 2048 bits.
- Textbook RSA is deterministic; in practice **OAEP** padding and hybrid
  encryption are used.
