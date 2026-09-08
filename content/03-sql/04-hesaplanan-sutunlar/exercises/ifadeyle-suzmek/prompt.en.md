Bring back the products whose stock value (price times stock) is **above
50000**.

Columns: `ad`, `fiyat`, `stok`, `stok_degeri`. Sort by stock value,
largest first.

```
ad           fiyat     stok  stok_degeri
-----------  --------  ----  -----------
Ofis Paketi  2400.00   99    237600.00
Laptop       24500.00  5     122500.00
...
```

The result should be three rows.

The point here: you cannot use the **alias** inside `WHERE`, but you can
use **the expression itself**. So you will write the calculation twice —
once in `SELECT` where you name it, once in `WHERE` where you filter.

In `ORDER BY` the alias is enough; that runs last.
