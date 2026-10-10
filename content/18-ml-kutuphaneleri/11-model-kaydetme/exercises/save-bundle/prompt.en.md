`save_bundle(path, threshold)` saves the model in a dictionary and loads it back.
It should also add the `"sklearn"` (`sklearn.__version__`) and `"columns"`
(`COLUMNS`) keys to the dictionary. The function returns `[keys, threshold,
columns]`; two keys are missing in the starter code.

**Expected output:**

```
['columns', 'model', 'sklearn', 'threshold']
0.3
['age', 'income', 'visits', 'score']
```
