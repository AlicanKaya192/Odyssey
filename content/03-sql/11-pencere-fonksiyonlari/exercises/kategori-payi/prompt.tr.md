İptal edilmeyen siparişlerde her kategorinin cirosunu ve toplam cirodaki
**yüzde payını** göster.

Sütunlar: `category_code`, `revenue`, `share`. `share` yüzde olarak,
virgülden sonra iki basamak (`DECIMAL(5,2)`). `revenue`'ya göre büyükten
küçüğe sırala.

```
category_code  revenue   share
-------------  --------  -----
COM            67900.00  68.47
DIS            12800.00  12.91
ACC            12165.00  12.27
SOF            6300.00   6.35
```

Payların toplamı 100.

Üç tablo gerekiyor: tutar `order_items`'ta, kategori `products`'ta, iptal
bilgisi `orders`'ta. Toplam ciroyu ayrı bir sorguyla bulmana gerek yok —
grupların toplamını her satıra yazan bir pencere var.

İptal edilenleri unutursan SOF `8700.00` çıkıyor ve bütün paylar kayıyor.
