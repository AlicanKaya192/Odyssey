Bölümün üç aracını birden kullanıyoruz.

Şu **üç koşulu birden** sağlayan ürünleri getir:

- kategorisi `Accessory` ya da `Display`,
- fiyatı 200 ile 2000 arasında (iki uç dahil),
- `supplier_code` sütunu **boş değil**.

Sütunlar: `name`, `category`, `price`. Pahalıdan ucuza sırala.

```
name        category   price 
----------  ---------  ------
Microphone  Accessory  1320.0
Webcam      Accessory  1150.0
...
```

Sonuç dört satır olmalı. Beş bulduysan büyük ihtimalle son koşulu
atlamışsındır: fiyatı ve kategorisi uyan ama tedarikçisi kayıtlı olmayan
bir ürün var.
