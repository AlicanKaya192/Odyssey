`split_sizes(n, train_fraction)` should split `n` examples into training and test
with `random_split` (seed 0): `int(n * train_fraction)` examples for training.
It should return `[training size, test size, shared count]`. For the shared count,
intersect the two parts' `indices` as sets.

**Expected output:**

```
[80, 20, 0]
[3, 4, 0]
```
