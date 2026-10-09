Write the function `kth_smallest(values, k)` with **quickselect**: it returns
the `k`-th smallest value counting from 0 (`k = 0` is the smallest). Choose the
pivot with `random.choice`; split the items into smaller / equal / larger and
continue only into the part where the wanted rank falls.

No `sorted` and no `sort`.

**Expected output:**

```
1 4 9
497600
```
