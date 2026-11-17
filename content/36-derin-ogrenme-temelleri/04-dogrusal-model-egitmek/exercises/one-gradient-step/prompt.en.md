`one_step(w_value, b_value, xs, ys, lr)` should take **one** gradient descent step
for the linear model: compute the MSE loss, `backward()`, update both parameters
inside `torch.no_grad()`. Return the new `[w, b]` with 4 places.

**Expected output:**

```
[1.3, 0.8]
[1.0, 1.0]
```
