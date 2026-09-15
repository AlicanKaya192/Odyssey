Bring back the customers with **at least two** orders that were not
cancelled: their name, number of orders, first and last order date and
the number of days between them.

Columns: `name`, `orders`, `first_order`, `last_order`, `span_days`.
Sort by `span_days` (largest first), then `name`.

```
name           orders  first_order  last_order  span_days
-------------  ------  -----------  ----------  ---------
Bright Office  2       2026-01-15   2026-03-22  66
Delta Systems  2       2026-02-11   2026-04-17  65
Helix Studio   2       2026-02-19   2026-04-01  41
Nova Retail    2       2026-01-08   2026-02-02  25
```

Nova Retail's third order was cancelled; it does not count. "At least
two" is a condition on a group, not on a row.
