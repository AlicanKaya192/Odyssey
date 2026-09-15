Her sipariş için, **aynı müşterinin** bir önceki siparişinden bu yana kaç
gün geçtiğini göster. Müşterinin ilk siparişinde bu değer boş (`NULL`)
kalsın. İptal edilenler de dahil, bütün siparişler.

Sütunlar: `customer_id`, `id`, `order_date`, `gap_days`. Önce
`customer_id`, sonra `order_date` ile sırala.

```
customer_id  id    order_date  gap_days
-----------  ----  ----------  --------
1            1001  2026-01-08  NULL
1            1003  2026-02-02  25
1            1006  2026-03-03  29
2            1002  2026-01-15  NULL
2            1008  2026-03-22  66
...
```

Önceki satırın değerini getiren işlev `LAG`. Gün farkı onuncu bölümdeki
`DATEDIFF`.

Dikkat: bütün siparişler tek bir sıraya konursa 1003'ün "öncesi" 1002
olur — başka bir müşterinin siparişi. Her müşterinin kendi sırası olmalı.
