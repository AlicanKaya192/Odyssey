Build the same table with three different indexes and compare the room the
index takes.

**What to do:**

1. Build the table `df` with `make_orders(50_000)` (no file).
2. Prepare three tables: `df` (the default index), `df.set_index("order_id")`,
   `df.set_index("customer_id")`.
3. For each one, print on a line the name of the index's type
   (`type(t.index).__name__`) and the index's bytes
   (`t.memory_usage(deep=True)["Index"]`). Put the three tables in a list and
   loop over it.
4. On the last line print the total memory (index included) of the table
   indexed by `customer_id` in MB, rounded to one decimal.

**Expected output:**

```
RangeIndex 132
RangeIndex 132
Index 400000
4.8
```

Since `order_id` goes up regularly it became a `RangeIndex` again.
