The `bumpy` function has more than one dip. `multi_start(starts)` should run
`optimize.minimize(bumpy, x0=[s])` from each starting point and pick the result
with the **smallest** value. Return `[x, value]` (3 places each). The starter
code tries only the first point.

**Expected output:**

```
[-0.512, -0.973]
[1.537, -0.759]
```
