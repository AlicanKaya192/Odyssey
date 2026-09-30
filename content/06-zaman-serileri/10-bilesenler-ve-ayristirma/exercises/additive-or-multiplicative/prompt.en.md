Decompose the monthly passenger series with both models and ask the
residual which one is right.

**What to do:**

1. `add = seasonal_decompose(p, model="additive", period=12)` and
   `mul = seasonal_decompose(p, model="multiplicative", period=12)`.
2. Average the absolute value of the additive residual **by year**; print the
   values for 2013, 2019 and 2023, rounded to one decimal, on one line.
3. Print the additive residual for **July** 2013 and July 2023 (one decimal)
   on one line.
4. The multiplicative residual is a ratio around 1. Turn it into a percentage
   deviation: `pct = (mul.resid - 1).abs() * 100`. Print the mean for the same
   three years, rounded to one decimal, on one line.
5. Print the largest value of `pct`, rounded to one decimal.
6. Print the smallest and the largest multiplicative seasonal factor together
   with its month number as `month factor month factor` (three decimals). The
   factors are in `mul.seasonal.iloc[:12]`, January to December.

**Expected output:**

```
12.7 2.8 13.1
-22.0 20.5
0.6 0.7 1.4
3.6
2 0.83 8 1.255
```

The residual of the additive model is large at the ends, small in the middle,
and in July its sign turns from negative to positive: a single fixed "July
share" is too much for the early years and too little for the late ones. In
the multiplicative model the deviation is around 1% every year. The series is
multiplicative.
