`needs_preflight(method, headers)` should return `True` if the request
is not simple. A simple request: the method is in `SIMPLE_METHODS`; every
header name (in lower case) is in `SIMPLE_HEADERS`; if there is a
`content-type`, the part of its value before `;` (lower case, `strip`)
is in `SIMPLE_TYPES`.

**Expected output:**

```
False
False
True
True
True
```
