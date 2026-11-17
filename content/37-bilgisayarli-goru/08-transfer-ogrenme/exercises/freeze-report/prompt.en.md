`freeze_report(num_classes)` should build `models.resnet18(weights=None)`,
freeze every parameter, **then** replace `fc` with a new `Linear` with
`num_classes` outputs and return `[number of trainable parameters, number of
frozen parameters]`.

**Expected output:**

```
[1026, 11176512]
[5130, 11176512]
```
