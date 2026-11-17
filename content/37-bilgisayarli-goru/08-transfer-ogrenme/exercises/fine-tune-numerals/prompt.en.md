`transfer(state, x, y, x_test, y_test, fine_tune)` should train a new model,
whose body is loaded from `state`, for the 10 digits and return the test
accuracy. If `fine_tune` is true the whole model trains with `lr=0.002`;
otherwise the body is frozen and only the head trains with `lr=0.005`. Both
use Adam, batch 8, `generator=torch.Generator().manual_seed(0)`, 30
epochs.

**Expected output:**

```
True True
True
```
