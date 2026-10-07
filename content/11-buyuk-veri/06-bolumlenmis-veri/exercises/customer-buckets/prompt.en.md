Split the orders into four buckets by customer number; find one customer's
orders by reading only one bucket.

**What to do:**

1. Build the table `df` with `make_orders(200_000)`.
2. Add the column `bucket = customer_id % 4`; write each bucket as
   `buckets/bucket=<n>/part-0.parquet` (with the `bucket` column dropped,
   `index=False`).
3. For `customer = 1234` work out the bucket number and print it.
4. Read only that bucket's file; print the number of rows in the file.
5. Print the number of orders of this customer in the table you read.
6. Find the same number by filtering `df` directly, and print whether the
   two numbers are equal.

**Expected output:**

```
2
50183
7
True
```

Only one of the four files was read, and the result is right.
