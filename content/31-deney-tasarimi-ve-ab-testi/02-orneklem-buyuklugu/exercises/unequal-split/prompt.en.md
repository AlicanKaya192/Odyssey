`split_sizes(d, share_b)` should return `[n_a, n_b, total]` for a test
where B's share is `share_b` (80% power, α = 0.05). `ratio = share_b /
(1 - share_b)`; `n_a` and `n_b` are rounded up. The starter code always
treats the split as 50/50.

**Expected output:**

```text
[6281, 6281, 12562]
[15700, 3925, 19625]
```
