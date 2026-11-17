`used_rates(epochs)` records the rate the optimizer uses in every epoch; but the
scheduler is called in the wrong place and the rate drops one epoch earlier
than planned. Fix the order: record the rate, `optimizer.step()`, then
`scheduler.step()`.

**Expected output:**

```
[0.1, 0.1, 0.05, 0.05, 0.025, 0.025]
```
