Write a decorator factory named `retry(times)`:

- It tries the wrapped function at most `times` times; if a `ValueError`
  comes, it writes `log.warning("retry %d: %s", attempt, error)` and tries
  again.
- If the last attempt fails too, it raises the error again (`raise`).
- The name is kept with `functools.wraps`.

The expected output:

```
ok 3 flaky
WARNING retry 1: try 1
WARNING retry 2: try 2
```

**Expected output:**

```
ok 3 flaky
WARNING retry 1: try 1
WARNING retry 2: try 2
```
