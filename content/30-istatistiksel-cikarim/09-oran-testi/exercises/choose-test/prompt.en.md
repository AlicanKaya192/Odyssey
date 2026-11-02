`choose_test(k_a, n_a, k_b, n_b)` should first look at the expected counts
under H₀: with the pooled proportion `pool`, `n_a * pool`,
`n_a * (1 - pool)`, `n_b * pool`, `n_b * (1 - pool)`. If any is below 5
return `["fisher", p]`, otherwise use the z-test
(`proportions_ztest([k_b, k_a], [n_b, n_a])`) and return `["z", p]` (p with
4 places). The starter code always runs the z-test.

**Expected output:**

```text
['z', 0.0033]
['z', 0.0186]
```
