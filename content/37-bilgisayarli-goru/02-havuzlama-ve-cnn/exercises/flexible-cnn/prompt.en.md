`build_cnn(num_classes)` should build this network: `Conv2d(1, 16, 3,
padding=1)`, `ReLU`, `MaxPool2d(2)`, `Conv2d(16, 32, 3, padding=1)`, `ReLU`,
`AdaptiveAvgPool2d(1)`, `Flatten`, `Linear(32, num_classes)`.
`param_count(num_classes)` should return its parameter count. The program
tries the network on pictures of two sizes.

**Expected output:**

```
16 (2, 5)
40 (2, 5)
4965
```
