Work out the number of orders and the revenue per payment type two ways: with
partial totals from row groups and with DuckDB.

**What to do:**

1. `orders.parquet` is ready (500 000 rows, row groups of 100 000).
2. Read every row group (`read_row_group`, only `payment`, `quantity`,
   `unit_price`); produce partial counts and revenue per payment type and
   combine them in the `counts` and `revenue` dictionaries.
3. Print the payment types in alphabetical order, with the type, the count
   and the revenue (two decimals) on each line.
4. Work out the same numbers from the file with DuckDB; print whether the
   counts match exactly and the revenues within less than 0.01.

**Expected output:**

```
card 359248 589500728.87
cash 40550 66462584.76
transfer 100202 164306286.55
True
```
