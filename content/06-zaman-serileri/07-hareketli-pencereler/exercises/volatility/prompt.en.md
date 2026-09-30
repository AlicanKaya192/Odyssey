`stock_price.csv` holds a stock's closing price. Measure how volatile the
price is and whether it runs above or below its long-term average.

**What to do:**

1. Read the file with a date index; compute the `close` series and the daily
   return (`pct_change()`).
2. Compute the 20-day rolling volatility as an annualised percentage:
   `r.rolling(20).std() * (252 ** 0.5) * 100`.
3. Print the mean of the volatility, rounded to one decimal.
4. Print the date (`"%Y-%m-%d"`) and value (one decimal) of the highest
   volatility on one line; then the same for the lowest volatility.
5. Compute the 100-day moving average (`close.rolling(100).mean()`). Print
   the number of days in 2024 on which the price closed **above** this
   average and the total number of trading days in 2024 on one line.

**Expected output:**

```
27.0
2023-03-02 39.8
2023-10-18 18.5
157 262
```

Volatility is not a fixed number: the calmest stretch and the most turbulent
one differ by more than a factor of two. That is why, when measuring risk,
you look at the rolling value of the day rather than a single average
volatility.
