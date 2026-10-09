`debug_value(log, value)` builds the message with an f-string, so it turns
`value` into text even with `DEBUG` off (`calls` grows). Change it to the
`log.debug("value: %s", value)` form: when the record is not written, the
text must never be built.

**Expected output:**

```
0
```
