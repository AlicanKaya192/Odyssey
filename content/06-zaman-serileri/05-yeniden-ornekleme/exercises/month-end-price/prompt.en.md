`stock_price.csv` holds a stock's daily closing price. Turn it into
monthly figures; choosing the right operation is up to you.

**What to do:**

1. Read the file with a date index; take the `close` column into a series
   called `close`.
2. See the wrong way: print the **sum** of the prices of March 2024, rounded
   to two decimals.
3. Print the month-end close (`last`) and the monthly mean (`mean`) of March
   2024, rounded to two decimals, on one line.
4. From the `ohlc()` summary of March 2024 print the high and the low on one
   line (two decimals).
5. Print the percentage change of the March 2024 month-end close against the
   February 2024 month-end close, rounded to one decimal.

**Expected output:**

```
3221.24
166.33 153.39
167.73 140.99
19.3
```

The number in the first line corresponds to nothing: the stock never traded
at that price. pandas raised no error, because it does not know what the
value measures. A price shows a moment; you take the last value for the state
of the month and the mean for its typical level.
