İptal edilmeyen her siparişin tutarını ve **o güne kadar biriken
ciroyu** göster.

Sütunlar: `id`, `order_date`, `total`, `running_total`. `order_date`'e
göre sırala.

```
id    order_date  total     running_total
----  ----------  --------  -------------
1001  2026-01-08  1815.00   1815.00
1002  2026-01-15  30900.00  32715.00
1003  2026-02-02  2340.00   35055.00
...
1010  2026-04-17  5110.00   99165.00
```

Siparişin tutarı kalemlerinde: `orders` ile `order_items`'ı birleştirip
siparişe göre grupla. İptal edilen sipariş (1006) ne tutarda ne birikimde
görünmeli.

Birikimli toplam, grup toplamının üstüne yazılan bir pencere. İçteki ve
dıştaki toplamı karıştırma: biri siparişin tutarı, öteki o tarihe kadar
gelenlerin toplamı.
