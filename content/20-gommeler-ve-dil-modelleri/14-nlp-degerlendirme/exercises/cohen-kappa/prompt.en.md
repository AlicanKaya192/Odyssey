`cohen_kappa(a, b)` should compute the kappa of two label lists: `p_o` is the
share of equal labels, `p_e` the sum over labels of the product of their
shares in the two lists; kappa = `(p_o − p_e) / (1 − p_e)` (3 places). If
`p_e` is 1, return `1.0`.

**Expected output:**

```
0.429
1.0
```
