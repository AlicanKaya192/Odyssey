Write the function `pagerank_exact(M, d)`: solve the equation
`(I − d M) r = (1 − d) / n` with `np.linalg.solve`; return `r` with
`.round(3).tolist()`. No loops.

**Expected output:**

```
[0.388, 0.215, 0.397]
[0.359, 0.256, 0.385]
```
