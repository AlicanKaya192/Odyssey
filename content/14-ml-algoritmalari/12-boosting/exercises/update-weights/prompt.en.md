Write the function `update_weights(w, wrong, alpha)`: multiply the weight of
misclassified samples (`wrong[i]` True) by `e^α`, then normalise the weights so
they add up to 1. Return a `round(..., 4)` list.

**Expected output:**

```
[0.1667, 0.5, 0.1667, 0.1667]
```
