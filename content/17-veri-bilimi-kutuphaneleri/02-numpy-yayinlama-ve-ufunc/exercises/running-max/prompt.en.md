`running_max(values)` should give, at each position, the largest value so
far (`[3, 1, 4]` → `[3, 3, 4]`). Loops are forbidden: use a ufunc's
`accumulate` method.

**Expected output:**

```
[3, 3, 4, 4, 5, 9, 9, 9]
```
