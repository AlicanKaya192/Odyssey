# Genel Tekrar

On beş bölüm önce SQL Server'ı kurup ilk `SELECT`'i yazdın. Şimdi bir
sipariş veritabanından her türlü soruyu cevaplayabiliyor, tablo kurup
kural koyabiliyor, bir sorgunun neden yavaş olduğunu ölçebiliyor ve kodu
veritabanının içine koyabiliyorsun.

Bu bölüm yeni bir şey öğretmiyor. Bir sorgunun **hangi sırayla**
çalıştığını ve patikanın en sık tuzaklarını ölçülmüş sayılarla tek yerde
topluyor. Her şey Orta Seviyenin sekiz tablolu şemasında ölçüldü.

## Bir sorgu hangi sırayla çalışıyor

Yazdığın sıra `SELECT ... FROM ... WHERE ...`. Sunucunun çalıştırdığı
sıra başka:

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>1</b><br>FROM<br>JOIN</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>2</b><br>WHERE</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>3</b><br>GROUP BY</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>4</b><br>HAVING</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>5</b><br>SELECT<br>pencereler</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>6</b><br>ORDER BY</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>7</b><br>TOP</span>
  </div>
  <figcaption>Bir adım, kendisinden sonra gelen bir adımın ürettiği şeyi göremiyor.</figcaption>
</figure>

Patikada karşılaştığın hataların çoğu bu sıradan çıkıyor (ölçüldü):

| Yazım | Sonuç | Neden |
|---|---|---|
| `SELECT name AS n ... WHERE n = 'Mouse'` | `Invalid column name 'n'.` | `WHERE` (2), `SELECT`'ten (5) önce |
| `SELECT price * 2 AS double_price ... WHERE double_price > 1000` | `Invalid column name 'double_price'.` | aynı |
| `SELECT category_code AS cc ... GROUP BY cc` | `Invalid column name 'cc'.` | `GROUP BY` (3), `SELECT`'ten önce |
| `WHERE COUNT(*) > 1` | `An aggregate may not appear in the WHERE clause ...` | toplama gruplamadan sonra; koşul `HAVING`'e |
| `WHERE ROW_NUMBER() OVER (...) <= 3` | `Windowed functions can only appear in the SELECT or ORDER BY clauses.` | pencere `SELECT`'te hesaplanıyor |
| `SELECT category_code, name, COUNT(*) ... GROUP BY category_code` | `Column 'products.name' is invalid in the select list ...` | gruplamadan sonra satır başına bir `name` yok |
| `SELECT price AS p ... ORDER BY p` | çalıştı | `ORDER BY` (6), `SELECT`'ten sonra |
| `ORDER BY 2` | çalıştı | ikinci sütuna göre |

Sonraki bir adımın ürettiği şeyi önceki bir adımda kullanmak gerekiyorsa
sorgu bir kat içeri alınıyor: `FROM (...)` ya da `WITH`.

## NULL: bilinmeyen

`orders` tablosunda iki siparişin çalışanı yok (`employee_id` `NULL`).
Ölçüldü:

| Sorgu | Sonuç |
|---|---|
| `WHERE employee_id = NULL` | 0 satır |
| `WHERE employee_id IS NULL` | 2 |
| `WHERE employee_id <> 3` | 4 — `NULL` olan iki sipariş ne "3" ne "3 değil" |
| `COUNT(*)` / `COUNT(employee_id)` | 10 / 8 |
| boş bir kümede `COUNT(*)` / `SUM(...)` | 0 / `NULL` |
| `id NOT IN (SELECT employee_id FROM orders)` | **0 çalışan** |
| aynı soru `NOT EXISTS` ile | 4 çalışan |

`NOT IN`'deki sonuç patikanın en sinsi tuzağı. `x NOT IN (3, 4, NULL)`
aslında "`x <> 3` ve `x <> 4` ve `x <> NULL`" demek; sonuncusu hiçbir
zaman doğru olmadığı için bütün koşul hiçbir satırda doğru olmuyor. Çare
`NOT EXISTS` ya da alt sorguda `WHERE employee_id IS NOT NULL` — ikisi de
4 verdi.

## LEFT JOIN'i sessizce içe çevirmek

"Her müşteri ve gönderilmiş siparişleri":

| Koşulun yeri | Satır | Müşteri |
|---|---|---|
| `LEFT JOIN orders o ON o.customer_id = c.id` + `WHERE o.status = 'shipped'` | 6 | 4 |
| `LEFT JOIN orders o ON o.customer_id = c.id AND o.status = 'shipped'` | 8 | 6 |

`WHERE` birleştirmeden sonra çalışıyor: eşleşmeyen müşterilerin `NULL`'lu
satırları `o.status = 'shipped'` koşulunu geçemiyor ve düşüyor. `LEFT JOIN`
yazmışken sonuç iç birleştirmeninki oluyor. Sağdaki tabloya ait koşul
`ON`'a yazılıyor.

## Satırlar çoğalınca

