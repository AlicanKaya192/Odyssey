`replace_first(names, new)` turns the list into an array, replaces the first
item with `new` and returns a list; but because the array's text width is
fixed by the longest original name, `new` gets cut. Build the array with
**`dtype=object`** so the text is not cut.

**Expected output:**

```
['hello', 'cde']
```
