`candidates(signatures, bands, rows)` should split each signature into `bands`
bands (each band `rows` numbers). Two signatures whose band with the same
number is exactly equal become a candidate pair. Return the candidate pairs
as `[i, j]` (`i < j`), unique and sorted.

**Expected output:**

```
[[0, 1], [0, 2]]
[]
```
