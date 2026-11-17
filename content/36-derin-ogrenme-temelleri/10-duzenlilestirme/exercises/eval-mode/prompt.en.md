`same_twice` gives a model with Dropout the same input twice and checks whether the
outputs are equal; the second comparison should be done in evaluation mode, but
the model is still in training mode. Fix it: it should print `[False, True]`.

**Expected output:**

```
[False, True]
```
