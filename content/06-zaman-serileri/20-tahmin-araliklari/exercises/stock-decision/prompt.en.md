How many should be produced each morning? Every demand that cannot be met
is a loss of 4 units, every product that cannot be sold a loss of 1.

In the starter code `past`, `base` and `actual` are ready (as in the previous
exercise).

**What to do:**

1. Write the function `cost(order)`. `order` is the quantity produced each day
   (a series):
   - short: `(actual - order).clip(lower=0)`
   - over: `(order - actual).clip(lower=0)`
   - return four things as a tuple: the number of days the stock ran out, the
     total short, the total over, the total cost (`4 * short + 1 * over`); all
     whole numbers.
2. For `q = 0.5, 0.8, 0.9, 0.95` the production rule is
   `base + past.quantile(q)`. For each print `q` together with the result of
   `cost`.
3. Compute and print the quantile the formula says: `4 / (4 + 1)`.
4. Print the `q` of the rule with the lowest cost among the four and the
   percentage it saves over the point forecast (`q = 0.5`), as a whole number,
   on one line.

**Expected output:**

```
0.5 (178, 2333, 2730, 12062)
0.8 (73, 609, 6130, 8566)
0.9 (32, 230, 8313, 9233)
0.95 (14, 119, 10032, 10508)
0.8
0.8 29
```

The lowest cost is at the quantile the formula says. Producing as many as the
point forecast leaves you out of stock on half the days; too much caution
(`q = 0.95`) swells the waste and raises the cost again. The same forecasting
method, the same data: the only difference is bringing the uncertainty and the
costs into the decision.
