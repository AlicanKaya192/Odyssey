## Building

| Code | What it does |
|---|---|
| `import statsmodels.api as sm` | the array interface |
| `sm.add_constant(X)` | adds a `const` column (do not forget) |
| `sm.add_constant(new, has_constant="add")` | adds it for one row too |
| `sm.OLS(y, X).fit()` | trains the model |
| `.fit(cov_type="HC3")` | standard errors robust to non-constant variance |

## The result object

| Attribute | What |
|---|---|
| `res.params` | the coefficients |
| `res.bse` | the standard errors |
| `res.pvalues` | the p-values |
| `res.conf_int(alpha=0.05)` | the confidence intervals |
| `res.rsquared`, `res.rsquared_adj` | R² and adjusted R² |
| `res.aic`, `res.bic` | model comparison (smaller is better) |
| `res.resid`, `res.fittedvalues` | residuals, fitted values |
| `res.summary()`, `res.summary().tables[1]` | the report, the coefficient table |
| `res.get_prediction(X_new).summary_frame()` | prediction, `mean_ci`, `obs_ci` |

## Diagnostics

| Code | Its question |
|---|---|
| `variance_inflation_factor(X.values, i)` | is this column the same as others? (10+ is bad) |
| `het_breuschpagan(res.resid, res.model.exog)` | is the error variance constant? (small p: no) |
| `res.f_test("x = 0")` | is one or more coefficients zero? |

## While reading

- A p-value is not the **size** of an effect; with large data a small effect
  also gets a very small p. Look at the coefficient and its interval first.
- A large p does not mean "no effect" but "cannot be told apart with this
  data".
- In observational data a coefficient tells a relationship, not **cause and
  effect**.
