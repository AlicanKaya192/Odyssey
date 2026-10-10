## Regression

| Class | When | Key setting |
|---|---|---|
| `LinearRegression()` | few columns, interpretation | — |
| `Ridge(alpha=1.0)`, `RidgeCV(alphas=...)` | many/correlated columns | large `alpha` is a strong penalty |
| `Lasso(alpha=...)`, `LassoCV(cv=5)` | some columns should become zero | larger `alpha`, more zeros |
| `ElasticNet(alpha, l1_ratio)`, `ElasticNetCV` | a mix of Lasso + Ridge | `l1_ratio` 0–1 |
| `HuberRegressor()` | a target with outliers | `epsilon` |
| `QuantileRegressor(quantile=0.9)` | a percentile, not the mean | `quantile`, `alpha` |
| `PoissonRegressor()` | a count target (0, 1, 2, ...) | `alpha` |
| `SGDRegressor()` | very large data, `partial_fit` | `alpha`, `max_iter` |

## Classification

| Class | When | Key setting |
|---|---|---|
| `LogisticRegression()` | a baseline that gives probabilities | small `C` is a strong penalty |
| `LogisticRegression(l1_ratio=1, solver="saga")` | L1, sparse coefficients | `C` |
| `LogisticRegression(C=np.inf)` | unpenalised | — |
| `LogisticRegressionCV(Cs=10, cv=5)` | chooses `C` itself | `Cs` |
| `SGDClassifier(loss="log_loss")` | very large data | `alpha` |
| `RidgeClassifier()` | fast, when no probabilities are needed | `alpha` |

## Attributes to read

| Attribute | What |
|---|---|
| `coef_`, `intercept_` | the coefficients and the constant |
| `alpha_`, `C_` | the penalty chosen by the `...CV` classes |
| `n_iter_` | the solver's steps; equal to `max_iter` means it did not converge |
| `classes_` | the class order of the rows of `coef_` |

## Rules

- `StandardScaler` before penalised models: the penalty applies to all
  coefficients equally, so an unscaled column is penalised unfairly.
- The penalty grows as `alpha` (Ridge/Lasso) grows and as `C` (logistic)
  shrinks.
- `penalty=` is deprecated: `l1_ratio=1` for L1, `C=np.inf` for none.
