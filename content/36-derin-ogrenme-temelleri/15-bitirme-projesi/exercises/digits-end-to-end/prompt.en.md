`train_and_test(epochs)` builds the data, the model, the `DataLoader` and the
optimizer and measures the test accuracy at the end; but the training loop in
between is missing. Write it: in every epoch, for every batch, `zero_grad`,
the loss, `backward`, `step`. In 10 epochs the test accuracy should pass 90%.

**Expected output:**

```
True
```
