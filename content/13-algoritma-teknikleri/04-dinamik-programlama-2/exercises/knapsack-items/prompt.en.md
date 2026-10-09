Write the function `best_items(items, capacity)`: build the knapsack table and
return **the indexes of the taken items** as a list from smallest to
largest.

Recovering: `w = capacity`, take `i` from `n` down to 1; if `best[i][w]`
differs from the row above, `i − 1` was taken and `w` drops by its weight.

**Expected output:**

```
[1, 2]
[1, 3]
```
