Write the function `count_groups(n, pairs)` with **union-find**: items
`0`..`n − 1`, `pairs` are `[a, b]` links. It returns how many separate groups
remain.

Fill in `find`; then for each pair, if the roots differ put one under the other
and decrease `groups` by one.

**Expected output:**

```
2
4
3
```
