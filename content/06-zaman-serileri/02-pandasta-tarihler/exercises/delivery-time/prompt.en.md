How many days do orders take to arrive? In `orders_raw.csv` both
columns are troublesome: `ordered_at` is day-first with a time, `delivered_on`
is ISO but empty or `not delivered` in some rows.

**What to do:**

1. Convert `ordered_at` with `format="%d.%m.%Y %H:%M"` and `errors="coerce"`.
2. Convert `delivered_on` with `errors="coerce"`.
3. Compute the delivery time in days:
   `(delivered - ordered.dt.normalize()).dt.days`.
4. Print in order: the number of orders whose time can be computed, the mean
   time (two decimals), the longest time (a whole number), and the number of
   orders that took longer than 3 days.

**Expected output:**

```
230
2.33
8
33
```

In 10 of the 240 orders one side is `NaT`; pandas left them out of the mean.
Without `normalize()` the order's clock time would be subtracted from the
difference, and orders placed in the evening would look one day shorter.
