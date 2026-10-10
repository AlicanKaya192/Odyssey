`plan(profits, hours, limits)` takes the profit per product (`profits`), the
hours per product on each machine (`hours[machine][product]`) and the machine
hour limits (`limits`). It should find the production that **maximises**
profit with `optimize.linprog` (units 0 or more) and return `{"units":
units, "profit": profit}` (units 2, profit 1 place). `linprog` minimises: give
the negative profits.

**Expected output:**

```
[25.0, 7.5] 1125.0
```
