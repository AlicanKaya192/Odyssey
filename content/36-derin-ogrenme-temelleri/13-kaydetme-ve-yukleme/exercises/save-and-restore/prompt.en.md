`restore_matches` saves a model to `weights.pt` and builds a second model with
another seed; but it never loads the saved numbers into the second model.
Before the `after` line, read the file with `weights_only=True` and load it
with `load_state_dict`. The result should be `[False, True]`.

**Expected output:**

```
[False, True]
```
