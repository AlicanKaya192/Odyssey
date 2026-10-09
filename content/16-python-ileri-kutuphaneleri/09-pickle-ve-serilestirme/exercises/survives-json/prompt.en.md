Write the function `survives_json(obj)`: write `obj` with `json.dumps`,
read it back with `json.loads` and return `True` if the result is **equal** to
the original. If JSON cannot write it (`TypeError`) or what comes back is
different (a tuple becomes a list, a number key becomes a string), return
`False`.

**Expected output:**

```
True
False
False
False
```
