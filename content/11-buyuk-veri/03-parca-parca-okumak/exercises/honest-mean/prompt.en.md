Work out the mean order quantity with chunks in two ways: the mean of
means, and total / count.

**What to do:**

1. Write the file of 200 000 orders.
2. Read it in chunks of 70 000 rows (the chunks will be 70 000, 70 000 and
   60 000 rows).
3. In each chunk add the mean of `quantity` to a list; in the same loop
   accumulate the total of `quantity` and the number of rows.
4. Print the mean of means and total / count, rounded to four decimals, on
   separate lines.
5. Print the mean of `quantity` over the whole file (four decimals).

**Expected output:**

```
2.2198
2.2196
2.2196
```

Total / count matches the all-at-once value exactly; the mean of means
drifts.
