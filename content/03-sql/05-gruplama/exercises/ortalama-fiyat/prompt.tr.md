Her kategori için üç bilgi birden getir: kaç ürün olduğu, en ucuzunun ve
en pahalısının fiyatı.

Sütunlar: `category`, `item_count`, `cheapest`, `priciest`. Kategoriye göre
sırala.

```
category   item_count  cheapest  priciest
---------  ----------  --------  --------
Accessory  6           95.0      1320.0  
Computer   2           18900.0   24500.0 
...
```

Aynı `GROUP BY` içinde istediğin kadar toplama işlevi kullanabiliyorsun;
hepsi aynı gruplara uygulanıyor.
