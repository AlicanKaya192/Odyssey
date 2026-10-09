Write the function `lasso_fit(X, y, alpha, rounds)` (scikit-learn's scale):
centre; `w` from zero; in each round for each `j`,
`resid = yc − Xc w + Xc[:, j] w[j]`, `ρ = Xc[:, j] · resid / n`,
`w[j] = soft(ρ, α) / (Xc[:, j] · Xc[:, j] / n)`. Return the list
`[intercept, w…]` with `round(..., 3)`.

No `Lasso`.

**Expected output:**

```
[1.15, 1.95, 0.0, -0.0]
[4.0, 1.0, 0.0, -0.0]
```
