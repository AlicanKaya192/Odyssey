`objectness_loss(logits, target)` should return the binary cross-entropy
(`binary_cross_entropy_with_logits`, the mean over all cells) for the raw
objectness scores on the grid and the 0/1 target, rounded to 3 places.

**Expected output:**

```
0.127
0.693
```
