Write orders as JSON Lines, look inside the file, read it back and compare
its size with CSV.

**What to do:**

1. Write the table `small = make_orders(4)[["order_id", "quantity"]]`
   to `orders.jsonl` as JSON Lines (`orient="records", lines=True`).
2. Read the file with `open`; print the number of lines and the first line.
3. Read the file back with `pd.read_json(..., lines=True)`; print the number
   of rows and columns (`shape`) and the total of `quantity` on one line.
4. Write the table `big = make_orders(50_000)` as both `big.jsonl` and
   `big.csv` (`index=False`); print the ratio of the JSON size to the CSV
   size, rounded to two decimals.

**Expected output:**

```
4
{"order_id":1,"quantity":2}
(4, 2) 15
2.61
```
