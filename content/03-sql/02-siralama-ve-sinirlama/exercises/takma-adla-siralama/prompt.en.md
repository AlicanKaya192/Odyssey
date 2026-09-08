This exercise brings the three parts of the section together.

Bring back the products that are **in stock** (`stok` above zero), return
`ad` under the heading `urun` and `fiyat` under `tutar`, and sort the
result **by `tutar` from largest to smallest**.

```
urun      tutar
--------  ---------
Laptop    24500.00
Masaustu  18900.00
...
```

The result should be six rows.

The real point here: **`ORDER BY` can use the alias.** In the previous
section, trying the same alias inside `WHERE` would have raised an error —
`WHERE` runs early, `ORDER BY` runs late.
