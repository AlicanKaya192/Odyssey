`last_real_steps(out, lengths)`: `out` is the `(B, T, H)` output of every
step, `lengths` the real length of each sequence. Return the output of each
sequence's last real step as a `(B, H)` list. Instead of a loop you can use
indexing with two indices.

**Expected output:**

```
[[3, 3], [5, 5]]
[[1, 1], [4, 4]]
```
