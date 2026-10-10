`mean_cost(fn_cost, weight)` should turn the cost (a false positive costs 1, a
false negative `fn_cost`) into a scorer with `make_scorer` and return the
5-fold mean cost of `LogisticRegression(class_weight=weight)` as a
**positive** number with 1 place. In the starter code the scorer does not
know the cost should be small.

**Expected output:**

```
26.4
21.6
```
