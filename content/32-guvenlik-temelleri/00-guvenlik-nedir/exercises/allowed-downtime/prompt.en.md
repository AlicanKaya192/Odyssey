Write the function `allowed_downtime(percent, days)`: over a period of
`days` days, how much downtime does a `percent` availability promise
allow?

- First compute the allowed minutes: `days * 24 * 60 * (1 - percent / 100)`.
- Round it to the nearest whole minute (`round`).
- Return the result as an `(hours, minutes)` tuple. `divmod(n, 60)` gives
  both at once.

**Expected output:**

```
(0, 43)
(87, 36)
(0, 53)
```
