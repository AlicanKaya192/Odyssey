`f_and_eta(groups)` should compute the F statistic and η² by hand for groups
given as a list of lists: `[F, eta]` (3 places). In F the sums of squares
are divided by their degrees of freedom: between groups by `k - 1`, within
groups by `n - k`. `f_oneway` is not allowed. The starter code forgot to
divide.

**Expected output:**

```text
[13.0, 0.812]
```
