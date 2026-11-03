Public-key cryptography rests on mathematical operations that are easy in
one direction and very hard in the other. The tools of this section give
the "easy" direction.

## Easy direction, hard direction

| Easy | Hard (no known fast way) | Where |
|---|---|---|
| Multiplying two big primes: `p * q` | Finding `p` and `q` from the product (factoring) | RSA |
| Computing `pow(g, x, p)` | Finding `x` from the result (discrete logarithm) | Diffie-Hellman |
| Adding a point on a curve to itself `k` times | Finding `k` from the result | Elliptic curves |

The hardness of the hard direction comes from the **size** of the numbers.
With the small toy numbers of these lessons everything can be found even
by hand; in real systems the numbers have hundreds of digits.

## Sizes in real systems

| System | Typical size |
|---|---|
| RSA modulus `n` | At least 2048 bits (about 617 digits) |
| Diffie-Hellman prime `p` | At least 2048 bits |
| Elliptic curve | 256 bits (e.g. P-256, X25519) |
| Symmetric key | 128 or 256 bits |

Elliptic curves give the same security with much smaller numbers; that is
why curves are mostly used for key exchange today.

## Warning

The code in this section is for seeing the mathematics. Real public-key
cryptography needs many details besides big numbers, such as padding,
randomness and timing; it is done with a well-tested library.
