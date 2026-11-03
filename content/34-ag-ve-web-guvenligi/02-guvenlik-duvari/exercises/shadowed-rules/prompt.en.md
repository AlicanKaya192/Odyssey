Rules are `[port, action]` lists; `port` is a number or `"any"`. If
there is a rule above a rule whose port is `"any"` or the **same** port,
that rule never runs. `shadowed(rules)` should return the numbers of these
rules (starting from 1) as a list.

**Expected output:**

```
[2]
[]
[2, 4]
```
