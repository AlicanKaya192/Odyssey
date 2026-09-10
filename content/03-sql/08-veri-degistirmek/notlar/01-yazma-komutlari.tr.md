Üç komutun tek sayfalık özeti. Hata metinleri bu bölümün şemasında
gerçek sunucudan alındı.

## Yazımlar

```sql
-- ekle
INSERT INTO tablo (sutun1, sutun2) VALUES (deger1, deger2);

-- cok satir
INSERT INTO tablo (sutun1, sutun2) VALUES
    (a1, a2),
    (b1, b2);

-- baska bir sorgudan
INSERT INTO tablo (sutun1, sutun2)
SELECT x, y FROM baska_tablo WHERE ...;

-- degistir
UPDATE tablo SET sutun = deger WHERE kosul;

-- sil
DELETE FROM tablo WHERE kosul;

-- tabloyu bosalt
TRUNCATE TABLE tablo;
```

## Hangi komut hangi soruya

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Yeni satır</span><span class="anat-body"><code>INSERT</code></span></div>
    <div class="anat-row"><span class="anat-label">Var olan satır</span><span class="anat-body"><code>UPDATE</code></span></div>
    <div class="anat-row"><span class="anat-label">Bazı satırlar gitsin</span><span class="anat-body"><code>DELETE</code> + <code>WHERE</code></span></div>
    <div class="anat-row"><span class="anat-label">Hepsi gitsin, tablo kalsın</span><span class="anat-body"><code>TRUNCATE TABLE</code></span></div>
    <div class="anat-row"><span class="anat-label">Tablo da gitsin</span><span class="anat-body"><code>DROP TABLE</code></span></div>
  </div>
</figure>

## Hata mesajları ve anlamları

| Mesaj | Ne olmuş |
|---|---|
| `Cannot insert the value NULL into column 'name' ... column does not allow nulls` | `NOT NULL` bir sütuna değer vermedin |
| `There are more columns in the INSERT statement than values specified` | Sütun sayısı ile değer sayısı tutmuyor |
| `Violation of PRIMARY KEY constraint ... The duplicate key value is (ACC)` | O anahtar tabloda zaten var |
| `Conversion failed when converting the varchar value 'abc' to data type int` | Sayı beklenen yere metin yazdın |
| `Invalid object name 'x'` | Tablo adı yanlış ya da tablo yok |

Bu mesajların hepsi **iyi haber**: sunucu yanlış veriyi içeri almadı.
Tehlikeli olan, hata vermeyen komutlar.

## Kaç satır etkilendi

```sql
UPDATE products SET stock = stock + 1 WHERE category_code = 'ACC';
SELECT @@ROWCOUNT AS affected;   -- 6
```

`@@ROWCOUNT` **son** komutun sayısını tutuyor ve araya giren her komut
onu eziyor. Ölçüldü: `UPDATE` ile `SELECT @@ROWCOUNT` arasına tek satır
döndüren bir sorgu koyunca sonuç `6` değil **`1`** çıkıyor — o satırı
sayan, araya giren sorgu. O yüzden hemen sonrasında okunuyor.

Sayının anlamı:

- **Beklediğinden büyük** → `WHERE` fazla satır tutuyor.
- **Sıfır** → `WHERE` hiçbir şey tutmamış. Hata değil ama muhtemelen
  istediğin de değil.
- **Beklediğin kadar** → doğru yoldasın.

## UPDATE ve DELETE'in gelişmiş biçimleri

Koşul başka bir tabloya bakıyorsa iki yol var:

```sql
-- alt sorguyla
DELETE FROM order_items
WHERE order_id IN (SELECT id FROM orders WHERE status = 'cancelled');

-- birlestirmeyle (T-SQL'e ozgu)
DELETE oi FROM order_items oi
JOIN orders o ON o.id = oi.order_id
WHERE o.status = 'cancelled';
```

İkisi de aynı sonucu veriyor. Alt sorgulu yazım her veritabanında
çalışıyor; `DELETE ... FROM ... JOIN` yazımı T-SQL'e özgü.

`UPDATE` için de aynısı geçerli:

```sql
UPDATE p SET p.stock = 0
FROM products p
JOIN categories c ON c.code = p.category_code
WHERE c.name = 'Software';
```

Dikkat: `UPDATE`'ten sonra yazdığın ad `FROM` içinde **geçen** bir ad
olmalı. Takma ad verdiysen ya takma adı ya tablo adını yazabiliyorsun,
ama `FROM`'da hiç geçmeyen bir ad yazarsan hata alıyorsun:
`Invalid object name 'p'` (ölçüldü).

## İşlem komutları

```sql
BEGIN TRANSACTION;   -- baslat
COMMIT;              -- kalici yap
ROLLBACK;            -- hepsini geri al
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">İşlem içindeyken</span><span class="anat-body">Değişiklikleri yalnızca sen görüyorsun. Başkasının sorgusu hâlâ eski hâli okuyor.</span></div>
    <div class="anat-row"><span class="anat-label">COMMIT sonrası</span><span class="anat-body">Herkes görüyor. Geri dönüş yok.</span></div>
    <div class="anat-row"><span class="anat-label">ROLLBACK sonrası</span><span class="anat-body">Hiçbir şey olmamış gibi.</span></div>
  </div>
</figure>

**Odyssey'de `COMMIT` yazmanın bir etkisi yok.** Alıştırma zaten bir
işlemin içinde çalışıyor ve sonunda veritabanı her hâlükârda tohumdan
geri kuruluyor. Gerçek bir sunucuda `COMMIT` geri dönüşü olmayan komut.

## Sık yapılan üç hata

1. **`WHERE`'i unutmak.** `UPDATE` ve `DELETE` için `WHERE`'siz yazım
   "hepsi" demek ve sunucu bunu sorgulamıyor.
2. **`INSERT`'te sütun listesi yazmamak.** Bugün çalışıyor, tabloya sütun
   eklendiği gün sessizce bozuluyor.
3. **`DELETE` yerine `DROP` yazmak.** `DELETE` satırları, `DROP` tabloyu
   siliyor.
