Two run records (`a`, `b`) are given as dictionaries: `config`, `data` (the fingerprint), `library` (the version) and `accuracy`.

Write the function `compare_runs(a, b)`:

- Find which of the `config`, `data` and `library` fields changed, **in that order**.
- If any changed, return `"changed: "` followed by their names separated by a comma and a space: `"changed: data, library"`.
- If none changed, return `"reproducible"` if the accuracy is the same and `"not reproducible"` if it differs: if the result changed while the inputs stayed the same, the training is not reproducible.

**Expected output:**

```
reproducible
not reproducible
changed: data
changed: config, library
```
