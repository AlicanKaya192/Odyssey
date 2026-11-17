`loss_looks_fresh(num_classes, loss)` should say whether a randomly initialised
model's starting loss is reasonable: `True` if the loss is less than 0.5 away
from `log(num_classes)`, otherwise `False`.

**Expected output:**

```
True
False
```
