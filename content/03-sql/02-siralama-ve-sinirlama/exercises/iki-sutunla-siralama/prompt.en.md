This time we sort on two criteria.

Sort the products **alphabetically by category first**, then **from
expensive to cheap inside each category**. Columns: `kategori`, `ad`,
`fiyat`.

```
kategori    ad         fiyat
----------  ---------  --------
Aksesuar    Webcam     1150.00
Aksesuar    Kulaklik   890.00
...
Bilgisayar  Laptop     24500.00
...
```

The thing to watch: `DESC` applies only to the column it is written on.
The category stays ascending, the price becomes descending.
