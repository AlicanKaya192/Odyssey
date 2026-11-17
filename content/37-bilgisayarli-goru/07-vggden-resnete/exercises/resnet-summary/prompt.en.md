`resnet_summary(num_classes)` should build `models.resnet18(weights=None)`,
replace `fc` with a `Linear` with `num_classes` outputs and return
`[number of convolution layers, parameter count]`.

**Expected output:**

```
[20, 11178051]
[20, 11181642]
```
