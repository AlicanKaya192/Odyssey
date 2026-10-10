`store_totals(stores, sales, order)` should draw the stores' **total** sales
with `sns.barplot`: `estimator="sum"`, no confidence interval
(`errorbar=None`), store order `order`. Save it as `totals.png`, close the
figure and return the bar heights (1 place) as a list. The starter code uses
the default: it draws the mean.

**Expected output:**

```
[330.0, 150.0, 90.0]
```
