A short version of everything in the lesson. Come back here when you get stuck on a question.

## Formulas

| What | Formula |
|---|---|
| covariance | $\operatorname{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)] = E[XY] - E[X]E[Y]$ |
| sample covariance | $s_{xy} = \frac{1}{n - 1}\sum (x_i - \bar{x})(y_i - \bar{y})$ |
| correlation | $r = \frac{s_{xy}}{s_x s_y}$, $\ -1 \leq r \leq 1$ |
| covariance from correlation | $\operatorname{Cov} = r \, \sigma_X \sigma_Y$ |
| variance of a sum | $\operatorname{Var}(X \pm Y) = \operatorname{Var}X + \operatorname{Var}Y \pm 2\operatorname{Cov}(X, Y)$ |
| linear transformation | $\operatorname{Cov}(aX + b, cY + d) = ac\operatorname{Cov}(X, Y)$ |
| covariance matrix | $\Sigma = \frac{1}{n - 1} X^\mathsf{T} X$ (centred $X$) |

## Reading r

| $r$ | Meaning |
|---|---|
| $1$ or $-1$ | the points lie exactly on a line |
| above $0.7$ (in absolute value) | strong linear relationship |
| $0.3$–$0.7$ | moderate |
| below $0.3$ | weak |
| $0$ | no linear relationship (another kind may exist) |

## The covariance matrix

- Diagonal: variances; off-diagonal: covariances.
- Symmetric and positive semi-definite.
- The diagonal of the correlation matrix is $1$.

## Practical tips

- Look at the scatter plot first; then compute $r$.
- Trust the sign of the covariance, not its size.
- Independence makes the covariance zero; zero covariance does not mean
  independence.
- Correlation is not causation; look for a hidden variable.
- With outliers, try Spearman (rank) correlation.
