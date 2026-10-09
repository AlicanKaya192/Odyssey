Let `safe_int(text)` convert the text to `int`; if that fails
(`ValueError`), log the error with `log.exception("bad number: %s", text)`
and return `None`. The logger's handler is ready: it writes records into
`buffer`.

**Expected output:**

```
42 None
ERROR: bad number: 4x
ValueError
```
