İptal edilmeyen **en az iki** siparişi olan müşterileri getir: adı, sipariş
sayısı, ilk ve son sipariş tarihi ve ikisi arasındaki gün sayısı.

Sütunlar: `name`, `orders`, `first_order`, `last_order`, `span_days`.
`span_days` (büyükten küçüğe), sonra `name` ile sırala.

```
name           orders  first_order  last_order  span_days
-------------  ------  -----------  ----------  ---------
Bright Office  2       2026-01-15   2026-03-22  66
Delta Systems  2       2026-02-11   2026-04-17  65
Helix Studio   2       2026-02-19   2026-04-01  41
Nova Retail    2       2026-01-08   2026-02-02  25
```

Nova Retail'in üçüncü siparişi iptal edilmiş; sayılmıyor. "En az iki"
bir satırın değil bir grubun koşulu.
