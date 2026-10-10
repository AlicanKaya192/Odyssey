`skewed_fit(seed)` generates an exponentially growing target and splits it.
Make the model `TransformedTargetRegressor(regressor=LinearRegression(),
func=np.log, inverse_func=np.exp)` and return `[test_R2, prediction_at_x=0]`
(2 places each). The starter code uses a plain `LinearRegression`.

**Expected output:**

```
[0.81, 2.66]
```
