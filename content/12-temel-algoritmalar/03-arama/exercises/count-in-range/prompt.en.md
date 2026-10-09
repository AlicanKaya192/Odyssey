In this exercise you use the `bisect` module.

1. `count_value(items, x)`: returns how many times `x` occurs in the sorted
   list.
2. `count_in_range(items, low, high)`: returns how many values in the sorted
   list satisfy `low <= value <= high`.

Both must be `O(log n)`: do not use `.count()` or a loop; take the difference
of two boundaries. Which boundary needs `bisect_left` and which
`bisect_right`? `low` and `high` themselves must be counted too.

**Expected output:**

```
3
0
6
0
```
