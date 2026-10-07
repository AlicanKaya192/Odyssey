Read files partitioned by payment method; rebuild the payment column from
the folder names.

**What to do:**

1. The starter code writes 100 000 orders in the
   `orders/payment=<method>/part-0.parquet` layout; there is no `payment`
   column inside the files.
2. Loop over the files in order with `Path("orders").glob("payment=*/*.parquet")`.
3. Read each file; take the payment method from the folder name
   (`f.parent.name.split("=")[1]`) and add it to the table as the `payment`
   column.
4. Join the pieces; print the number of rows per payment method on each line,
   sorted by name.
5. On the last line print the total number of rows.

**Expected output:**

```
card 72243
cash 7872
transfer 19885
100000
```
