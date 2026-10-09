Write the function `minhash_similarity(a, b, size)`: build the two sets'
MinHash signatures of length `size` (for each `s = 0..size − 1`,
`min(h(x, s) for x in set)`), and return the share of positions where the
signatures are equal, `round(..., 3)`.

**Expected output:**

```
0.625
1.0
```
