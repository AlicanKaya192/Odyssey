`restock(cities, stock, amount)` should set the stock of rows with zero stock
to `amount` and return the stock list. The starter code uses chained
assignment (`df[...]["stock"] = ...`); in pandas 3 this does **not** change
the original table. Write it in one step: `df.loc[condition, "stock"] =
amount`.

**Expected output:**

```
[5, 10, 10]
```
