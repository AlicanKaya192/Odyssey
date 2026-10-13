`mean_reciprocal_rank(rankings, relevant)` should find, for each query, the
rank of the first right item in the ranking (starting at 1) and return the
mean of the `1 / rank` values with 3 places. If there is no right item, that
query counts as 0.

**Expected output:**

```
0.5
0.75
```
