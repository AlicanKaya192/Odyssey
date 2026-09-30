Do the same decomposition with `seasonal_decompose`, save its chart and
question the residual.

**What to do:**

1. `result = seasonal_decompose(s, model="additive", period=7)`.
2. Save the four-panel chart: `fig = result.plot()`, then
   `fig.savefig("chart.png")`.
3. Print the number of `NaN` values in the residual and its standard
   deviation (two decimals) on one line.
4. Print the dates of the three residuals that are largest in absolute value
   as a list (`"%Y-%m-%d"`).
5. For the day of the largest residual print the observation, trend, seasonal
   value and residual (one decimal) on one line.
6. Print the largest absolute value among the means of the residual by day of
   the week, rounded to one decimal.
7. Average the **trend** component by month; print the number and value (a
   whole number) of the lowest and the highest month as
   `month value month value`.

**Expected output:**

```
6 12.32
['2023-12-30', '2024-11-09', '2022-05-14']
462 338.3 76.2 47.5
0.0
6 231 12 322
```

The mean of the residual by day of the week is zero: the weekly pattern has
been separated completely. But the trend itself swings 90 units from June to
December: the yearly season was not separated, it sits inside the trend. In
the **Output** tab on the left you will see the trend panel draw one wave a
year.
