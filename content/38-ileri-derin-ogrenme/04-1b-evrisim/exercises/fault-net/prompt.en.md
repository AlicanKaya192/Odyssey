Write the `features` part of `FaultNet`: `nn.Conv1d(1, 8, 5, padding=2)`, ReLU,
`nn.Conv1d(8, 8, 5, padding=2)`, ReLU and `nn.AdaptiveMaxPool1d(1)`. The rest
is ready: the code first prints the shape of the features, then trains the
network and prints whether the test accuracy is above 90%.

**Expected output:**

```
(2, 8, 1)
True
```
