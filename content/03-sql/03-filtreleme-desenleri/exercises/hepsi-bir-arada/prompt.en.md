We use three of the section's tools at once.

Bring back the products that satisfy **all three**:

- the category is `Aksesuar` or `Ekran`,
- the price is between 200 and 2000 (both ends included),
- `tedarikci_kod` is **not empty**.

Columns: `ad`, `kategori`, `fiyat`. Sort from expensive to cheap.

```
ad         kategori  fiyat
---------  --------  -------
Mikrofon   Aksesuar  1320.00
Webcam     Aksesuar  1150.00
...
```

The result should be four rows. If you got five you most likely skipped
the last condition: there is a product whose price and category match but
whose supplier is not recorded.
