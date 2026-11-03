# Diffie-Hellman and Elliptic Curves

In the RSA section we saw how to encrypt a symmetric key with a public key
and send it. There is another way: two sides can reach the same secret over
a line anyone can listen to **without sending any key at all**. This idea
is called **key exchange**, and its first method is **Diffie-Hellman**.
Today the same idea is mostly applied on **elliptic curves**.

## Diffie-Hellman: the paint-mixing analogy

Ada and Can agree on a color everyone knows. Each picks a secret color,
mixes it into the common color, and sends the mixture openly. Then each
adds **their own secret color to the mixture that came from the other
side**. Both end up with the mixture of the same three colors; someone
listening on the line sees only the two intermediate mixtures, and
separating colors from a mixture is hard. In mathematics "mixing" is
`pow(g, secret, p)`, and "the hardness of separating" is the **discrete
logarithm** problem (the one-way operations of the Modular Arithmetic
section).

```python
p, g = 23, 5
ada_secret, can_secret = 6, 15

ada_public = pow(g, ada_secret, p)
can_public = pow(g, can_secret, p)
print(ada_public, can_public)

ada_shared = pow(can_public, ada_secret, p)
can_shared = pow(ada_public, can_secret, p)
print(ada_shared, can_shared)
```

```text
8 19
2 2
```

Only `p`, `g`, 8 and 19 travel in the clear. Both sides reached 2, because
`(g ** a) ** b` and `(g ** b) ** a` are the same number. The secret numbers
(6 and 15) were never sent.

## From the shared secret to a key

The shared secret is not used directly as a key: it is a number whose
length varies. As in the Key Derivation section, it goes through a KDF.
To save space we use a single SHA-256 here; in practice, HKDF.

```python
import hashlib

p, g = 4294967291, 5
ada_secret, can_secret = 1234567, 7654321
ada_public = pow(g, ada_secret, p)
can_public = pow(g, can_secret, p)

ada_shared = pow(can_public, ada_secret, p)
can_shared = pow(ada_public, can_secret, p)
key = hashlib.sha256(ada_shared.to_bytes(4, "big")).digest()
print(ada_shared == can_shared)
print(len(key))
print(1 < ada_public < p - 1, 1 < can_public < p - 1)
```

```text
True
32
True True
```

Both sides reached the same 32-byte key. The last line is a **defensive
check**: if the public value from the other side is a number such as `1` or
`p - 1`, the shared secret falls to predictable values; so an incoming value
is checked to be in `1 < value < p - 1` before it is used. In real systems
the secret numbers are made at random with `secrets`, and `p` is at least
2048 bits.

## What Diffie-Hellman does not provide

Diffie-Hellman lets the two sides reach **the same secret**, but it does not
verify **who** the other side is. If Ada does not know that the number she
takes for Can's public value really came from Can, someone in the middle
can run a separate key exchange with each side. That is why public values
are **signed**, and the signer's identity is bound with a **certificate**:
the Digital Signatures section and the Certificates and PKI section cover
this. In The TLS Handshake section we will see how the parts fit together.

The second important idea is **forward secrecy**: if new secret numbers are
made for every session and deleted when the work is done, then even if
long-lived keys are stolen one day, the keys of old sessions cannot be
computed again.

## Elliptic curves

An elliptic curve is the set of points satisfying `y² = x³ + a·x + b`. In
cryptography this equation is solved mod a prime, which gives a finite
number of points. An **addition** is defined between these points: the line
through two points cuts the curve at a third point, and its reflection is
the sum. The formulas mod a prime are:

```python
P, A, B = 97, 1, 4


def on_curve(pt):
    if pt is None:
        return True
    x, y = pt
    return (y * y - (x ** 3 + A * x + B)) % P == 0


def add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if p1 == p2:
        s = (3 * x1 * x1 + A) * pow(2 * y1, -1, P) % P
    else:
        s = (y2 - y1) * pow(x2 - x1, -1, P) % P
    x3 = (s * s - x1 - x2) % P
    y3 = (s * (x1 - x3) - y1) % P
    return (x3, y3)


G = (0, 2)
print(on_curve(G))
print(add(G, G), on_curve(add(G, G)))
print(add(G, (0, 95)))
```

```text
True
(91, 48) True
None
```

`(0, 2)` is on the curve, and its sum with itself is also a point on the
curve. `(0, 95)` is the inverse of `(0, 2)` (`95 = -2` mod 97): their sum is
"the point at infinity", the zero of the addition; `None` in the code. The
**inverse** from the Modular Arithmetic section is used instead of
division. This toy curve has 89 points including the point at
infinity; since that number is prime, adding `G` to itself again and again
visits every point.

## Elliptic-curve Diffie-Hellman

Adding a point to itself `k` times (`k·G`) is easy: it is the points'
version of square and multiply from the Modular Arithmetic section,
**double and add**. Finding `k` from the resulting point is hard.
Diffie-Hellman moves over directly: `secret·G` instead of `pow(g, secret,
p)`.

```python
def mul(k, pt):
    result = None
    while k > 0:
        if k & 1:
            result = add(result, pt)
        pt = add(pt, pt)
        k >>= 1
    return result


ada_secret, can_secret = 13, 29
ada_public = mul(ada_secret, G)
can_public = mul(can_secret, G)
print(ada_public, can_public)
print(mul(ada_secret, can_public) == mul(can_secret, ada_public))
print(mul(ada_secret, can_public))
```

```text
(41, 75) (31, 12)
True
(48, 8)
```

Both sides reached the same point; its `x` coordinate is the shared secret
that goes into the KDF. Real curves (X25519, P-256) are defined over a
256-bit prime and give roughly the same security as 2048-bit
Diffie-Hellman with much smaller numbers. The curve over 97 in this lesson
is only for seeing the formulas.

## Summary

- **Diffie-Hellman** brings two sides to the same secret without sending a
  key: `pow(their_public, my_secret, p)`.
- Its security rests on the hardness of the **discrete logarithm** problem.
- The shared secret goes through a **KDF** to become a key; an incoming
  public value is checked first.
- DH does **not authenticate** the other side: public values are signed and
  identity is bound with a certificate.
- **Elliptic-curve DH** applies the same idea with point addition and much
  smaller keys (X25519, P-256).
