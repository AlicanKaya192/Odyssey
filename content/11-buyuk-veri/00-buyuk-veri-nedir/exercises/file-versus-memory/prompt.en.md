`orders_data.py` (the read-only tab) produces orders. Write 100 000 orders
to a CSV, read it back and compare the two sizes.

**What to do:**

1. Write the file with `write_orders_csv("orders.csv", 100_000)`.
2. Read it into a table `df` with `pd.read_csv`.
3. Print the number of rows.
4. Print the file's size on disk (`os.path.getsize`) and the table's size in
   memory (`memory_usage(deep=True).sum()`) in MB, rounded to one decimal,
   on one line.
5. Print the ratio of the size in memory to the file size, rounded to two
   decimals.
6. Print the name of the column that takes the most memory. The result of
   `memory_usage` also has a row for the index itself (`"Index"`); remove it
   first with `.drop("Index")`, then use `.idxmax()`.

**Expected output:**

```
100000
5.9 9.6
1.62
order_time
```

The most expensive column is a text column. The next section looks at it
column by column.
