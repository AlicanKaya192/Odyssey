Write the function `min_capacity(weights, days)` with **binary search on the
answer**: the boxes are loaded in order, and a day's total load cannot exceed
the capacity. It returns the smallest capacity needed to finish in `days`
days.

Write the helper `days_needed` too. The search range is `max(weights)` to
`sum(weights)`. On the two hundred thousand boxes on the last line, trying the
candidates one by one runs out of time.

**Expected output:**

```
13
15
1001394
```
