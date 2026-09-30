Apply the two tests to the price and to its difference, and let the code
print the verdict.

**What to do:**

1. Write a function `verdict(x)`. Inside it:
   - `adf_p = adfuller(x)[1]`
   - `kpss_p = kpss(x, regression="c", nlags="auto")[1]`
   - Stationary according to ADF: `adf_p < 0.05`. Stationary according to
     KPSS: `kpss_p >= 0.05`.
   - If both say stationary return `"stationary"`, if both say not,
     `"not stationary"`, otherwise `"mixed"`.
   The function returns three things as a tuple: `round(adf_p, 3)`,
   `round(kpss_p, 3)` and the verdict text (convert the p-values with
   `float(...)`).
2. Print the result of `verdict(k)`.
3. Print the result of `verdict(k.diff().dropna())`.
4. Print the ADF statistic and its 5% critical value for the price, rounded to
   two decimals, on one line (`result = adfuller(k)`; the statistic is
   `result[0]`, the critical values `result[4]["5%"]`).

**Expected output:**

```
(0.348, 0.01, 'not stationary')
(0.0, 0.1, 'stationary')
-1.87 -2.87
```

For the price both tests say "not stationary": the p-value of ADF is large,
that of KPSS small. For the difference both say "stationary". The last line
says the same another way: the statistic (−1.87) is **less negative** than the
critical value (−2.87), so there is no rejection.
