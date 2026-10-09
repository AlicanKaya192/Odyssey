Write the function `kmp_count(text, pattern)` with **KMP**: it returns how
many times the pattern occurs in the text; overlapping ones count too.
`prefix_table` is ready.

After a match do not reset `k`: `k = table[k - 1]`. No `find`, `index`,
`count`, `startswith`.

**Expected output:**

```
3
18
0
```
