`EarlyStopping.step(val_loss)` should take each epoch's validation loss: if the loss
is lower than the best so far, update the best, reset the counter and return
`False`; otherwise grow the counter and return `True` if it reached
`patience`.

**Expected output:**

```
6
None
```
