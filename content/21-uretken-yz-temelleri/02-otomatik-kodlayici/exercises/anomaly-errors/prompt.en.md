`anomaly_errors(k)` should build PCA **only from the training images of digits
0–4** (`y_train = y[order[:1500]]`). Then rebuild every test image with the
first `k` directions, find the mean squared error per image and return two
averages: `[mean error of the 0–4 test images, mean error of the 5–9 test
images]`, as `float`s rounded to 4 places.

**Expected output:**

```
[0.0199, 0.0398]
[0.009, 0.0214]
```
