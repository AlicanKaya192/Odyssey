`python -c "code"` is the way to give Python code directly instead of a
file: `python -c "print(1 + 1)"` prints `2`.

**What to do:** in the `python:3.13-slim` image, write the `CMD` line that
prints the result of `7 * 6` with `python -c` when the container runs. In
the bracketed form the command has three parts: `"python"`, `"-c"` and the
code itself.

**Expected output:**

```
42
```
