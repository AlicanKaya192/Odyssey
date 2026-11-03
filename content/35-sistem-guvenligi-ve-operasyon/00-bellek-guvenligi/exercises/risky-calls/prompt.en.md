`risky_calls(lines)` should find calls to functions that write without
knowing the size in lines of C source: `gets`, `strcpy`, `strcat`,
`sprintf`. Each finding is `"<line no>: <name>"` (lines counted from 1), in
line order, left to right within a line. Safe counterparts such as `fgets`
or `snprintf` must **not** be caught: use a word boundary (`\b`) and a
following `(` in the regular expression.

**Expected output:**

```
3: strcpy
5: gets
5: strcat
```
