Write the function `cm_estimates(stream, queries, width, depth)`: build a
Count-Min table with `depth` rows and `width` columns; for each item in the
stream, increase column `h(item, row) % width` by one in every row (`row`).
Return the estimate for each query (the smallest of the counters across the
rows) as a list.

**Expected output:**

```
[56, 25, 5, 4]
```
