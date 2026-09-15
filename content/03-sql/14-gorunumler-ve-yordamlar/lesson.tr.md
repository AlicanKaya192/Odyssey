# Görünümler ve Saklı Yordamlar

Şimdiye kadar yazdığın her sorgu senin editöründe yaşadı: çalıştırdın,
sonucu gördün, sorgu orada kaldı. Aynı hesabı başka biri — ya da bir
uygulama — da istiyorsa sorgunun kendisini ona vermek gerekirdi.

Bu bölüm sorguyu **veritabanının içine** koyuyor. **Görünüm** bir
sorguya kalıcı bir ad veriyor; tablo gibi sorgulanıyor. **Saklı yordam**
parametre alan, birden fazla adım içerebilen, adıyla çağrılan bir kod
parçası. Aşağıdaki her şey Orta Seviyenin sekiz tablolu şemasında
ölçüldü.

## Görünüm: adı olan sorgu

```sql
CREATE VIEW dbo.customer_revenue AS
SELECT c.id, c.name,
       SUM(i.quantity * i.unit_price) AS revenue
FROM customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_items i ON i.order_id = o.id
WHERE o.status <> 'cancelled'
GROUP BY c.id, c.name;
```

Artık bir tablo gibi:

```sql
SELECT name FROM dbo.customer_revenue WHERE revenue > 10000 ORDER BY name;
```

Sonuç: Bright Office, Helix Studio. Görünümü kullanan kişinin üç tabloyu,
birleştirmeyi ve iptal kuralını bilmesi gerekmiyor.

<figure class="fig">
  <div class="versus">
    <div>
      <h4>WITH</h4>
      <p>Bir sorguya ad veriyor, ama ad <strong>yalnızca o cümle boyunca</strong> yaşıyor.</p>
      <p>Senin editöründe duruyor.</p>
    </div>
    <div>
      <h4>VIEW</h4>
      <p>Ad <strong>veritabanında kalıcı</strong>: silinene kadar herkes kullanabiliyor.</p>
      <p>Başka sorgular, başka kişiler, uygulamalar.</p>
    </div>
  </div>
</figure>

**Görünüm veri tutmuyor.** Yalnızca tanımı saklanıyor; her kullanıldığında
sorgu tablolardan yeniden çalışıyor. Ölçüldü: 1007 siparişinde bir
kalemin adedi 4'ten 3'e indirilince görünüm Orion Labs için `4510.00`
yerine hemen `3620.00` gösterdi.

## Kurallar

Ölçüldü:

| Yazım | Sonuç |
|---|---|
| aynı toplu işte `CREATE VIEW`'dan önce başka bir cümle | `'CREATE VIEW' must be the first statement in a query batch.` |
| `CREATE VIEW` ardından `GO`'suz bir `SELECT` | `Incorrect syntax near the keyword 'SELECT'.` |
| araya `GO` | çalışıyor |
| `SELECT customer_id, COUNT(*)` (adsız sütun) | `Create View or Function failed because no column name was specified for column 2.` |
| görünümde `ORDER BY` | `The ORDER BY clause is invalid in views ... unless TOP, OFFSET or FOR XML is also specified.` |
| aynı adla ikinci `CREATE VIEW` | `There is already an object named 'customer_revenue' in the database.` |
| `CREATE OR ALTER VIEW` | var olanı değiştiriyor |

`CREATE VIEW` kendi toplu işinde olmak zorunda. Bu uygulamada toplu işler
`GO` satırıyla ayrılıyor: görünümü kurup altında denemek istersen araya
`GO` yaz. Başındaki yorum satırları sorun değil (ölçüldü).

## SELECT * tuzağı

```sql
CREATE VIEW dbo.v_suppliers AS SELECT * FROM suppliers;
ALTER TABLE suppliers ADD phone NVARCHAR(20) NULL;
```

Sütun eklendikten sonra tablo beş sütun gösterdi, görünüm **hâlâ dört**
(ölçüldü). `*` görünüm kurulurken sütun listesine çevrilip öyle
saklanıyor. `EXEC sp_refreshview 'dbo.v_suppliers'` sonrasında beşinci
sütun geldi.

Kural: görünümde sütunları adıyla yaz. Hangi sütunların verildiği bir
karar; `*` o kararı sessizce tablonun o anki hâline bırakıyor.

## Görünüm üzerinden değiştirmek

Tek tablolu bir görünümün üstünden `UPDATE` yazılabiliyor ve değişiklik
tabloya gidiyor:

```sql
CREATE VIEW dbo.pending_orders AS
SELECT id, customer_id, order_date, status
FROM orders WHERE status = 'pending';

UPDATE dbo.pending_orders SET status = 'shipped' WHERE id = 1004;
```

