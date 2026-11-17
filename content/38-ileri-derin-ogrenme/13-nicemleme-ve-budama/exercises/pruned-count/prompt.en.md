`pruned_count(amount)` should apply pruning at the rate `amount` to the ready
layer with `prune.l1_unstructured` and return the number of zeros in the
weight.

**Expected output:**

```
50
30
```
