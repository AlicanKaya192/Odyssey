Write the function `sla_report(outages, days, target)`:

- `outages`: the list of outages in the period, in minutes,
- `days`: the number of days in the period, `target`: the promised
  percentage.

Compute the availability reached as a percentage rounded to 3 digits and
return a `(percent, kept)` tuple. The promise is kept if the rounded
percentage is equal to or greater than the target.

**Expected output:**

```
(99.903, True)
(99.891, False)
(100.0, True)
```
