Write the function `apply_updates(n, updates)` **with a difference array**:
picture a list of `n` daily counters, all 0 at first. `updates` is a list of
`[lo, hi, amount]` triples; each adds `amount` to every day from `lo` to `hi`
(**both included**). Return the list after all the updates.

Do not apply each update to every day of the range one by one:
`diff[lo] += amount`, `diff[hi + 1] -= amount`, and one prefix sum at the end.

**Expected output:**

```
[5, 8, 8, 2, 2, -1]
[0, 0, 0]
```
