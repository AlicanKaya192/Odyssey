`cnn_params(channels, kernel)` should build convolutions in a row: one
`nn.Conv2d(in, out, kernel)` for each neighbouring pair `(in, out)` in the
`channels` list. It should return the total number of parameters (weights +
biases) of all layers.

**Expected output:**

```
1248
1216
```
