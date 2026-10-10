`faster(f, g)` should measure two functions with
`timeit.repeat(..., number=3, repeat=3)` (the smallest time) and return the
**name of the faster one** (`__name__`). The expected output:

```
quick quick
```

**Expected output:**

```
quick quick
```