`orders` ile `order_items` birleşince **20 satır** çıktı, sipariş 10.
`COUNT(o.customer_id)` 20 verdi, `COUNT(DISTINCT o.customer_id)` 5.
Birleştirmeden sonra her satır artık bir **kalem**; siparişe ait bir şeyi
saymak ya da toplamak onu kalem sayısı kadar tekrarlıyor.

Aynı soru `UNION` ile: müşteri ve tedarikçi şehirleri `UNION` ile 5,
`UNION ALL` ile 10.

## Sayılar

| İfade | Sonuç |
|---|---|
| `7 / 2` | `3` — iki tam sayı, tam sayı sonuç |
| `7 / 2.0` | `3.500000` |
| `7 % 2` | `1` |
| `10 / 0` | `Divide by zero error encountered.` |
| `10 / NULLIF(0, 0)` | `NULL` |
| `CAST('abc' AS INT)` | `Conversion failed when converting the varchar value 'abc' to data type int.` |
| `TRY_CAST('abc' AS INT)` | `NULL` |
| `LEN('abc  ')` / `DATALENGTH('abc  ')` | `3` / `5` — `LEN` sondaki boşlukları saymıyor |

## Değiştirmek ve kurmak

| Durum | Ölçülen |
|---|---|
| `WHERE`'siz `UPDATE products SET stock = stock` | 12 satır etkilendi — hepsi |
| bu şemada yabancı anahtar | yok (0) |
| 1 numaralı müşteriyi silmek (geri alınan işlemde) | silindi; 3 siparişi öksüz kaldı |
| `INSERT INTO categories VALUES ('XYZ')` | `Column name or number of supplied values does not match table definition.` |
| `WHERE id = (SELECT ... )` alt sorgu 3 satır dönünce | `Subquery returned more than 1 value ...` |

Yabancı anahtar olmayan bir şemada silme ve güncelleme hiçbir şeyi
korumuyor. Dokuzuncu bölümdeki kurallar tam bunun için.

## İleri Seviyenin en sık tuzakları

| Tuzak | Ölçülen | Çare |
|---|---|---|
| eşitlikte `ROW_NUMBER` | aynı pencere iki sorguda farklı 1 numara | ayırt edici bir sütun |
| varsayılan çerçeve | 1001'in üç kalemi de 1815 | `ROWS UNBOUNDED PRECEDING` |
| özyinelemede metin | `Types don't match between the anchor and the recursive part` | iki parçada `CAST` |
| dizinli sütuna işlev | 2 okuma yerine 42 | sütunu çıplak bırak |
| `SELECT *` görünüm | yeni sütun görünmedi | sütunları adıyla yaz |
| çağrıda unutulan `OUTPUT` | `NULL`, hata yok | tanımda ve çağrıda `OUTPUT` |

## Hangi soruya hangi araç

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">"Şu koşula uyan satırlar"</span><span class="anat-body"><code>WHERE</code> — <code>NULL</code> için <code>IS NULL</code></span></div>
    <div class="anat-row"><span class="anat-label">"Grup başına bir sayı"</span><span class="anat-body"><code>GROUP BY</code>; grubun koşulu <code>HAVING</code></span></div>
    <div class="anat-row"><span class="anat-label">"Satır kalsın, yanına grubun bilgisi"</span><span class="anat-body"><code>OVER (PARTITION BY ...)</code></span></div>
    <div class="anat-row"><span class="anat-label">"Başka tablodaki bilgi"</span><span class="anat-body"><code>JOIN</code>; eşleşmeyen de kalsın: <code>LEFT JOIN</code>, koşul <code>ON</code>'da</span></div>
    <div class="anat-row"><span class="anat-label">"Önce şunu hesapla, sonra onu kullan"</span><span class="anat-body"><code>WITH</code></span></div>
    <div class="anat-row"><span class="anat-label">"Derinliği bilinmeyen ağaç, hiçbir tabloda olmayan dizi"</span><span class="anat-body">özyinelemeli <code>WITH</code></span></div>
    <div class="anat-row"><span class="anat-label">"Her gün aynı sorgu"</span><span class="anat-body"><code>VIEW</code>; parametreli ve kurallı iş: <code>PROCEDURE</code></span></div>
    <div class="anat-row"><span class="anat-label">"Yavaş"</span><span class="anat-body">okumayı ölç; sütunu çıplak bırak; dizin</span></div>
    <div class="anat-row"><span class="anat-label">"Bu asla olmamalı"</span><span class="anat-body"><code>NOT NULL</code>, <code>CHECK</code>, <code>FOREIGN KEY</code>, <code>UNIQUE</code></span></div>
  </div>
</figure>

## Alıştırmalar

Beş alıştırmanın her biri birkaç bölümü birleştiriyor: ay içinde kategori
payı (birleştirme, gruplama, tarih, `WITH`, pencere), tekrar gelen
müşteriler (`HAVING`, tarih), bir ekibin cirosu (özyineleme, `LEFT JOIN`),
bir sipariş özeti görünümü (`LEFT JOIN`, `COALESCE`, görünüm) ve bir iade
tablosu (tablo tasarımı, kurallar, veri eklemek).

SQL patikası burada bitiyor. Notlarda patikanın tamamı tek sayfada ve
buradan sonra neye bakabileceğin var.
