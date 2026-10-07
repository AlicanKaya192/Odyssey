Work out the revenue per payment method with chunks and compare it with the
all-at-once result.

**What to do:**

1. Write the file of 200 000 orders.
2. Read it in chunks of 50 000 rows. In each chunk add the column
   `revenue = quantity * unit_price` and put the result of
   `groupby("payment")["revenue"].sum()` in a list.
3. Combine the chunk results with `pd.concat(...).groupby(level=0).sum()`.
4. Sort from largest to smallest and print on each line the payment method
   and the revenue in millions of lira (`/ 1e6`, two decimals).
5. Read the file once more in full, do the same calculation, and print
   whether the two results are the same to two decimals (`True` / `False`).

**Expected output:**

```
card 235.58
transfer 65.32
cash 26.53
True
```
