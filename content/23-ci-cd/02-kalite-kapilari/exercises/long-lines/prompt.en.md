The simplest rule of a format gate: lines should not be longer than a limit.

Write the function `long_lines(source, limit)`. `source` is a text with many lines:

- Split the text into lines: `source.split("\n")`
- Return a list of the numbers of the lines whose length is **greater** than `limit`.
- Lines are counted from 1.

`SAMPLE` is ready; the lines below call your function.

**Expected output:**

```
[4]
[4]
[3]
```
