Summarise the monthly revenue by payment method with DuckDB and work out
the shares with pandas.

**What to do:**

1. The starter code writes 200 000 orders as `orders.parquet`.
2. With DuckDB find the revenue (the total of `quantity * unit_price`) per
   month (`strftime(order_time, '%Y-%m')`) and payment method, and take it
   into pandas with `.df()`.
3. Build a month × payment method table with `pivot`; work out the shares
   within each month as percentages.
4. For the first three months print the month and the share of card (`card`)
   (one decimal).
5. On the last line print the twelve-month mean of the share of cash
   (`cash`) (one decimal).

**Expected output:**

```
2024-01 71.5
2024-02 72.7
2024-03 71.1
8.1
```
