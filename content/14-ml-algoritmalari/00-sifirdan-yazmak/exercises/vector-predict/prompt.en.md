Write the function `predict(X, w, b)`: it returns the prediction
`x · w + b` for each row as a list (`.round(3).tolist()`).

**No loops:** a single matrix product (`X @ w`) and broadcasting. The last line
has two hundred thousand rows.

**Expected output:**

```
[-0.25, -1.75, 2.25]
-0.0037439849999999996
```
