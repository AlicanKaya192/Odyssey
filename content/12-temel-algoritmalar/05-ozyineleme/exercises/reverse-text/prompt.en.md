Write the function `reverse_text(text)` **recursively**: it returns the string
reversed. Do not use a loop, `reversed` or `[::-1]`.

- `reverse_text("python")` → `"nohtyp"`
- `reverse_text("")` → `""`

**The idea:** set the first letter aside; find the reverse of the rest and
add the first letter at its end.

**Expected output:**

```
nohtyp
a
level
```
