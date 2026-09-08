The `urunler` table also has a `tedarikci_kod` column, and **for some
products it is empty.**

Bring back the `ad` and `kategori` of the products where that column is
empty, in alphabetical order.

```
ad           kategori
-----------  --------
Kulaklik     Aksesuar
Ofis Paketi  Yazilim
Projeksiyon  Ekran
```

**Careful:** write `WHERE tedarikci_kod = NULL` and you get no rows and no
error. `NULL` is not a value but the absence of one; it cannot be
compared.

Press the **Tables** button if you want to see the table; the empty cells
show up there as `NULL`.
