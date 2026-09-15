For orders that were not cancelled, show each category's revenue in each
month and its percentage share of **that month's** total.

Columns: `month` (the first day of the month), `category_code`,
`revenue`, `share` (`DECIMAL(5,2)`). Sort by `month`, then `revenue`
(largest first).

```
month       category_code  revenue   share
----------  -------------  --------  -----
2026-01-01  COM            24500.00  74.89
2026-01-01  DIS            6400.00   19.56
2026-01-01  ACC            1815.00   5.55
2026-02-01  COM            18900.00  65.90
...
```

Each month's shares add up to 100 within that month. The sections you
use: joining tables (06), grouping (05), dates (10), `WITH` (12),
windows (11).
