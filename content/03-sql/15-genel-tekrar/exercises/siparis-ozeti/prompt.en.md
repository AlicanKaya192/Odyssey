Create a **view** that sums up each order on a single row:
`dbo.order_summary`. All orders, the cancelled ones included.

Columns: `id`, `order_date`, `customer` (the customer's name), `employee`
(the employee's name; `'Unassigned'` if there is none), `item_count` (the
number of lines), `total` (the amount).

The check reads it with `SELECT ... FROM dbo.order_summary ORDER BY id;`:

```
id    order_date  customer       employee     item_count  total
----  ----------  -------------  -----------  ----------  --------
1001  2026-01-08  Nova Retail    Ceren Aksoy  3           1815.00
1002  2026-01-15  Bright Office  Ceren Aksoy  2           30900.00
1003  2026-02-02  Nova Retail    Deniz Kaya   1           2340.00
1004  2026-02-11  Delta Systems  Unassigned   2           1600.00
...
```

All ten orders must be in the view. Two orders have no employee; `JOIN`
drops them. Sections: joins (06), `COALESCE` (03), grouping (05), views
(14).
