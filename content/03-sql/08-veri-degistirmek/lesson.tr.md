# Veri Değiştirmek

Yedi bölümdür veriyi hep **okudun**. `SELECT` ne yazarsan yaz, tabloda
hiçbir şey değişmiyordu: yanlış sorgu yanlış cevap veriyor, o kadar.

Bu bölümde yazmaya başlıyorsun. Üç komut var — `INSERT`, `UPDATE`,
`DELETE` — ve üçünün de ortak bir özelliği var: **geri alma düğmesi yok.**

## Önce şunu bil: burada güvendesin

Odyssey'de yazdığın her şey, çalıştırma bittiğinde geri alınıyor. Bütün
tabloları silsen bile bir sonraki denemede yerlerinde duruyorlar.

Gerçek bir veritabanında böyle bir ağ yok. Bu bölümdeki alışkanlıklar
tam da bu yüzden var.

## INSERT: satır eklemek

```sql
INSERT INTO categories (code, name)
VALUES ('NET', 'Networking');
```

Üç parça: **hangi tabloya**, **hangi sütunlara**, **hangi değerler**.

Sütun listesini yazmadan da olur:

```sql
INSERT INTO categories VALUES ('NET', 'Networking');
```

Bu çalışıyor ama **yazma**. Değerler tablodaki sütun sırasına göre
dağıtılıyor; yarın tabloya bir sütun eklenirse bu satır sessizce yanlış
yere yazmaya başlıyor. Sütun listesi yazan `INSERT` ise çalışmayı
sürdürüyor.

### Tek seferde çok satır

```sql
INSERT INTO categories (code, name) VALUES
    ('NET', 'Networking'),
    ('PRN', 'Printing');
```

İki satır ekleniyor ve sunucu "2 satır etkilendi" diyor. Ayrı ayrı iki
`INSERT` yazmakla aynı sonuç, ama tek komut daha hızlı ve **ya ikisi de
girer ya hiçbiri**.

### Değerler bir sorgudan da gelebiliyor

```sql
INSERT INTO categories (code, name)
SELECT ... FROM ...;
```

`VALUES` yerine bir `SELECT` yazıyorsun. Sütun sayısı ve sırası tutmak
zorunda. Bu, bir tablodan diğerine veri taşımanın en kısa yolu.

### Ne zaman hata veriyor

Üç yaygın durum var; üçü de ölçüldü:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Eksik sütun</span><span class="anat-body"><code>Cannot insert the value NULL into column 'name' ... column does not allow nulls.</code> Sütun <code>NOT NULL</code> ve sen değer vermedin.</span></div>
    <div class="anat-row"><span class="anat-label">Sayı uyuşmuyor</span><span class="anat-body"><code>There are more columns in the INSERT statement than values specified in the VALUES clause.</code></span></div>
    <div class="anat-row"><span class="anat-label">Anahtar tekrarı</span><span class="anat-body"><code>Violation of PRIMARY KEY constraint ... The duplicate key value is (ACC).</code> O anahtar zaten var.</span></div>
  </div>
</figure>

Bu hatalar **iyi haber**: sunucu seni yanlış veriden koruyor. Asıl
tehlikeli olan hata vermeyen komutlar — birazdan geliyorlar.

## UPDATE: var olanı değiştirmek

```sql
UPDATE products
SET price = price * 1.10
WHERE category_code = 'ACC';
```

`SET` neyin değişeceğini, `WHERE` hangi satırlarda değişeceğini söylüyor.
Bu sorgu **altı satırı** güncelliyor.

Sağ tarafta sütunun kendisini kullanabiliyorsun: `price = price * 1.10`
"fiyatı %10 arttır" demek. Sunucu her satır için o satırın kendi eski
değerini okuyor.

Birden fazla sütun virgülle:

```sql
UPDATE products
SET price = 500.00, stock = 40
WHERE id = 1;
```

### WHERE'i unutursan

```sql
UPDATE products SET price = price * 1.10;
```

Bu sorgu **on iki satırın on ikisini** birden değiştiriyor (ölçüldü).
Hata yok, uyarı yok, "emin misin" yok. Sunucu tam olarak dediğini yapıyor
— çünkü `WHERE` yazmayan bir `UPDATE`'in anlamı gerçekten "hepsi".

Katalogdaki bütün fiyatlar %10 arttı ve hangilerinin doğru olduğunu artık
bilmiyorsun.

**`WHERE`'siz `UPDATE`, `WHERE`'siz `DELETE` ve `DROP TABLE`** — bu üçü
veritabanı işinin klasik felaketleri.

## DELETE: satır silmek

```sql
DELETE FROM orders
WHERE status = 'cancelled';
```

`SELECT` yok, sütun yok: satırın tamamı gidiyor. Bu sorgu bir satır
siliyor, geriye dokuz sipariş kalıyor.

Ve evet, aynı tuzak burada da var:

```sql
DELETE FROM shipments;
```

Altı satırın altısı gitti.

### DELETE, TRUNCATE, DROP

