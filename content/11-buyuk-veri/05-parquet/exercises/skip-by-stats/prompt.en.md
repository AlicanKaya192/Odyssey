Find only the March 2024 orders by reading just the row groups you need.

**What to do:**

1. The starter code writes 200 000 orders in groups of 20 000 rows
   (10 groups).
2. Define `start = pd.Timestamp("2024-03-01")` and
   `end = pd.Timestamp("2024-04-01")`.
3. Choose the groups that **could** contain March orders: those whose
   largest time is **not** smaller than `start` and whose smallest time is
   smaller than `end`. Print the chosen group numbers as a list.
4. Read only those groups with `read_row_group` and join them; print the
   number of rows read.
5. Filter what was read with `start <= order_time < end`; print the number of
   March orders.

**Expected output:**

```
[1, 2]
40000
16591
```

Only some of the ten groups were read; the rest were recognised from the
statistics and skipped.
