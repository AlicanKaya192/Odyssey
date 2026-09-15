Her kategorinin en pahalı ürününü getir.

Sütunlar: `category_code`, `name`, `price`. `category_code`'a göre
sırala. Sonuç dört satır.

```
category_code  name          price
-------------  ------------  --------
ACC            Microphone    1320.00
COM            Laptop        24500.00
DIS            Projector     7400.00
SOF            Office Suite  2400.00
```

`GROUP BY` ile `MAX(price)` en yüksek fiyatı buluyor ama ürünün **adını**
getirmiyor. Ürünleri her kategoride pahalıdan ucuza numaralandır ve 1
numaraları al.

İki kısa yol da hata veriyor: pencere işlevi `WHERE` içinde yazılamıyor,
takma adı da aynı sorgunun `WHERE`'inde görünmüyor. Numaralı sorguyu
`FROM (...)` içine al, süzmeyi dışarıda yap.
