Write the function `mf_step(r, p, q, lr, reg)` (no biases): `err = r − p·q`;
`p_new = p + lr (err q − reg p)`, `q_new = q + lr (err p − reg q)` (both with
the **old** `p` and `q`). Return the lists `(p_new, q_new)` with
`round(..., 4)`.

**Expected output:**

```
[0.2192, 0.1591]
[0.3384, -0.0197]
```
