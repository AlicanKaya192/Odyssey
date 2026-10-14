`summary(log)` should take a list whose every entry is
`{"tokens": ..., "cost": ...}` and return `[number of calls, total tokens,
total cost]`; the cost a `float` rounded to 6 places.

**Expected output:**

```
[2, 240, 0.00016]
```
