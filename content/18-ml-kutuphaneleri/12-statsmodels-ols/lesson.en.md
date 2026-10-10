# statsmodels: OLS

scikit-learn is built for **prediction**: it trains a model and gives the
outcome for a new row. Sometimes the question is different: "Does age really
affect the price, or is this coefficient chance? How sure are we about the
size of the effect?" That is an **inference** question, and statsmodels
exists for it: it gives each coefficient's standard error, p-value and
confidence interval. This section covers the most basic model, ordinary
least squares (OLS) regression.

## OLS and the coefficient table

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(7)
area = rng.uniform(50, 200, 120)
age = rng.uniform(0, 40, 120)
noise = rng.normal(0, 1, 120)                 # unrelated to the price
price = 50 + 3 * area - 2 * age + rng.normal(0, 40, 120)
X = pd.DataFrame({"area": area, "age": age, "noise": noise})
res = sm.OLS(price, sm.add_constant(X)).fit()
print(res.summary().tables[1])
print(round(res.rsquared, 3), round(res.rsquared_adj, 3))
sk = LinearRegression().fit(X, price)
print(np.round(sk.coef_, 2).tolist(), round(sk.intercept_, 2))
```

```text
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
const         63.4200     11.489      5.520      0.000      40.664      86.176
area           2.9337      0.078     37.385      0.000       2.778       3.089
age           -2.5867      0.289     -8.943      0.000      -3.160      -2.014
noise         -4.1466      3.606     -1.150      0.253     -11.290       2.996
==============================================================================
0.925 0.923
[2.93, -2.59, -4.15] 63.42
```

- `sm.OLS(y, X).fit()` trains the model; the result object (`res`) carries
  everything. `summary()` is a long report; here we printed only the
  coefficient table (`tables[1]`).
- **coef** are the coefficients: the same as scikit-learn's (2.93, −2.59).
  The difference is in the columns beside them.
- **std err** (standard error): how unsteady the coefficient is. With
  another sample of 120 houses the coefficient would move by about this
  much.
- **[0.025 0.975]** is the 95% confidence interval: 2.78–3.09 for `area`,
  which contains the 3 that made the data; −3.16 to −2.01 for `age`, which
  contains the true −2.
- **P>|t|** (the p-value): "the probability of seeing an estimate this large
  if the true coefficient were zero". For `noise` it is 0.253: the data does
  **not show** that this coefficient differs from zero. Its interval also
  contains zero (−11.29 to 3.00). This does not mean "no effect"; it means
  "cannot be told apart with this data".
- R² 0.925; adjusted R² (which penalises the number of columns) 0.923.

## Forgetting add_constant

```python
no_const = sm.OLS(price, X).fit()
print({k: round(v, 2) for k, v in no_const.params.items()})
print(round(no_const.rsquared, 3))
```

```text
{'area': 3.28, 'age': -1.89, 'noise': -4.23}
0.989
```

- statsmodels does **not** add the constant term itself; `sm.add_constant(X)`
  adds a `const` column (all ones). When it is forgotten, the model forces the
  line through zero and all the coefficients shift (`area` 3.28, `age`
  −1.89).
- On top of that R² **rises** to 0.989. Without a constant R² is defined
  differently (relative to zero, not the mean); this number cannot be
  compared with the one above. What looks like a better model is the wrong
  model.
- In scikit-learn `LinearRegression` adds the constant itself
  (`fit_intercept=True`); in statsmodels it is done by hand.

## Related columns: VIF

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

twin = area * 0.09 + rng.normal(0, 0.5, 120)   # almost a copy of area
X2 = sm.add_constant(pd.DataFrame({"area": area, "twin": twin, "age": age}))
res2 = sm.OLS(price, X2).fit()
print({k: round(v, 2) for k, v in res2.params.items()})
print({k: round(v, 2) for k, v in res2.bse.items()})
vif = [variance_inflation_factor(X2.values, i) for i in range(1, 4)]
print([round(float(v), 1) for v in vif])
```

```text
{'const': 62.7, 'area': 3.33, 'twin': -4.34, 'age': -2.58}
{'const': 11.62, 'area': 0.7, 'twin': 7.54, 'age': 0.29}
[79.1, 78.9, 1.0]
```

- `twin` is a noisy copy of the area (correlation above 0.99). When the two
  carry the same information, the model splits the effect between them
  arbitrarily: `area` 3.33, `twin` −4.34 (negative!). The price is still
  predicted well, but the coefficients cannot be interpreted.
- The standard error of `area` rose from 0.08 to 0.7, about 9 times.
- **VIF** (variance inflation factor) says this with a number: 79 for `area`
  and `twin`, 1 for `age`. Roughly, above 10 means "this column is almost the
  same as others". The cure: drop one, or combine the two into one column.

## Prediction and two intervals

```python
new = pd.DataFrame({"area": [100, 180], "age": [10, 30], "noise": [0, 0]})
pred = res.get_prediction(sm.add_constant(new, has_constant="add"))
print(pred.summary_frame(alpha=0.05).round(1))
```

```text
    mean  mean_se  mean_ci_lower  mean_ci_upper  obs_ci_lower  obs_ci_upper
0  330.9      4.9          321.3          340.6         256.9         405.0
1  513.9      5.9          502.2          525.6         439.5         588.2
```

- `mean` is the prediction. Beside it there are **two** intervals:
- `mean_ci` (321.3–340.6): an interval for the **average** price of houses
  with these features. Narrow, because the average is estimated well.
- `obs_ci` (256.9–405.0): an interval for the price of **a single** house.
  Much wider, because a single house's own noise is included.
- The answer to "how much will this house sell for?" is `obs_ci`. Giving
  `mean_ci` for a single house is speaking too confidently.
- `has_constant="add"`: the new data needs the `const` column too. By default
  `add_constant` does not add one if it sees a column that is already
  constant; with **one row** every column looks constant, so no `const` is
  added and the prediction fails. `"add"` always adds it.

## Summary

- scikit-learn for prediction, statsmodels for "how large is the effect and
  how sure are we".
- Do not forget `sm.add_constant`; when forgotten, R² rises misleadingly.
- The coefficient table: coefficient, standard error, p-value, confidence
  interval.
- A large p-value does not mean "no effect" but "cannot be told apart".
- Related columns spoil the coefficients; check with VIF.
- `obs_ci` for a single observation, `mean_ci` for the average.
