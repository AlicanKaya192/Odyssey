`vgg_summary(config)` should build a VGG-style network from a list: for a number,
a `Conv2d(..., 3, padding=1)` with that many output channels + `ReLU`; for
`"M"`, `MaxPool2d(2)`. The first input has 1 channel. Return `[parameter
count, the output shape for a (1, 1, 16, 16) input, without the batch]`.

**Expected output:**

```
[16368, [32, 4, 4]]
[1248, [8, 2, 2]]
```
