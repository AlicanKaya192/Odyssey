Write the function `fit_weights(X, y)`: add a column of 1s at the front and
solve `(Aᵀ A) w = Aᵀ y` with `np.linalg.solve`. It returns the list
`[w₀, w₁, …]` with `.round(4).tolist()`.

No `LinearRegression`.

**Expected output:**

```
[1.7333, 0.4444, 3.4444]
```
