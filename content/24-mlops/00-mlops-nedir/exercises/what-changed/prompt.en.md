In an ML system three things can change: code, data and model. Each version is written as a dictionary:

- `{"code": "c1", "data": "d1", "model": "m1"}`

The values are the identity of each part. If the identity changed, the part changed.

Write the function `review(old, new)`. It compares the old and the new version and returns:

- If nothing changed: `"nothing"`
- If the code or the data changed but the model is the same: `"retrain"` (the model is out of date)
- If the model changed but the code and the data are the same: `"unknown model"` (where did this model come from?)
- If the model changed and so did the code or the data: `"ok"`

**Expected output:**

```
nothing
retrain
unknown model
ok
```
