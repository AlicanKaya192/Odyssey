`ppmi(counts)` should compute the PPMI matrix from a co-occurrence matrix (a
list of lists) and return it as a list of lists with 3 places. Row sums give
`P(w)`, column sums `P(c)`; cells never seen together (and negative PMI)
are 0.

**Expected output:**

```
[0.0, 0.624, 0.0]
[0.624, 0.0, 0.442]
[0.0, 0.442, 0.0]
```
