`stock_price.csv` holds a stock's daily closing price. Compute the
total return of the three years in three ways; one of them is wrong.

**What to do:**

1. Read the file with a date index; take the `close` column into a series
   called `close`.
2. Compute the daily simple return: `r = close.pct_change()`.
3. The **true** total return: from the ratio of the last price to the first,
   as a percentage with one decimal.
4. The **wrong** way: the sum of the daily returns (`r.sum()`), as a
   percentage with one decimal.
5. The **right** way: from the last value of the series `(1 + r).cumprod()`,
   as a percentage with one decimal.
6. Compute the logarithmic returns (`np.log(close).diff()`), add them up,
   turn the total into a percentage with `np.exp(total) - 1` and print it
   (one decimal).
7. Print the date (`"%Y-%m-%d"`) and the percentage value (two decimals) of
   the highest daily return on one line.

**Expected output:**

```
66.1
62.3
66.1
66.1
2023-03-02 5.3
```

Three of the four numbers are the same; the odd one out adds percentages up.
Returns build up by multiplying; if you want a measure that can be added,
use logarithmic returns.
