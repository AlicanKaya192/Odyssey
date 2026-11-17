`training_mode(model)` should prepare a two-part model (body `model[0]`, head
`model[1]`) for training with a frozen body: the model in training mode, but
the body (including the BatchNorm inside it) in evaluation mode.

**Expected output:**

```
True False True
False
```
