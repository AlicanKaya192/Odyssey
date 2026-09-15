Her siparişi tek satırda özetleyen bir **görünüm** kur: `dbo.order_summary`.
İptal edilenler dahil bütün siparişler.

Sütunlar: `id`, `order_date`, `customer` (müşterinin adı), `employee`
(çalışanın adı; çalışanı yoksa `'Unassigned'`), `item_count` (kalem
sayısı), `total` (tutar).

Denetim `SELECT ... FROM dbo.order_summary ORDER BY id;` ile okuyor:

```
id    order_date  customer       employee     item_count  total
----  ----------  -------------  -----------  ----------  --------
1001  2026-01-08  Nova Retail    Ceren Aksoy  3           1815.00
1002  2026-01-15  Bright Office  Ceren Aksoy  2           30900.00
1003  2026-02-02  Nova Retail    Deniz Kaya   1           2340.00
1004  2026-02-11  Delta Systems  Unassigned   2           1600.00
...
```

On siparişin onu da görünümde olmalı. İki siparişin çalışanı yok;
`JOIN` onları düşürüyor. Bölümler: birleştirme (06), `COALESCE` (03),
gruplama (05), görünüm (14).
