`find_weak(lines)` should return a list of the numbers (starting at 1)
of the code lines that use the `random` module. A line is marked when:

- it contains `random.`, or the line (with leading spaces removed) starts
  with `from random import`,
- **but** a line that (with leading spaces removed) starts with `#` is a
  comment and is not marked,
- and a line containing `random.SystemRandom` is safe and is not marked.

The starter code searches for `"random" in line`: it also catches `import
random`, `os.urandom` and comments.

**Expected output:**

```
[3, 7]
```
