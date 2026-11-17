`three_way(n, seed)` should shuffle the indices `0..n-1` with the seed and split
them 60% / 20% / 20% (with the boundaries `int(0.6 * n)` and
`int(0.8 * n)`) and return `[training, validation, test sizes, the number of
distinct indices in the three together]`. The last number should be `n`: the
sets are disjoint.

**Expected output:**

```
[1078, 359, 360, 1797]
```
