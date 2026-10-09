Write the function `find_all(text, pattern)` with **naive search**: it returns
all positions where the pattern starts in the text, in order; overlapping ones
count too (`"aa"` in `"aaaa"`: `0, 1, 2`).

No `find`, `index`, `count`, `startswith`: compare the letters yourself.

**Expected output:**

```
[0, 7]
[0, 1, 2]
[]
```
