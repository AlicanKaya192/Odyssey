Write the four error measures as functions and apply them to the
experiment of Section 14. In the starter code `actual` (the 28-day test) and
`forecast` (the seasonal naive forecast) are ready as numpy arrays.

**What to do:**

1. Write four functions, each taking `actual` and `forecast`:
   - `mae`: the mean of the absolute errors
   - `rmse`: the square root of the mean of the squared errors
   - `mape`: the mean of `|error| / |actual|`, × 100
   - `bias`: the mean of the errors (actual − forecast)
2. Print the four results, rounded to two decimals, on one line (order: MAE,
   RMSE, MAPE, bias).
3. Print the RMSE / MAE ratio, rounded to two decimals.
4. Print the same four measures for the method that forecasts the training
   mean for every day (`np.full(28, train.mean())`).

**Expected output:**

```
11.64 13.98 3.46 6.79
1.2
75.98 94.02 20.9 75.98
```

For seasonal naive the bias is about half the MAE: the errors go both ways.
For the mean forecast the MAE and the bias are the same number: the forecast
is low on all 28 days. The four measures give the same ranking, but each says
something different: the typical miss, the big miss, the proportional miss and
the direction of the miss.
