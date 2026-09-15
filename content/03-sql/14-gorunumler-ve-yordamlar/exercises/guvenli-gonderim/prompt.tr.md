Bir siparişi `'shipped'` yapan bir yordam kur: `dbo.ship_order`. Tek
parametresi `@order_id` (`INT`).

Kural: sipariş `'pending'` değilse — ya da hiç yoksa — hiçbir şeyi
güncellemeden şu hatayı versin:

```sql
THROW 50001, N'Order is not pending.', 1;
```

Denetim iki şey deniyor:

| Çağrı | Beklenen |
|---|---|
| `EXEC dbo.ship_order 1001;` (zaten gönderilmiş) | hata numarası `50001` |
| `EXEC dbo.ship_order 1004;` (bekliyor) | 1004'ün durumu `shipped` |

Kuralı uygulamayı çağıranlara bırakmak yerine yordamın içine koymak,
tablonun hiçbir yoldan yanlış duruma düşmemesi demek.

Kurduğun şeyi aynı kodda denemek istersen araya `GO` yaz: `CREATE`
kendi toplu işinde olmak zorunda, `GO`'suz altına yazılan bir sorgu
sözdizimi hatası veriyor. Her çalıştırma sonunda geri alındığı için bir
sonraki çalıştırmada aynı adla yeniden kurabilirsin.
