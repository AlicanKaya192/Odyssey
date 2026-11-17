`fit_save_load` learns the line `y = 2x + 1` and builds a new `fresh` model with
another seed. Save the trained model's state_dict to `line.pt` and load it into
`fresh` with `weights_only=True`; the result should be `[2.0, 1.0, True]`.

**Expected output:**

```
[2.0, 1.0, True]
```
