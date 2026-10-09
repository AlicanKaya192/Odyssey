Write the function `prefix_table(pattern)`: it returns KMP's prefix table.
`table[i]` is the length of the longest piece that is both a prefix and a
suffix of `pattern[:i + 1]` (not the piece itself).

`k` is the match length so far: on a mismatch step back with
`k = table[k - 1]`, on a match increase `k`.

**Expected output:**

```
[0, 0, 1, 0, 1, 2]
[0, 1, 0, 1, 2, 2, 3]
[0, 0, 0, 0]
```
