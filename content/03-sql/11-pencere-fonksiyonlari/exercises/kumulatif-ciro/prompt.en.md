For every order that was not cancelled, show its amount and **the
revenue built up to that day**.

Columns: `id`, `order_date`, `total`, `running_total`. Sort by
`order_date`.

```
id    order_date  total     running_total
----  ----------  --------  -------------
1001  2026-01-08  1815.00   1815.00
1002  2026-01-15  30900.00  32715.00
1003  2026-02-02  2340.00   35055.00
...
1010  2026-04-17  5110.00   99165.00
```

An order's amount is in its lines: join `orders` with `order_items` and
group by order. The cancelled order (1006) must appear neither in the
amounts nor in the running total.

The running total is a window written on top of the group total. Do not
mix up the inner and the outer sum: one is the order's amount, the other
the total of everything up to that date.
