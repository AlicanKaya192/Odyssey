`two_by_two(k_a, n_a, k_b, n_b)` should test the 2×2 table
(`[[k_a, n_a - k_a], [k_b, n_b - k_b]]`) with chi-square and return
`[χ², p]` (3 and 4 places). The result should match the two-proportion
z-test, so **uncorrected** (`correction=False`). The starter code uses the
default Yates correction.

**Expected output:**

```text
[8.615, 0.0033]
[3.692, 0.0547]
```
