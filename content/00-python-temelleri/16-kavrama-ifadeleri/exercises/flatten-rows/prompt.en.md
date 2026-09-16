You will flatten a nested list and add it up.

The data you have:

```python
rows = [[3, -1, 4], [0, 5], [-2, 8, 1]]
```

**What to do:**

1. `flat` — every number in a single list (with a nested comprehension).
2. `positives` — only the numbers **above zero**, again in one list.
3. `total` — the sum of every number. Do not build a list here: put a
   **generator expression** inside `sum()` (no square brackets).

Then print all three in order.

**Expected output:**

```
[3, -1, 4, 0, 5, -2, 8, 1]
[3, 4, 5, 8, 1]
18
```

> The two `for` clauses are written side by side: the outer list first,
> then the inner one.
