Fiyatı **kendi kategorisinin** ortalamasından yüksek olan ürünleri
getir.

Sütunlar: `name`, `category_code`, `price`. Ada göre sırala.

```
name     category_code  price  
-------  -------------  -------
Headset  ACC            890.0  
Laptop   COM            24500.0
...
```

Sonuç altı satır olmalı.

İlk alıştırmadaki genel ortalama değil bu: her ürün **kendi
kategorisindeki** ürünlerle karşılaştırılacak. Bir aksesuar 890 TL ile
kategorisinin üstünde kalabilirken, aynı fiyat bilgisayar kategorisinde
ortalamanın çok altında.

Bunun için alt sorgunun dıştaki satıra bağlanması gerekiyor — iki tarafa
farklı takma ad vermen gerekecek.
