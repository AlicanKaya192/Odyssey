`set_seed(seed)` should fix the `random`, `numpy` and `torch` seeds.
`same_seed` is ready: it builds two layers with two seeds and compares their
weights.

**Expected output:**

```
True False
```
