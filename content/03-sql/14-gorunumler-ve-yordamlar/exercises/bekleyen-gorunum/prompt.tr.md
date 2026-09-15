Bekleyen siparişleri gösteren bir görünüm kur: `dbo.pending_orders`.
Sütunlar: `id`, `customer_id`, `order_date`, `status`; yalnızca `status`
değeri `'pending'` olanlar.

```
id    customer_id  order_date  status
----  -----------  ----------  -------
1004  3            2026-02-11  pending
1008  2            2026-03-22  pending
1010  3            2026-04-17  pending
```

Bir şart daha var. Görünümün üstünden `UPDATE` yazılabiliyor ve değişiklik
`orders` tablosuna gidiyor. Biri görünüm üzerinden bir siparişi
`'shipped'` yaparsa sipariş görünümden **sessizce kayboluyor** — ölçüldü.
Senin görünümün bunu **reddetsin**.

Denetim iki şeye bakıyor: görünümün satırları ve şu denemenin sonucu —
reddedilmesi bekleniyor:

```sql
UPDATE dbo.pending_orders SET status = 'shipped' WHERE id = 1004;
```

Kurduğun şeyi aynı kodda denemek istersen araya `GO` yaz: `CREATE`
kendi toplu işinde olmak zorunda, `GO`'suz altına yazılan bir sorgu
sözdizimi hatası veriyor. Her çalıştırma sonunda geri alındığı için bir
sonraki çalıştırmada aynı adla yeniden kurabilirsin.
