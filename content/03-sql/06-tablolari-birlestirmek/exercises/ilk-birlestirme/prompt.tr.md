Bu bölümden itibaren **sekiz tablolu** bir sipariş veritabanıyla
çalışıyorsun. Hepsini **Tablolar** düğmesinden görebilirsin.

`products` tablosunda kategorinin yalnızca **kodu** var (`ACC`, `DIS`...);
adı `categories` tablosunda duruyor.

Her ürünün adını ve kategorisinin **adını** getir.

Sütunlar: `product` ve `category`. Ürün adına göre sırala.

```
product    category 
---------  ---------
Antivirus  Software 
Cable      Accessory
...
```

Sonuç on iki satır olmalı — her ürünün kategorisi kayıtlı.

**Dikkat:** iki tabloda da `name` adında bir sütun var. Hangisini
istediğini söylemezsen `Ambiguous column name` hatası alırsın.
