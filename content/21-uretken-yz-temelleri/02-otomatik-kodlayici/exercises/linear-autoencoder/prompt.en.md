`train_linear(k, steps, lr, seed)` should train a linear autoencoder with
gradient descent. `A = X_train - mean`; with the generator
`np.random.default_rng(seed)` first `E = rng.normal(0, 0.1, (64, k))`, then
`D = rng.normal(0, 0.1, (k, 64))`. At each step: `code = A @ E`,
`err = code @ D - A`, `gD = code.T @ err * 2 / err.size`,
`gE = A.T @ (err @ D.T) * 2 / err.size`, then `E -= lr * gE` and
`D -= lr * gD`. At the end return the test images' error (rebuilding with
`(X_test - mean) @ E @ D + mean`) as a `float` rounded to 4 places.

**Expected output:**

```
0.0248
0.0245
```
