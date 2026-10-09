Write the function `kernel_matrix(X, degree)`: the polynomial kernel
`K = (X Xᵀ + 1)^degree`; return the matrix with `.round(3).tolist()`. No loops:
a single matrix product.

**Expected output:**

```
[4.0, 1.0, 4.0]
[1.0, 4.0, 4.0]
[4.0, 4.0, 9.0]
```
