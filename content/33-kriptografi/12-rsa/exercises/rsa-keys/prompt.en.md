`rsa_keys(p, q, e)` should return `[n, d]`: `n = p * q`, `phi = (p - 1) *
(q - 1)`, `d = pow(e, -1, phi)`. The starter code computes `phi` wrongly;
`e * d % phi` does not come out as 1.

**Expected output:**

```
3233 2753
1
```
