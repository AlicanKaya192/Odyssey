Use the Ljung–Box test to see whether three series hold usable memory.

**What to do:**

1. Write a function `memory(x, lags)`: it calls
   `acorr_ljungbox(x, lags=[lags])` and returns the single value in the
   `lb_pvalue` column rounded to four decimals (convert with `float(...)`).
2. For three series print the result and the verdict as `name p verdict`, one
   per line:
   - `"price"`: the price itself, 10 lags
   - `"price change"`: the daily difference of the price, 10 lags
   - `"sales d7"`: the `diff(7)` of the sales, 14 lags

   The verdict: `memory` if p < 0.05, otherwise `noise`.
3. Print the test statistic (`lb_stat`) for the daily difference of the price,
   rounded to two decimals.

**Expected output:**

```
price 0.0 memory
price change 0.2833 noise
sales d7 0.0 memory
12.03
```

The price itself looks full of memory (the trend). In its daily difference no
memory can be found: it cannot be told from white noise. In the seasonal
difference of the sales there is still structure that can be modelled; that is
the job of the model in Section 17.
