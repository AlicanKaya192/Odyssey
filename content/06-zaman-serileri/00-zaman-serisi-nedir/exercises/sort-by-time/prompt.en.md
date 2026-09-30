Sales records arrived from a system **in scrambled order**:
`sales_shuffled.csv`. The first job is to fix the order.

The dates are written like `2022-01-01` (ISO 8601). This format falls into
calendar order even when sorted as text, so `sort_values("date")` works
correctly here.

**What to do:**

1. Read `sales_shuffled.csv`.
2. Sort by date and renumber the index from zero
   (`reset_index(drop=True)`).
3. Print the first date, the last date, the number of rows and the first
   three days' sales as a list, one per line.

**Expected output:**

```
2022-01-01
2024-12-31
1096
[305, 277, 201]
```

Why `reset_index(drop=True)`: sorting moves the rows but they carry their
old index numbers with them. `iloc[0]` looks at position, so it would still
work, but leaving a sorted table with its old numbers causes confusion later
when you use `loc`.
