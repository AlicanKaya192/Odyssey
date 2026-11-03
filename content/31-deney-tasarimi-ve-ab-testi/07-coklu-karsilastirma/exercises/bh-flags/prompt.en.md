`bh_flags(p_values, q=0.05)` should return the Benjamini–Hochberg decisions
in the original order: all up to the **largest** k whose k-th sorted p ≤
k · q / m are accepted. The starter code stops at the first failure.

**Expected output:**

```text
[True, True, True, False]
```
