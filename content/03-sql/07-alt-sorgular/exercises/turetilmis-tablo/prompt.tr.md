**En az iki siparişi** olan müşterilerin id'sini ve sipariş sayısını
getir.

Sütunlar: `customer_id` ve `order_count`. Önce sayıya göre büyükten
küçüğe, eşitlik olursa id'ye göre sırala.

```
customer_id  order_count
-----------  -----------
1            3          
2            2          
...
```

Sonuç dört satır olmalı.

Bu soruyu `HAVING` ile de çözebilirsin ve daha kısa olurdu. Ama burada
**türetilmiş tabloyu** öğreniyoruz: gruplamayı `FROM` içindeki bir alt
sorguda yap, sonucunu dışarıdan süz.

Bu kalıp, gruplama sonucunu başka bir tabloyla birleştirmek gerektiğinde
tek yol oluyor.

**Takma ad zorunlu:** parantezi kapattıktan sonra geçici tabloya bir ad
vermezsen sözdizimi hatası alıyorsun.
