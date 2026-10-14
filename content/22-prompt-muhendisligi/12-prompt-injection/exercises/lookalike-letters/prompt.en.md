`detect_normalized(text)` should simplify the text before searching it with
the given `DETECT` pattern: turn it into lower case, replace every
character in `LOOKALIKE` with its letter (such as `"1"` → `"i"`) and
squeeze several spaces into one (`" ".join(plain.split())`). Return
`True` if the pattern is found.

**Expected output:**

```
True
True
False
```