`orders`'ta 1004 `shipped` oldu ve **görünümden kayboldu**: artık
görünümün `WHERE`'ine uymuyor. Aynı görünümden `status = 'shipped'` ile
bir satır eklemek de mümkün oldu — satır tabloya girdi, görünümde yoktu
(ölçüldü). Görünümün göstermediği bir şeyi görünüm üzerinden yazmak
kafa karıştırıcı.

İki sınır (ölçüldü):

| Yazım | Sonuç |
|---|---|
| toplamalı görünümden `UPDATE` (`customer_revenue`) | `Update or insert of view or function 'dbo.customer_revenue' failed because it contains a derived or constant field.` |
| görünümde olmayan `NOT NULL` bir sütunu olan tabloya görünümden `INSERT` | `Cannot insert the value NULL into column 'order_date' ...` |

## WITH CHECK OPTION

Görünümün sonuna eklenince, görünümün `WHERE`'ine uymayacak bir değişiklik
reddediliyor:

```sql
CREATE VIEW dbo.pending_checked AS
SELECT id, customer_id, order_date, status
FROM orders WHERE status = 'pending'
WITH CHECK OPTION;
```

`UPDATE ... SET status = 'shipped'` ve `status = 'shipped'` ile `INSERT`
ikisi de reddedildi: `The attempted insert or update failed because the
target view either specifies WITH CHECK OPTION ...` (hata 550).
`'pending'` ile eklenen satır kabul edildi.

## Bağımlılık: tablo değişince görünüm

Görünüm tablolarına yalnızca adıyla bağlı. Ölçüldü:

| Durum | Sonuç |
|---|---|
| görünümün tablosu silindi, görünüm kullanıldı | `Invalid object name 'dbo.t_tmp'.` ve `Could not use view or function 'dbo.v_tmp' because of binding errors.` |

`WITH SCHEMABINDING` görünümü tablosuna sıkı bağlıyor:

| `WITH SCHEMABINDING` ile | Sonuç |
|---|---|
| `SELECT *` | `Syntax '*' is not allowed in schema-bound objects.` |
| tek parçalı ad (`FROM t_sb`) | `... Names must be in two-part format ...` — `dbo.t_sb` gerekiyor |
| bağlı tabloyu silmek | `Cannot DROP TABLE 'dbo.t_sb' because it is being referenced by object 'v_sb'.` |
| görünümün kullandığı sütunun tipini değiştirmek | `The object 'v_sb' is dependent on column 'a'.` |
| tabloya yeni bir sütun eklemek | izin verildi |

## Saklı yordam

```sql
CREATE PROCEDURE dbo.customer_orders
    @customer_id INT
AS
SELECT id, order_date, status
FROM orders
WHERE customer_id = @customer_id
ORDER BY order_date;
```

Çağırmak:

```sql
EXEC dbo.customer_orders @customer_id = 1;   -- adiyla
EXEC dbo.customer_orders 4;                  -- sirasiyla
```

1 numaralı müşteri için üç satır (1001, 1003, 1006), 4 numaralı için iki
(1005, 1009). Görünümden farkları: parametre alıyor ve içinde `ORDER BY`
yazılabiliyor.

Ölçüldü:

| Çağrı | Sonuç |
|---|---|
| `EXEC dbo.customer_orders` (parametresiz) | `Procedure or function 'customer_orders' expects parameter '@customer_id', which was not supplied.` |
| `@customer_id = 'abc'` | `Error converting data type varchar to int.` |
| `@customer_id = '4'` | çalıştı — metin sayıya çevrildi |
| `@customer_id = 99` (olmayan müşteri) | boş sonuç, hata yok |
| fazladan bir parametre | `Procedure or function customer_orders has too many arguments specified.` |
| `SELECT * FROM dbo.customer_orders` | `Invalid object name 'dbo.customer_orders'.` — yordam `FROM`'a yazılamıyor |

## Varsayılan değer

```sql
CREATE PROCEDURE dbo.orders_by_status
    @status NVARCHAR(20) = N'pending'
AS
SELECT id, customer_id, status FROM orders
WHERE status = @status ORDER BY id;
```

`EXEC dbo.orders_by_status` parametresiz çalıştı ve üç bekleyen siparişi
getirdi; `@status = N'shipped'` altı satır. `EXEC dbo.orders_by_status
DEFAULT` de varsayılanı kullandı.

## Çıkış parametresi: OUTPUT

Bir yordam sonuç tablosu yerine (ya da yanında) değer döndürebiliyor:

```sql
CREATE PROCEDURE dbo.customer_order_count
    @customer_id INT,
    @order_count INT OUTPUT
AS
SELECT @order_count = COUNT(*) FROM orders WHERE customer_id = @customer_id;
```

```sql
DECLARE @n INT;
EXEC dbo.customer_order_count 1, @n OUTPUT;
SELECT @n;   -- 3
```

