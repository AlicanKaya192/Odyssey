Write the function `module_kind(name)` and check in order: if it is in
`sys.builtin_module_names` return `"built-in"`, if it is in
`sys.stdlib_module_names` return `"standard"`, if
`importlib.util.find_spec(name)` finds something return `"third-party"`,
otherwise return `"missing"`.

**Expected output:**

```
math built-in
json standard
numpy third-party
no_such_module_x missing
```
