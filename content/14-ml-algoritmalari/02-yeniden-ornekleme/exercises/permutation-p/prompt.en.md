Write the function `permutation_p(a, b, rounds, seed)`: the real statistic is
the absolute difference of the two groups' means.
`rng = np.random.default_rng(seed)`; `rounds` times shuffle the combined data
with `rng.permutation`, count the first `len(a)` as a and the rest as b, and
compute the difference. The p-value is
`(those at least as large as the real one + 1) / (rounds + 1)`,
`round(..., 4)`.

**Expected output:**

```
0.022
1.0
```
