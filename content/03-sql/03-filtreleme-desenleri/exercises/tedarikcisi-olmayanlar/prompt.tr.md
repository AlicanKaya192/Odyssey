`urunler` tablosunda bir de `tedarikci_kod` sütunu var ve **bazı ürünlerde
boş.**

Bu sütunu boş olan ürünlerin `ad` ve `kategori` bilgisini alfabetik sırada
getir.

```
ad           kategori
-----------  --------
Kulaklik     Aksesuar
Ofis Paketi  Yazilim
Projeksiyon  Ekran
```

**Dikkat:** `WHERE tedarikci_kod = NULL` yazarsan hiçbir satır gelmez ve
hata da almazsın. `NULL` bir değer değil, değerin yokluğu; onunla
karşılaştırma yapılamıyor.

Tabloyu görmek istersen **Tablolar** düğmesine basabilirsin; boş hücreler
orada `NULL` diye görünüyor.
