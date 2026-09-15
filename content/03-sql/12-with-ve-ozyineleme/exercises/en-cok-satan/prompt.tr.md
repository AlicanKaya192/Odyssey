İptal edilmeyen siparişlerde her kategorinin **adet olarak** en çok satan
ürününü getir.

Sütunlar: `category_code`, `name`, `units`. `category_code`'a göre
sırala.

```
category_code  name       units
-------------  ---------  -----
ACC            Cable      15
COM            Laptop     2
DIS            Monitor    4
SOF            Antivirus  5
```

İki adım var: önce ürün başına satılan adet, sonra her kategoride o
adetlere göre sıra. İkisini iki ayrı CTE olarak yaz; ikincisi birincinin
adını kullansın.
