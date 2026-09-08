Stok değeri (fiyat çarpı stok) **50000'den büyük** olan ürünleri getir.

Sütunlar: `ad`, `fiyat`, `stok`, `stok_degeri`. Stok değerine göre
büyükten küçüğe sırala.

```
ad           fiyat     stok  stok_degeri
-----------  --------  ----  -----------
Ofis Paketi  2400.00   99    237600.00
Laptop       24500.00  5     122500.00
...
```

Sonuç üç satır olmalı.

Buradaki nokta şu: `WHERE` içinde **takma adı** kullanamıyorsun ama
**ifadenin kendisini** kullanabiliyorsun. Yani hesabı iki kez yazacaksın —
bir kez `SELECT` içinde ada bağlarken, bir kez `WHERE` içinde süzerken.

`ORDER BY`'da takma ad yeterli; o en son çalışıyor.
