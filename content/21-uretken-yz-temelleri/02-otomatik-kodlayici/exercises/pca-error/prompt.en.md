`pca_error(k)` should find the PCA directions from the training images
(subtract the mean first, then `np.linalg.svd(..., full_matrices=False)`),
project the test images onto the first `k` directions, rebuild them and
return the mean squared error as a `float` rounded to 4 places.

**Expected output:**

```
2 0.0539
8 0.0245
16 0.0115
```
