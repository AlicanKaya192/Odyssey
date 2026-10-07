Work out the total quantity per payment method with dask and check it with
pandas.

**What to do:**

1. The starter code writes the four CSV files.
2. Read them with `dd.read_csv("orders-*.csv")`; build the recipe
   `groupby("payment")["quantity"].sum()` and work it out with `compute()`.
3. Sort the result by name and print the payment method and the total on each
   line.
4. Work out the same result with pandas from the `orders` table and print
   whether the two results are the same (`.equals`, both sorted by name).

**Expected output:**

```
card 319710
cash 35594
transfer 88622
True
```
