The data with gain, the 1D convolutional network, the optimiser and the
`DataLoader` are ready.

1. Train for 10 epochs: `model.train()`, in every batch `zero_grad`,
   `cross_entropy`, `backward`, `step`.
2. `model.eval()`; predict on the test windows (`500:600`).
3. Compute `acc` (accuracy) and `recall` (the fault class's recall).

**Expected output:**

```
True True
```
