`poly_score(degree)` should put `PolynomialFeatures(degree)` at the start of the model
(`PolynomialFeatures` → `StandardScaler` → `Ridge(alpha=1e-3)`) and return the
mean R² with the given `KFold` with 3 places. The starter code never uses
`degree`.

**Expected output:**

```
0.641
0.963
```
