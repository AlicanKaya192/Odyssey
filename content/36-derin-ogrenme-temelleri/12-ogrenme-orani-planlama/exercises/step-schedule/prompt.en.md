`step_rates(lr, step_size, gamma, epochs)` should wrap a one-parameter SGD in
`StepLR` and append the learning rate at the start of every epoch (with 6
places) to a list. In every epoch, first `optimizer.step()`, then
`scheduler.step()`.

**Expected output:**

```
[0.1, 0.1, 0.05, 0.05, 0.025]
```
