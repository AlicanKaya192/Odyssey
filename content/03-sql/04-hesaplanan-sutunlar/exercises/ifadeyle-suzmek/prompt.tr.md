Stok değeri (fiyat çarpı stok) **50000'den büyük** olan ürünleri getir.

Sütunlar: `name`, `price`, `stock`, `stock_value`. Stok değerine göre
büyükten küçüğe sırala.

```
name          price    stock  stock_value
------------  -------  -----  -----------
Office Suite  2400.0   99     237600.0   
Laptop        24500.0  5      122500.0   
...
```

Sonuç üç satır olmalı.

Buradaki nokta şu: `WHERE` içinde **takma adı** kullanamıyorsun ama
**ifadenin kendisini** kullanabiliyorsun. Yani hesabı iki kez yazacaksın —
bir kez `SELECT` içinde ada bağlarken, bir kez `WHERE` içinde süzerken.

`ORDER BY`'da takma ad yeterli; o en son çalışıyor.
