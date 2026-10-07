Find the number of different customers correctly with chunks and show how
far the wrong way goes off.

**What to do:**

1. Write the file of 200 000 orders.
2. Read only the `customer_id` column (`usecols`) in chunks of 50 000 rows.
3. Do two things in the same loop: collect the customers in a `set`, and add
   each chunk's `nunique()` result to a counter.
4. Print the number of customers in the set, the counter, and the counter's
   ratio to the set's size (two decimals), on separate lines.

**Expected output:**

```
49031
126247
2.57
```

The wrong way counted the same customer again and again in different
chunks.
