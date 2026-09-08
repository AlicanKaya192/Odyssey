Her kategoride kaç ürün olduğunu getir.

Sütunlar: `category` ve `item_count`. Kategoriye göre alfabetik sırala.

```
category   item_count
---------  ----------
Accessory  6         
Computer   2         
Display    2         
Software   2         
```

`GROUP BY` olmadan `COUNT(*)` bütün tablo için **tek bir sayı** veriyor
(12). Kategori başına ayrı sayı istiyorsan satırları önce kümelere ayırman
gerekiyor.

Sonuç dört satır olmalı — tabloda dört farklı kategori var.
