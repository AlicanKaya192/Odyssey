`scale_with_train(values, split)` should scale the whole series but take the
mean and standard deviation **from the first `split` values only**
(`statistics.mean`, `statistics.pstdev`): `(v - mean) / std`. Return the
result with 3 places.

**Expected output:**

```
[-1.225, 0.0, 1.225, 2.449, 3.674]
```
