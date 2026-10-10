`store_share(stores, sales)` should return each sale's share of **its own
store's** total sales as a list rounded to 3 places. Spread the group total
back to the rows with `groupby(...).transform("sum")`; no `merge` or loop
needed. **Do not write a loop.**

**Expected output:**

```
[0.1, 1.0, 0.3, 0.6]
```
