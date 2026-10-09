## Formulas

| What | Formula | NumPy / scikit-learn |
|---|---|---|
| Model | `ŷ = w₀ + Σ wᵢ xᵢ` = `A w` | `LinearRegression` |
| Intercept column | `A = [1, X]` | `np.column_stack([np.ones(n), X])` |
| Solution | `(Aᵀ A) w = Aᵀ y` | `np.linalg.solve`, `np.linalg.lstsq` |
| MSE | `Σ(y − ŷ)² / n` | `mean_squared_error` |
| RMSE | `√MSE` (same unit as the target) | `root_mean_squared_error` |
| MAE | <code>Σ&#124;y − ŷ&#124; / n</code> (less sensitive to outliers) | `mean_absolute_error` |
| R² | `1 − Σ(y − ŷ)² / Σ(y − ȳ)²` | `r2_score` |

## When to be careful?

- **Collinearity:** almost identical features; if `np.linalg.cond` is large, do
  not interpret the weights, use regularisation.
- **Scale:** the normal equation is not affected by scale, but features are
  standardised to compare weights and for gradient descent (section 4).
- **Outliers:** the squared error punishes large errors heavily; a single
  outlier can pull the line towards itself.
- **A non-linear relation:** if the residuals show a pattern, add features
  (`x²`, an interaction `x₁·x₂`).

## Common mistakes

- Forgetting the intercept column: the line is forced through the origin.
- Writing `np.linalg.inv(A.T @ A)`: `solve` or `lstsq` is sounder.
- Measuring R² on the training data and stopping there: it does not show
  overfitting.
