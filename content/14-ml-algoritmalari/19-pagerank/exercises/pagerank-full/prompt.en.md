Write the function `pagerank(links, d=0.85, tol=1e-10)` (`links[j]`: `j`'s
links): build the transition matrix (a dangling page's column is `1 / n`),
start from `1 / n` and repeat the step until `Σ abs(new − old) < tol`. Return
`(ranks round(3) list, the number of steps)`; the step count is the number of
updates.

**Expected output:**

```
[0.373, 0.196, 0.394, 0.038]
47
```
