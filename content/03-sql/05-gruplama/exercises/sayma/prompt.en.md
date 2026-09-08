This exercise puts the three forms of `COUNT` side by side. One row,
three columns:

- `total_rows` — the number of rows in the table
- `with_supplier` — the number of rows where `supplier_code` is **filled**
- `distinct_categories` — how many **different** categories there are

```
total_rows  with_supplier  distinct_categories
----------  -------------  -------------------
12          9              4                  
```

All three numbers differ, and that is not an accident: the gap of 12 − 9
says three products have no supplier recorded.

There is no `GROUP BY` here — you are treating the whole table as a single
group.
