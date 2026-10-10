`save_and_check(path)` saves and loads the model and returns `[keys, same]`. It
should also add the column list (`"columns": list(X.columns)`) to the
dictionary and save the file with `compress=3`.

**Expected output:**

```
[['columns', 'model'], True]
```
