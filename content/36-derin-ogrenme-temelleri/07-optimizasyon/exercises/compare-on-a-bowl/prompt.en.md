`run` should run an optimizer for 40 steps in the valley `20·w₁² + w₂²` and give
the remaining loss, but the loop is missing. Write the loop; the results of three
optimizers are printed. The order may not match the lesson: the winner depends on
the valley and the settings.

**Expected output:**

```
SGD 0.153
momentum 0.166
Adam 0.258
```
