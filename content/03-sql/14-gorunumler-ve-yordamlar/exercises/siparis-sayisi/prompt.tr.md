Bir müşterinin sipariş sayısını bir **çıkış parametresiyle** döndüren bir
yordam kur: `dbo.customer_order_count`. Parametreler, bu sırayla:

| Parametre | Tip | Görevi |
|---|---|---|
| `@customer_id` | `INT` | hangi müşteri |
| `@order_count` | `INT` | **çıkış**: sayı buraya yazılıyor |
| `@status` | `NVARCHAR(20)` | isteğe bağlı; verilmezse bütün durumlar |

Yordam bir sonuç tablosu döndürmesin; sayı yalnızca `@order_count` ile
dönsün. Denetim şöyle çağırıyor:

```sql
DECLARE @all INT, @shipped INT, @none INT;
EXEC dbo.customer_order_count 1, @all OUTPUT;
EXEC dbo.customer_order_count @customer_id = 1, @order_count = @shipped OUTPUT,
                              @status = N'shipped';
EXEC dbo.customer_order_count 6, @none OUTPUT;
SELECT @all, @shipped, @none;   -- beklenen: 3, 2, 0
```

Çağıran taraf da `OUTPUT` yazmak zorunda. Yazmazsa değişken `NULL` kalıyor
ve **hata da gelmiyor** (ölçüldü).

Kurduğun şeyi aynı kodda denemek istersen araya `GO` yaz: `CREATE`
kendi toplu işinde olmak zorunda, `GO`'suz altına yazılan bir sorgu
sözdizimi hatası veriyor. Her çalıştırma sonunda geri alındığı için bir
sonraki çalıştırmada aynı adla yeniden kurabilirsin.
