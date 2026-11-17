`running_after(batches)` should give the batches in order (in training mode) to a
single-feature `nn.BatchNorm1d(1)` and at the end return `running_mean` with 4
places. Each batch is a list of numbers; it must reach the layer in shape
`(n, 1)`.

**Expected output:**

```
1.27
```
