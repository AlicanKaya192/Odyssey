`step_param(c)` should build a `Pipeline` with the steps `("scale",
StandardScaler())` and `("model", LogisticRegression())`, set the model's `C`
to `c` with `set_params` and return `[step_names, model_C]`. The starter code
writes `set_params(C=c)` and fails.

**Expected output:**

```
[['scale', 'model'], 0.1]
```
