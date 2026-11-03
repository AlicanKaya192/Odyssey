## Diffie-Hellman steps

| Step | Ada | In the clear | Can |
|---|---|---|---|
| Common values | | `p`, `g` | |
| Secret number | `a` | | `b` |
| Public value | `A = pow(g, a, p)` | `A`, `B` | `B = pow(g, b, p)` |
| Shared secret | `pow(B, a, p)` | | `pow(A, b, p)` |

The two shared secrets are the same: `g ** (a·b) mod p`. A listener sees
`p`, `g`, `A`, `B`; finding `a` or `b` is the discrete logarithm problem.

## Elliptic-curve DH

| | DH with numbers | DH with a curve |
|---|---|---|
| Common value | `g`, `p` | Point `G`, the curve |
| Public value | `pow(g, a, p)` | `a·G` (double and add) |
| Shared secret | `pow(B, a, p)` | The `x` of the point `a·(b·G)` |
| Hard problem | Discrete logarithm | Discrete logarithm on the curve |
| Typical size | 2048+ bits | 256 bits (X25519, P-256) |

## Point addition (mod `p`)

- Different points: `s = (y2 - y1) / (x2 - x1)`.
- The same point (doubling): `s = (3·x1² + a) / (2·y1)`.
- `x3 = s² - x1 - x2`, `y3 = s·(x1 - x3) - y1`.
- "Division" = multiplying by the inverse: `pow(denominator, -1, p)`.
- `(x, y) + (x, -y)` = the point at infinity (the zero of the addition).

## Rules

- The shared secret is not used as a key without going through a **KDF**
  (HKDF).
- An incoming public value is **checked**: `1 < A < p - 1` for DH with
  numbers, and that the point lies on the curve for a curve.
- Secret numbers are made again with `secrets` for every session and thrown
  away when done (**forward secrecy**).
- DH does not authenticate; public values are signed.
