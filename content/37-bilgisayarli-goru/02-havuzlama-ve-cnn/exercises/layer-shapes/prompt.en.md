`layer_shapes(size)` should build the lesson's network up to `Flatten`:
`Conv2d(1, 8, 3, padding=1)`, `ReLU`, `MaxPool2d(2)`, `Conv2d(8, 16, 3,
padding=1)`, `ReLU`, `MaxPool2d(2)`, `Flatten`. Pass a zero input of size
`(1, 1, size, size)` through it layer by layer and collect the shape after
each layer (without the batch dimension) as a list.

**Expected output:**

```
[8, 16, 16]
[8, 16, 16]
[8, 8, 8]
[16, 8, 8]
[16, 8, 8]
[16, 4, 4]
[256]
```
