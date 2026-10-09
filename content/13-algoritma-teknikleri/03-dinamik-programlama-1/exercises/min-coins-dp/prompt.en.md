Write the function `min_coins(amount, coins)` **by filling a table**: it returns
the fewest coins needed to give the amount; `-1` if it cannot be given.

- `best = [0] + [inf] * amount`
- for each `a`, for each coin `c <= a`, update if `best[a − c] + 1` is smaller
- at the end, `-1` if `best[amount]` is still `inf`

**Expected output:**

```
2
4
-1
51
```
