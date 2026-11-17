`dropout_values(p)` should apply Dropout to 1000 ones: first in training mode, then
in `eval()` mode. It should return the **distinct** values in each mode as sorted
lists: `[in training, in evaluation]`. Round the training ones to 4 places.

**Expected output:**

```
[[0.0, 2.0], [1.0]]
[[0.0, 1.25], [1.0]]
```
