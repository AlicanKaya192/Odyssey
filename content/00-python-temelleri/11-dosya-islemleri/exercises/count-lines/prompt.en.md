A file called `report.txt` has been placed next to your code. Some of its
lines are empty.

**What you need to do:**

1. Read the file `report.txt`.
2. Hold the **total** number of lines in a variable called `total`.
3. Hold the number of **non-empty** lines in a variable called `filled`.
4. Print `total` first, then `filled`.

**Expected output:**

```
5
3
```

Note: a line may contain nothing but whitespace. If it is empty after
`strip()`, it counts as empty.

> For the emptiness check you can write `if not line.strip():` — an empty
> string counts as `False` in Python.
