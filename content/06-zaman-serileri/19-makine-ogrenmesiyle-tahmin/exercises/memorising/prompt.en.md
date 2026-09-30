Compare three models on the same table and look at the gap between the
training and the test error.

**What to do:**

1. Fit three models (all on `train[columns]`, `train["y"]`):
   - `"linear"`: `LinearRegression()`
   - `"forest"`: `RandomForestRegressor(n_estimators=200, random_state=0)`
   - `"boosting"`: `HistGradientBoostingRegressor(random_state=0)`
2. For each print the training error, the test error (MAE, two decimals) and
   their ratio (test / training, one decimal) as `name training test ratio`,
   one per line.
3. Print the names of the models whose test error is below seasonal naive
   (`test["lag7"]`) as a list.

**Expected output:**

```
linear 10.89 11.51 1.1
forest 4.31 12.87 3.0
boosting 4.79 14.63 3.1
['linear', 'forest']
```

For the linear model the two errors are almost the same. The two tree-based
models "know" the training data very well yet are behind the linear model on
the test: 700 rows are not enough to feed a model with thousands of leaves.
Gradient boosting does not even beat seasonal naive. A low training error is
not an achievement, it is a warning.
