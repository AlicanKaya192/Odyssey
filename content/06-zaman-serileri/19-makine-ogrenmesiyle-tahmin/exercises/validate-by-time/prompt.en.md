Measure the same model with two different cross-validations: shuffled
`KFold` and `TimeSeriesSplit`.

**What to do:**

1. The model: `HistGradientBoostingRegressor(random_state=0)`.
2. Compute the MAE with `cross_val_score`
   (`scoring="neg_mean_absolute_error"`; multiply the result by minus one).
   Two splits:
   - `KFold(5, shuffle=True, random_state=0)`
   - `TimeSeriesSplit(5)`
3. For each print the error of the five parts with one decimal as a list and
   their mean with two decimals, as `[list] mean`, one per line (`KFold`
   first).
4. Print the number of training and test rows in the first and the last split
   of `TimeSeriesSplit(5)` as `training test`, on two lines.

**Expected output:**

```
[11.8, 12.0, 12.0, 12.4, 11.3] 11.88
[24.9, 11.8, 15.0, 14.5, 12.7] 15.78
178 178
890 178
```

Shuffled validation gives a similar, small error in all five parts: the model
saw the neighbours of every test day in training. Validation by time is larger
and more variable: in the first split the training is very short and the error
large. The job you will really do is the second; that is the honest number.
