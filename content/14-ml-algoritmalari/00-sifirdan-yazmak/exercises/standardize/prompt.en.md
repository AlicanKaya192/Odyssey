Write the function `standardize(train, test)`: compute the mean and
standard deviation **only from the training** data (per column, `ddof=0`) and
scale the **test** data with `(x − mean) / sd`. It returns the result with
`.round(3).tolist()`.

No scikit-learn `StandardScaler`.

**Expected output:**

```
[[0.0, 0.566], [-2.236, -2.828]]
```
