Deliver the forecast: the first 28 days of January 2025, with a point
forecast and a tested 80% interval.

In the starter code `features`, `log_model` and `cuts` are ready.

**What to do:**

1. Collect the **relative** errors of the 13 experiments: at each cut
   `actual / forecast - 1` (28 values); a 13 × 28 numpy array.
2. Print the mean of the relative error and its 10% and 90% quantiles with
   three decimals on one line.
3. Test the interval: for each experiment take the quantiles from the errors
   of **the other 12** (`np.delete(errors, i, axis=0)`) and measure how many
   of that experiment's errors are inside. Print the mean of the 13 coverages
   with three decimals.
4. Fit the model on the whole series and forecast 1–28 January 2025
   (`pd.date_range("2025-01-01", periods=28, freq="D")`). Print the total of
   the 28 days as a whole number.
5. For the first day print the forecast and the lower and upper end of the 80%
   interval (`forecast * (1 + quantile)`) as whole numbers on one line.
6. Draw a chart: the last 42 days of 2024, the forecast and the interval with
   `fill_between`. Save it as `chart.png`.

**Expected output:**

```
0.003 -0.309 0.258
0.797
7541
255 177 321
```

The model is unbiased (the mean error is very close to zero) but the
uncertainty is large: the 80% interval runs from 31% below the forecast to 26%
above. Tested, it holds what it says (0.80). The interval being longer
downwards comes from rain: a rainy day ends up far below the forecast. What
you deliver is not a single number: a forecast, an honest interval and the
source of the error.
