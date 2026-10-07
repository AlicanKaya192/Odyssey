A container's exit code is the exit code of the program inside it. In
Python, `sys.exit(3)` ends the program with code 3.

**What to do:** write a `CMD` that runs with `python -c`: it should first
print `failing`, then end the program with code **3**. The code is on one
line, the statements separated by semicolons:

```python
import sys; print('failing'); sys.exit(3)
```

Since the bracketed form already uses double quotes, use single quotes in the
Python code (`'failing'`).

**Expected:** the output `failing`, the container's exit code `3`.
