`add_scores(a, b)` turns two lists of scores into `int8` arrays and adds
them item by item; `100 + 100` overflows and comes out negative. Turn the
arrays into **`int16`** before adding and return the result as a list.

**Expected output:**

```
[200, 130]
```
