The starter has a forecast of shape `(batch, 1)` and a target of shape
`(batch,)`. `loss_shapes(batch)` should return two shapes as lists: the shape
of the difference `pred - target` and that of `pred.squeeze(-1) - target`.

**Expected output:**

```
[[4, 4], [4]]
[[1, 1], [1]]
```
