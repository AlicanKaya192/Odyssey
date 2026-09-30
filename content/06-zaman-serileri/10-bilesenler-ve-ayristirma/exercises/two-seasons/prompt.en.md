The daily sales hold two patterns: weekly and yearly. Compare the
classical method, which separates only the weekly one, with `MSTL`, which
separates both.

**What to do:**

1. `classic = seasonal_decompose(s, model="additive", period=7)`.
2. `fit = MSTL(s, periods=(7, 365)).fit()`.
3. Print the columns of the `fit.seasonal` table as a list.
4. Print the standard deviation of the residual for the classical method and
   MSTL, rounded to two decimals, on one line.
5. Average the **trend** component by month for the two methods; for each,
   print the difference between the highest and the lowest month, rounded to a
   whole number, on one line (classical first).
6. Print the first and the last value of the MSTL trend, rounded to one
   decimal, on one line.
7. Print the highest and the lowest day in 2024 of the yearly seasonal
   component (`fit.seasonal["seasonal_365"]`) in `"%m-%d"` form on one line.

**Expected output:**

```
['seasonal_7', 'seasonal_365']
12.32 5.89
91 32
207.4 310.7
12-30 06-11
```

In the classical method the trend swung 90 units within the year: that swing
was the yearly season. MSTL moved it into its own column and the residual has halved.
The 32 units left in the MSTL trend are not a season: the shop grows by about
35 units a year, which is why the December mean is above January's.
