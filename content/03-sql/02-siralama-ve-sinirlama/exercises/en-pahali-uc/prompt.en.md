Bring back the `ad` and `fiyat` of the **three** most expensive products.

```
ad        fiyat
--------  ---------
Laptop    24500.00
Masaustu  18900.00
Monitor   3200.00
```

Two pieces are needed: how many rows you want (`TOP`) and the ordering
that decides **which** rows those are (`ORDER BY`).

Writing `TOP 3` without `ORDER BY` means "three products at random" — the
query runs but does not answer the question you asked.
