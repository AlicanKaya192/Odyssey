`lost_share(n, seed, S)` should return, for the scenes of
`make_scenes(n, size=32, seed=seed)`, the share of objects lost because they
share a cell, out of all objects, rounded to 3 places.

**Expected output:**

```
2 0.164
4 0.073
8 0.015
```
