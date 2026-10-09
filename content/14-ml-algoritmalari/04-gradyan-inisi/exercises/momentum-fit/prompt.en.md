Write the function `momentum_fit(A, y, lr, beta, steps)`: `w` and `v` start
from zero; at each step `v = beta · v + gradient`, `w = w − lr · v` (the MSE
gradient). Return the final weights with `.round(3).tolist()`. `beta = 0` is
plain gradient descent.

**Expected output:**

```
[0.971, 2.013]
[1.045, 2.094]
```
