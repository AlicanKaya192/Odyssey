For orders that were not cancelled, bring back each category's
best-selling product **by units**.

Columns: `category_code`, `name`, `units`. Sort by `category_code`.

```
category_code  name       units
-------------  ---------  -----
ACC            Cable      15
COM            Laptop     2
DIS            Monitor    4
SOF            Antivirus  5
```

There are two steps: first the units sold per product, then a ranking by
those units within each category. Write them as two separate CTEs; the
second one uses the first one's name.
