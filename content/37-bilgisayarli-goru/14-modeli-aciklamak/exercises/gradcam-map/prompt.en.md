`gradcam_map(maps, grads)` should take two lists of shape `(C, H, W)`: the
last convolution maps and the gradient of the class score with respect to
them. It should return the Grad-CAM map (channel weight = mean gradient;
weighted sum of the maps; ReLU) as a list of lists rounded to 3 places.

**Expected output:**

```
[[1.0, 0.0], [0.0, 0.0]]
[[0.5, 0.0], [0.0, 1.0]]
```
