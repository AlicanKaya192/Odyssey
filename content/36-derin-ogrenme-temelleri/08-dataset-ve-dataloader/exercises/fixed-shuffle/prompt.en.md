`first_batch(seed)` gives the first shuffled batch, but the order changes on every
run; that is why the last line usually prints `False`. Fix the shuffling with
`seed`.

**Expected output:**

```
[5, 3, 1, 7]
True
```
