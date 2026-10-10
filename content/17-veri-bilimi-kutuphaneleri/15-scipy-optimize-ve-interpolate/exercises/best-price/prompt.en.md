Demand is `1000 - 8 * price`, profit `(price - cost) * demand`.
`best_price(cost, max_price)` should find the price that **maximises** profit
with `minimize_scalar` (`bounds=(cost, max_price)`, `method="bounded"`) and
return `[price, profit]` (2 and 1 places). The starter code minimises the
profit itself.

**Expected output:**

```
[72.5, 22050.0]
[82.5, 14450.0]
```
