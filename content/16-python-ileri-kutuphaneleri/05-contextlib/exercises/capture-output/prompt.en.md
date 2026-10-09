Write the function `capture(func, *args)`: while running `func(*args)`,
redirect everything it prints into an `io.StringIO` with `redirect_stdout`,
and return the captured text.

**Expected output:**

```
'hello ada\nbye\n'
```