Ölçüldü: 1 numaralı müşteri **3**, siparişi olmayan 6 numaralı **0**.

`OUTPUT` iki yerde yazılıyor: tanımda **ve** çağrıda. Çağrıda unutulunca
`@n` **`NULL` kaldı ve hata gelmedi** (ölçüldü). Tersi, tanımda `OUTPUT`
olmayan bir parametreyi `OUTPUT` ile çağırmak hata veriyor: `The formal
parameter "@x" was not declared as an OUTPUT parameter ...`.

`RETURN` ise yalnızca bir tam sayı döndürüyor, genellikle durum kodu
olarak (`RETURN 0` başarı, `RETURN 1` "müşteri yok"; `EXEC @r =
dbo.p6 1` ile alındı). `RETURN 'abc'` yazılan bir yordam kuruldu ama
çalışınca `Conversion failed when converting the varchar value 'abc' to
data type int.` verdi.

## Hata vermek: THROW

Yordamın asıl gücü, kuralı tablonun yanına koymak:

```sql
CREATE PROCEDURE dbo.ship_order
    @order_id INT
AS
BEGIN
    SET NOCOUNT ON;
    IF NOT EXISTS (SELECT 1 FROM orders
                   WHERE id = @order_id AND status = 'pending')
        THROW 50001, N'Order is not pending.', 1;
    UPDATE orders SET status = 'shipped' WHERE id = @order_id;
END;
```

Ölçüldü: `EXEC dbo.ship_order 1004` siparişi `shipped` yaptı; `EXEC
dbo.ship_order 1001` (zaten gönderilmiş) `Order is not pending.` hatasıyla
durdu, `UPDATE`'e gelinmedi. `TRY ... CATCH` içinde çağrılınca
`ERROR_NUMBER()` 50001, `ERROR_MESSAGE()` `Order is not pending.`,
`ERROR_PROCEDURE()` `dbo.ship_order` verdi.

`THROW`'dan önceki cümle noktalı virgülle bitmezse yordam kurulmuyor:
`Incorrect syntax near 'THROW'.`

## Kurulurken denetlenmeyen şey

| Yordamın içinde | Sonuç |
|---|---|
| olmayan bir tablo | yordam **kuruldu**; `EXEC`'te `Invalid object name 'dbo.no_such_table'.` |
| var olan tabloda olmayan bir sütun | kurulurken hata: `Invalid column name 'no_such_column'.` |

Olmayan bir tabloyu adıyla anan yordam, tablo sonradan kurulabilir diye
kabul ediliyor. Yazım hatası bir tablo adındaysa bunu ancak çalıştırınca
görüyorsun.

## Veritabanında ne var

```sql
SELECT name, type_desc FROM sys.objects WHERE type IN ('V', 'P');
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.pending_orders'));
```

Birincisi görünümleri (`VIEW`) ve yordamları (`SQL_STORED_PROCEDURE`)
listeledi, ikincisi görünümün tanımını olduğu gibi verdi.
`sys.parameters` yordamın parametrelerini, tiplerini ve hangisinin
`OUTPUT` olduğunu gösterdi.

Bu uygulamada her çalıştırma sonunda geri alındığı için kurduğun görünüm
ve yordam bir sonraki çalıştırmada durmuyor (ölçüldü: geri almadan sonra
`OBJECT_ID` `NULL`).

## Özet

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">CREATE VIEW</span><span class="anat-body">Sorguya kalıcı bir ad; veri tutmuyor. Sütunları adıyla yaz, <code>ORDER BY</code> yok.</span></div>
    <div class="anat-row"><span class="anat-label">WITH CHECK OPTION</span><span class="anat-body">Görünüm üzerinden yazılan şey görünümün <code>WHERE</code>'ine uymak zorunda.</span></div>
    <div class="anat-row"><span class="anat-label">SCHEMABINDING</span><span class="anat-body">Tabloyu görünüm varken silinemez, değiştirilemez yapıyor.</span></div>
    <div class="anat-row"><span class="anat-label">CREATE PROCEDURE</span><span class="anat-body">Parametre alan, adıyla çağrılan kod; <code>EXEC</code> ile.</span></div>
    <div class="anat-row"><span class="anat-label">OUTPUT</span><span class="anat-body">Tanımda ve çağrıda; çağrıda unutulursa sessizce <code>NULL</code>.</span></div>
    <div class="anat-row"><span class="anat-label">THROW</span><span class="anat-body">Kuralı tablonun yanına koyar; öncesi <code>;</code> ile biter.</span></div>
    <div class="anat-row"><span class="anat-label">GO</span><span class="anat-body"><code>CREATE VIEW</code> / <code>PROCEDURE</code> kendi toplu işinde.</span></div>
  </div>
</figure>

Sıradaki bölüm SQL patikasının son bölümü: genel tekrar.
