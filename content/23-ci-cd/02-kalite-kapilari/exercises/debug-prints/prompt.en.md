`print` lines added while debugging and then forgotten are a common lint rule.

Write the function `find_prints(source)`: return a list of the numbers (from 1) of the lines that **start** with `print(` once their leading spaces are removed.

- `line.strip()` removes the spaces at the start and end of a line.
- `text.startswith("print(")` is `True` if the text starts with `print(`.

A commented-out `# print(...)` does not count: that line starts with `#`.

**Expected output:**

```
[5, 9]
[]
```
