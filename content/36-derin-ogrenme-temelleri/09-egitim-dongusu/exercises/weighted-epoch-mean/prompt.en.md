`epoch_mean(batch_losses, batch_sizes)` should return two means: the mean weighted
by the number of examples and the plain mean of the batches, `[weighted, plain]`,
4 places. How do they differ when the last batch is small?

**Expected output:**

```
[0.4118, 0.5833]
```
