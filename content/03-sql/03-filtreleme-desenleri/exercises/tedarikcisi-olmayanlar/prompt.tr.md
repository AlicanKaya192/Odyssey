`products` tablosunda bir de `supplier_code` sütunu var ve **bazı ürünlerde
boş.**

Bu sütunu boş olan ürünlerin `name` ve `category` bilgisini alfabetik sırada
getir.

```
name          category 
------------  ---------
Headset       Accessory
Office Suite  Software 
Projector     Display  
```

**Dikkat:** `WHERE supplier_code = NULL` yazarsan hiçbir satır gelmez ve
hata da almazsın. `NULL` bir değer değil, değerin yokluğu; onunla
karşılaştırma yapılamıyor.

Tabloyu görmek istersen **Tablolar** düğmesine basabilirsin; boş hücreler
orada `NULL` diye görünüyor.
