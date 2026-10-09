Write the function `knapsack(items, capacity)` **with a DP table**: `items` are
`[value, weight]` pairs, each item at most once. It returns the largest total
value that can be taken without exceeding the capacity.

`best[i][w] = max(best[i − 1][w], best[i − 1][w − weight] + value)` (the
second only if the item fits).

There are 100 items on the last line: trying every subset is `2¹⁰⁰`, while
the table is only a few hundred thousand cells.

**Expected output:**

```
220
90
4428
```
