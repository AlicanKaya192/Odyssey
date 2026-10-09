Write the function `load_safely(blob)`: override `find_class` in a class
derived from `pickle.Unpickler`; if `(module, name)` is in `ALLOWED`, call the
parent class's `find_class`, otherwise raise `pickle.UnpicklingError`.
`load_safely` returns the loaded object; if it is blocked, it returns the
text `"blocked: <module>.<name>"`. To make the bytes look like a file,
`io.BytesIO(blob)`.

**Expected output:**

```
Counter({'a': 2, 'b': 1, 'c': 1})
blocked: builtins.print
[1, 'x', None]
```
