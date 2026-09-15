For each carrier, work out the **average number of days** between the
order and the shipment.

Columns: `carrier`, `avg_days`. `avg_days` rounded to **two places**.
Sort by carrier.

```
carrier   avg_days
--------  --------
CityMove  3.00
FastLine  2.67
NorthWay  3.00
```

Three traps at once:

- The order date is in `orders` and the shipment date in `shipments`:
  you have to join the two tables.
- The order matters in `DATEDIFF`: the earlier date first. The other way
  round the result is negative.
- `DATEDIFF` returns a whole number and **the average of whole numbers is
  a whole number too**: FastLine comes out as 2 instead of 2.67. The same
  as the integer division in the fifth section.