Üçü karışıyor, oysa farkları net:

<figure class="fig">
  <div class="versus">
    <div>
      <h4>DELETE</h4>
      Satırları siler. <code>WHERE</code> alabilir. İşlemin parçası, geri alınabilir. Kaç satır sildiğini söyler.
    </div>
    <div>
      <h4>TRUNCATE</h4>
      Tablonun <b>tamamını</b> boşaltır. <code>WHERE</code> almaz. Çok daha hızlı, ama kaç satır gittiğini söylemez.
    </div>
    <div class="no">
      <h4>DROP</h4>
      Tabloyu <b>yok eder</b>. Satırlar değil, tablonun kendisi gider.
    </div>
  </div>
</figure>

`TRUNCATE` tek tek satır silmiyor, tabloyu sıfırlıyor — o yüzden hızlı.
Bir milyon satırlık tabloyu boşaltmak gerekiyorsa doğru araç o.

## Kaç satır etkilendi

Her üç komut da çalıştıktan sonra kaç satıra dokunduğunu söylüyor.
Odyssey bunu sonuç panelinde gösteriyor; kendi sorgunda da okuyabilirsin:

```sql
UPDATE products SET stock = stock + 1 WHERE category_code = 'ACC';
SELECT @@ROWCOUNT AS affected;
```

Sonuç: **6**.

Bu sayı en iyi denetim aracın. "Bir müşteriyi güncelliyorum" deyip 40
görüyorsan `WHERE`'de bir sorun var — ve bunu **veriyi bozmadan önce**
görüyorsun.

## Yazmadan önce: SELECT ile prova

Bu bölümün en önemli alışkanlığı, tek satırlık:

```sql
-- once bunu calistir
SELECT * FROM products WHERE category_code = 'ACC';

-- dogru satirlari getirdigini gorunce
UPDATE products SET price = price * 1.10 WHERE category_code = 'ACC';
```

Aynı `WHERE`'i önce bir `SELECT` ile çalıştırıyorsun. Ekranda hangi
satırların değişeceğini görüyorsun. Doğruysa `SELECT`'i `UPDATE`'e
çeviriyorsun.

İki saniye sürüyor ve bu bölümdeki hataların neredeyse hepsini
engelliyor.

## İşlemler: geri alınabilir değişiklik

Bir de asıl ağ var. Değişikliği **deneme** hâlinde yapıp sonra karar
verebiliyorsun:

```sql
BEGIN TRANSACTION;

DELETE FROM shipments;

-- bak bakalim ne olmus
SELECT COUNT(*) FROM shipments;

ROLLBACK;   -- vazgectim
-- COMMIT;  -- ya da: kalsin
```

<figure class="fig">
  <div class="flow">
    <span class="node">BEGIN TRANSACTION</span>
    <span class="arrow">→</span>
    <span class="node">değişiklikler</span>
    <span class="arrow">→</span>
    <span class="node ok">COMMIT</span>
    <span class="arrow">/</span>
    <span class="node no">ROLLBACK</span>
  </div>
</figure>

`BEGIN TRANSACTION` ile `COMMIT` arasındaki her şey tek bir paket. `COMMIT`
diyene kadar hiçbiri kalıcı değil; `ROLLBACK` dersen hepsi birden geri
alınıyor.

Odyssey'in "her çalıştırmadan sonra sıfırlanıyor" sözü tam olarak bu:
senin SQL'in bir işlemin içinde çalışıyor ve sonunda `ROLLBACK` çağrılıyor.

**İşlem tek bir komuttan ibaret değil.** Asıl gücü birden fazla değişikliği
birbirine bağlamak: para bir hesaptan çıkıp diğerine giriyorsa ikisi birden
olmalı ya da hiçbiri olmamalı. İşlem bunu garanti ediyor.

## Özet

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Satır ekle</span><span class="anat-body"><code>INSERT INTO t (sütunlar) VALUES (...)</code> — sütun listesini yaz</span></div>
    <div class="anat-row"><span class="anat-label">Satır değiştir</span><span class="anat-body"><code>UPDATE t SET ... WHERE ...</code> — <code>WHERE</code>'i unutma</span></div>
    <div class="anat-row"><span class="anat-label">Satır sil</span><span class="anat-body"><code>DELETE FROM t WHERE ...</code> — <code>WHERE</code>'i unutma</span></div>
    <div class="anat-row"><span class="anat-label">Tabloyu boşalt</span><span class="anat-body"><code>TRUNCATE TABLE t</code></span></div>
    <div class="anat-row"><span class="anat-label">Önce dene</span><span class="anat-body">Aynı <code>WHERE</code> ile bir <code>SELECT</code></span></div>
    <div class="anat-row"><span class="anat-label">Geri alınabilir yap</span><span class="anat-body"><code>BEGIN TRANSACTION</code> ... <code>ROLLBACK</code></span></div>
  </div>
</figure>

Bir sonraki bölümde tabloların kendisini kuracaksın — ve orada, yanlış
veriyi en baştan engelleyen kısıtları göreceksin.
