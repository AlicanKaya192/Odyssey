Write the decorator `count_calls(func)`: on every call the wrapper
increases the `wrapper.calls` counter by one and returns the real function's
result; the counter starts at 0. Keep the real function's name with
`@wraps(func)`. The lines below try the decorator on `square`.

**Expected output:**

```
5
square 81
```
