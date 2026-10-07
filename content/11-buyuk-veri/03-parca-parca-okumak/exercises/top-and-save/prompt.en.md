Do two jobs with chunks: find the three orders with the highest revenue,
and write the orders whose revenue is over 20 000 lira to a separate file.

**What to do:**

1. Write the file of 200 000 orders.
2. Read it in chunks of 50 000 rows. In each chunk add the column
   `revenue = quantity * unit_price`.
3. Put each chunk's `nlargest(3, "revenue")` result in a list.
4. In the same loop write the rows with `revenue >= 20_000` to `large.csv`
   by **appending**: for the first chunk `mode="w"` with a header, for the
   rest `mode="a"` without one, `index=False`.
5. After the loop join the list and take `nlargest(3, "revenue")` again;
   print `order_id` and the revenue (two decimals) on each line.
6. Read `large.csv`; print its number of rows and its smallest revenue (two
   decimals) on one line.

**Expected output:**

```
77834 37969.65
64034 37358.2
181799 35445.5
284 20058.12
```

The smallest revenue in the file is above 20 000: the filter worked.
