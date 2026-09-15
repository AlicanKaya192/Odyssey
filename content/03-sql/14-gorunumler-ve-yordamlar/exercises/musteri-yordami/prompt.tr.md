Bir müşterinin siparişlerini getiren bir **saklı yordam** kur:
`dbo.customer_orders`. Tek parametresi `@customer_id` (`INT`).
Sütunlar: `id`, `order_date`, `status`; `order_date`'e göre sıralı.

Denetim yordamı iki kez çağırıyor:

```sql
EXEC dbo.customer_orders @customer_id = 1;
EXEC dbo.customer_orders @customer_id = 4;
```

```
id    order_date  status
----  ----------  ---------
1001  2026-01-08  shipped
1003  2026-02-02  shipped
1006  2026-03-03  cancelled
```

(4 numaralı müşteri için iki satır: 1005 ve 1009.)

Parametre adıyla çağrıldığı için adı tam olarak `@customer_id` olmalı.
Görünümün aksine yordamın içinde `ORDER BY` yazılabiliyor.

Kurduğun şeyi aynı kodda denemek istersen araya `GO` yaz: `CREATE`
kendi toplu işinde olmak zorunda, `GO`'suz altına yazılan bir sorgu
sözdizimi hatası veriyor. Her çalıştırma sonunda geri alındığı için bir
sonraki çalıştırmada aynı adla yeniden kurabilirsin.
