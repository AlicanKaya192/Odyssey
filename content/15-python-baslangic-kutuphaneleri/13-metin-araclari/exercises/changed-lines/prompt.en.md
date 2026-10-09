Write the function `changed_lines(old, new)`: from the
`difflib.unified_diff(old, new, lineterm="")` difference of two lists of
lines, return only the **line** changes starting with `+` or `-` as a list;
the header lines starting with `+++` and `---` stay out.

**Expected output:**

```
-b = 2
+b = 3
+print('done')
```
