Görünüm ve yordam hatalarının çoğu mesaj veriyor ve mesaj ne yapılacağını
söylüyor. Bu not **mesaj vermeyenleri** topluyor: hepsi bu bölümde
ölçüldü ve hepsinde sorgu çalıştı, sonuç yanlış ya da eksikti.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">SELECT * görünüm</span><span class="anat-body">Tabloya eklenen sütun görünümde çıkmıyor.</span></div>
    <div class="anat-row"><span class="anat-label">Kaybolan satır</span><span class="anat-body">Görünüm üzerinden değişen satır görünümden düşüyor.</span></div>
    <div class="anat-row"><span class="anat-label">Görünmeyen ekleme</span><span class="anat-body">Görünüm üzerinden eklenen satır tabloda var, görünümde yok.</span></div>
    <div class="anat-row"><span class="anat-label">Unutulan OUTPUT</span><span class="anat-body">Değişken <code>NULL</code> kalıyor.</span></div>
    <div class="anat-row"><span class="anat-label">Olmayan müşteri</span><span class="anat-body">Yordam boş sonuç döndürüyor.</span></div>
    <div class="anat-row"><span class="anat-label">Olmayan tablo</span><span class="anat-body">Yordam kuruluyor, hata ancak çalışınca.</span></div>
  </div>
</figure>

## 1. SELECT * görünüm eskiyor

`CREATE VIEW dbo.v_suppliers AS SELECT * FROM suppliers` sonrasında
tabloya `phone` sütunu eklendi. Tablo beş sütun, görünüm dört gösterdi.
`sp_refreshview` sonrasında beş.

**Çare:** görünümde sütunları adıyla yaz. Yeni sütun gerekiyorsa görünümü
bilerek değiştir (`CREATE OR ALTER VIEW`). Sıkı bağ istiyorsan
`WITH SCHEMABINDING` — o zaman `*` zaten yazılamıyor.

## 2. Görünüm üzerinden değişen satır kayboluyor

`pending_orders` üzerinden 1004'ün durumu `shipped` yapıldı. Hata yok;
satır tabloda güncellendi ve görünümden düştü.

## 3. Görünüm üzerinden eklenen satır görünmüyor

Aynı görünümden `status = 'shipped'` ile bir satır eklendi. Tabloda 1,
görünümde 0.

**Çare (2 ve 3):** `WITH CHECK OPTION`. İkisi de hata 550 ile reddedildi;
`'pending'` ile ekleme kabul edildi.

## 4. Çağrıda unutulan OUTPUT

```sql
DECLARE @n INT;
EXEC dbo.customer_order_count 1, @n;      -- OUTPUT yok
SELECT @n;                                -- NULL
```

Yordam çalıştı, sayıyı hesapladı, ama `@n`'ye yazmadı. Hata yok.

**Çare:** `OUTPUT` iki yerde: tanımda ve çağrıda. Çağrıdan sonra değeri
bir kez kontrol etmek (`NULL` mı?) bu hatayı hemen gösteriyor.

## 5. Olmayan kayıt boş sonuç

`EXEC dbo.customer_orders @customer_id = 99` hata vermedi, boş döndü.
Siparişi olmayan bir müşteri de (6) aynı boş sonucu veriyor. İkisini
çağıran ayırt edemiyor.

**Çare:** fark önemliyse yordam söylesin: `RETURN 1` ile bir durum kodu
(ölçüldü: 99 için 1, 1 için 0) ya da `THROW` ile bir hata.

## 6. Olmayan tabloyu anan yordam kuruluyor

`CREATE PROCEDURE dbo.p8 AS SELECT * FROM dbo.no_such_table` hata
vermeden kuruldu; `EXEC`'te `Invalid object name`. Olmayan bir **sütun**
ise kurulurken yakalandı.

**Çare:** yordamı kurduktan sonra bir kez çalıştır. Kurulmuş olması
doğru olduğu anlamına gelmiyor.

## Bir de mesajı yanıltıcı olan: GO

`CREATE VIEW` ardından `GO`'suz yazılan bir `SELECT`
`Incorrect syntax near the keyword 'SELECT'.` verdi. Mesaj `SELECT`'te
bir yazım hatası varmış gibi okunuyor; asıl sebep `CREATE VIEW`'ın kendi
toplu işinde olmaması. Araya `GO` yazınca çalıştı.

## Kontrol soruları

- **Görünümde `*` var mı?** Varsa sütun listesi kurulduğu günde donmuş.
- **Görünüm üzerinden yazılıyor mu?** Yazılıyorsa `WITH CHECK OPTION`.
- **Yordamın çıkış parametresi çağrıda da `OUTPUT` mu?**
- **"Bulunamadı" ile "boş" ayrı şeyler mi?** Öyleyse yordam bunu
  söylemeli.
