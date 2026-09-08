Her müşterinin kaç siparişi olduğunu getir.

**Hiç sipariş vermemiş müşteriler de listede olmalı** ve yanlarında `0`
yazmalı.

Sütunlar: `customer` ve `order_count`. Önce sayıya göre büyükten küçüğe,
eşitlik olursa müşteri adına göre sırala.

```
customer       order_count
-------------  -----------
Nova Retail    3          
Bright Office  2          
Delta Systems  2          
Helix Studio   2          
...
```

Sonuç altı satır olmalı.

Burada iki tuzak birden var:

1. Düz `JOIN` yazarsan siparişi olmayan müşteri **listeden düşüyor**.
2. `COUNT(*)` yazarsan o müşteri için **1** çıkıyor, 0 değil — çünkü
   birleştirme onun için boş sütunlu bir satır üretiyor ve `COUNT(*)`
   satırları sayıyor.

İkincisinden kaçınmak için sağ tablonun bir sütununu saymak gerekiyor.
