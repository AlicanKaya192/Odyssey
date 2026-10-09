Write the function `is_standard(name)`: return `True` if the module name
is in the standard library, otherwise `False`. Do not import the module; look
at the set `sys.stdlib_module_names`.

**Expected output:**

```
json True
csv True
numpy False
requests False
```
