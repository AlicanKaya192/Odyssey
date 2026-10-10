`to_long(rows, months)` takes a wide table where each row is `[city, month1,
month2, ...]`; the column names are `["city", *months]`. It should turn it
into the long form with `melt` (`var_name="month"`, `value_name="sales"`)
and return the rows as a `[city, month, sales]` list (`.values.tolist()`).
**Do not write a loop.**

**Expected output:**

```
['Izmir', 'jan', 80]
['Ankara', 'jan', 120]
['Izmir', 'feb', 95]
['Ankara', 'feb', 110]
```
