For orders that were not cancelled, show each customer's total spending
and **its difference from the customer average**.

Columns: `name`, `total`, `vs_avg`. Sort by `total`, largest first. A
customer with no orders is not on the list.

```
name           total     vs_avg
-------------  --------  ---------
Helix Studio   49690.00  29857.00
Bright Office  34100.00  14267.00
Delta Systems  6710.00   -13123.00
Orion Labs     4510.00   -15323.00
Nova Retail    4155.00   -15678.00
```

The average is the average of the five customers' totals (`19833.00`) —
not of the lines or the orders. Name the customer totals once with `WITH`
and you can use the same name both in the list and for the average.
