`fill(template, values)` should find the `{name}` placeholders in the
template (`\{(\w+)\}`). If any is missing, return `[None, missing]`
without filling (in the template's order). If all are there, replace every
placeholder with `str(value)` and return `[text, []]`.

**Expected output:**

```
Hello Ada, order ORD-48213 is shipped.
[None, ['order', 'status']]
```
