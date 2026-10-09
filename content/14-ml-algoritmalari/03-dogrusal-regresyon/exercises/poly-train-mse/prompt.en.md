Write the function `poly_train_mse(x, y, degree)`: the features are
`x, x², …, x^degree` (and a column of 1s at the front); find the weights with
`np.linalg.lstsq` and return the **training** MSE, `round(..., 4)`.

The training error keeps falling as the degree grows; that does not mean the
model is better.

**Expected output:**

```
1 6.2347
2 0.0125
4 0.0007
```
