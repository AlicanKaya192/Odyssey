`trainable_count(n_in, n_hidden, n_out)` builds the model and returns `[trainable
parameter count, total parameter count]`. Freeze the first layer (`model[0]`) and
count the trainable ones only among those with `requires_grad`.

**Expected output:**

```
[51, 163]
[12, 67]
```
