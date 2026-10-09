Write the function `prefix_sums(values)`: it returns the prefix-sum list with
a leading `0` (`len(values) + 1` elements).

- `prefix_sums([3, 1, 4])` → `[0, 3, 4, 8]`

Do not use `itertools.accumulate` or `sum`; build it in one loop by adding to
the previous one.

**Expected output:**

```
[0, 3, 4, 8, 9, 14]
[0]
```
