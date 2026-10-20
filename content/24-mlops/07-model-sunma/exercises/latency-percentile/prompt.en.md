Write the lesson's `percentile(values, p)` function with the nearest-rank method and add two edge cases:

- Sort the values; `rank = ceil(p / 100 * len(values))`; return element number `rank` of the sorted list (counting from 1).
- If `p` is 0, `rank` becomes 0: then return the first element.
- If the list is empty, return `None`.

**Expected output:**

```
p50: 13
p95: 90
p99: 250
empty: None
```
