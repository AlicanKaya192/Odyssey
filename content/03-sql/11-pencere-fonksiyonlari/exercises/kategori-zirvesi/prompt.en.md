Bring back the most expensive product in each category.

Columns: `category_code`, `name`, `price`. Sort by `category_code`. The
result is four rows.

```
category_code  name          price
-------------  ------------  --------
ACC            Microphone    1320.00
COM            Laptop        24500.00
DIS            Projector     7400.00
SOF            Office Suite  2400.00
```

`GROUP BY` with `MAX(price)` finds the highest price but not the
product's **name**. Number the products in each category from most to
least expensive and keep the number 1s.

Both short cuts raise an error: a window function cannot be written
inside `WHERE`, and its alias is not visible in the same query's
`WHERE`. Put the numbered query inside `FROM (...)` and filter outside.
