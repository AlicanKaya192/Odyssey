# Tabloları Birleştirmek

Başlangıç seviyesinde tek bir tabloyla çalıştın. Gerçek bir veritabanında
böyle olmuyor: veri **parçalara** ayrılıp birbirine bağlanıyor.

Bu bölümden itibaren sekiz tablolu bir sipariş veritabanıyla
çalışacaksın. İlk iş, o tabloları birleştirmeyi öğrenmek.

## Neden tek tabloda durmuyor?

Ürün tablosunda tedarikçinin adını, şehrini ve ülkesini de tutabilirdik.
Üç sorun çıkıyor:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Tekrar</span><span class="anat-body">Aynı tedarikçi üç üründe geçiyorsa adı üç kez yazılıyor.</span></div>
    <div class="anat-row"><span class="anat-label">Tutarsızlık</span><span class="anat-body">Tedarikçi taşınınca üç satırın üçünü de güncellemek gerekiyor; biri unutulursa veri kendi içinde çelişiyor.</span></div>
    <div class="anat-row"><span class="anat-label">Kayıp</span><span class="anat-body">Henüz ürünü olmayan bir tedarikçiyi hiçbir yere yazamıyorsun.</span></div>
  </div>
</figure>

Çözüm, her şeyi kendi tablosuna koyup aralarına **bağ** kurmak:

```
suppliers.code  <---  products.supplier_code
```

`products.supplier_code` sütununa **yabancı anahtar** deniyor: başka bir
tablodaki satırı işaret ediyor.

Bu ayrımın bedeli şu: bir soruyu cevaplamak için artık iki tabloya birden
bakman gerekiyor. `JOIN` bunu yapıyor.

## INNER JOIN

```sql
SELECT p.name, s.name
FROM products p
JOIN suppliers s ON p.supplier_code = s.code;
```

Üç parça var:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">FROM products p</span><span class="anat-body">Soldaki tablo ve ona verilen kısa ad (<b>takma ad</b>).</span></div>
    <div class="anat-row"><span class="anat-label">JOIN suppliers s</span><span class="anat-body">Eklenecek tablo.</span></div>
    <div class="anat-row"><span class="anat-label">ON ... = ...</span><span class="anat-body">İki satırın <b>hangi koşulda</b> eşleştiği. Bu olmadan birleştirme anlamsız.</span></div>
  </div>
</figure>

`INNER JOIN` yalnızca **eşleşen** satırları getiriyor. Tabloda on iki ürün
var ama üçünün tedarikçisi kayıtlı değil; bu sorgu **dokuz** satır
döndürüyor.

Üç ürün sessizce kayboluyor. Hata yok, uyarı yok.

### Takma adlar

`p` ve `s` zorunlu değil ama neredeyse her zaman yazılıyor: sorgu kısalıyor
ve hangi sütunun hangi tablodan geldiği görünüyor.

Zorunlu olduğu bir durum var: **iki tabloda aynı adlı sütun varsa.**

```sql
SELECT name FROM products p JOIN categories c ON p.category_code = c.code;
-- hata: Ambiguous column name 'name'
```

İki tabloda da `name` sütunu var; sunucu hangisini istediğini bilemiyor.
`p.name` ya da `c.name` yazman gerekiyor.

## LEFT JOIN

Kaybolan üç ürünü de istiyorsan:

```sql
SELECT p.name, s.name AS supplier
FROM products p
LEFT JOIN suppliers s ON p.supplier_code = s.code;
```

Sonuç **on iki** satır. Eşleşme bulunamayan üç satırda sağ tablonun
sütunları `NULL` geliyor.

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h4>INNER JOIN</h4>
      <p>Yalnızca <b>eşleşenler</b>. Sol tablodan satır kaybedebilirsin.</p>
    </div>
    <div class="ok">
      <h4>LEFT JOIN</h4>
      <p><b>Soldaki her satır</b> kalıyor; eşleşme yoksa sağ taraf boş geliyor.</p>
    </div>
  </div>
  <figcaption>"Sol" ve "sağ", FROM ile JOIN'in iki yanı demek. RIGHT JOIN da var ama nadiren kullanılıyor: tabloların sırasını değiştirip LEFT yazmak daha okunur.</figcaption>
</figure>

### Eşleşmeyenleri bulmak

`LEFT JOIN`'in en çok işe yarayan kullanımı bu:

```sql
SELECT p.name
FROM products p
LEFT JOIN suppliers s ON p.supplier_code = s.code
WHERE s.code IS NULL;
```

"Tedarikçisi kayıtlı olmayan ürünler" — üç satır. Aynı kalıp "siparişi
olmayan müşteriler", "hiç satılmamış ürünler" için de kullanılıyor.

## Tuzak: LEFT JOIN'i öldüren WHERE

Bu, `JOIN` konusundaki en sık hata.

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>LEFT JOIN'i öldürüyor</h4>
      <pre><code>FROM products p
LEFT JOIN suppliers s
  ON p.supplier_code = s.code
WHERE s.country = 'Turkey'</code></pre>
    </div>
    <div class="ok">
      <h4>Sol tarafı koruyor</h4>
      <pre><code>FROM products p
LEFT JOIN suppliers s
  ON p.supplier_code = s.code
 AND s.country = 'Turkey'</code></pre>
    </div>
  </div>
  <figcaption>Soldaki 9, sağdaki 12 satır döndürüyor. Sebep: WHERE birleştirmeden sonra çalışıyor ve NULL olan satırlar koşulu sağlayamıyor — LEFT JOIN sessizce INNER JOIN'e dönüşüyor.</figcaption>
</figure>

Kural: **sağ tabloya bir koşul koyacaksan `ON` içine yaz**, `WHERE` içine
değil. `WHERE`, birleştirme bittikten sonra çalışıyor.

Tek istisna `IS NULL`: eşleşmeyenleri bulmak için bilerek `WHERE` içine
yazılıyor.

## Birden çok tabloyu birleştirmek

`JOIN` peş peşe yazılıyor:

```sql
SELECT o.id, c.name AS customer, p.name AS product, i.quantity
FROM orders o
JOIN customers c   ON o.customer_id = c.id
JOIN order_items i ON o.id = i.order_id
JOIN products p    ON i.product_id = p.id;
```

Her `JOIN` bir öncekinin sonucuna ekleniyor. Sıra okunabilirliği
etkiliyor ama sonucu değiştirmiyor — sunucu en verimli sırayı kendisi
seçiyor.

## Satırlar çoğalıyor

Bu, `JOIN` öğrenirken en çok şaşırtan şey.

`orders` tablosunda **10** sipariş var. `order_items` ile
birleştirdiğinde sonuç **20** satır oluyor: her siparişin birden çok
kalemi var ve sipariş bilgisi her kalem için tekrar ediyor.

Sonucu şöyle düşün: birleştirme yeni bir tablo üretiyor ve o tablonun
satır sayısı ikisinden de farklı olabiliyor.

**Somut sonucu:** birleştirmeden sonra `COUNT(*)` artık sipariş sayısını
vermiyor, kalem sayısını veriyor. Sipariş saymak istiyorsan
`COUNT(DISTINCT o.id)` yazman gerekiyor.

## Kendi kendine JOIN

Bir tablo kendisiyle de birleştirilebiliyor. Çalışanlar tablosunda her
kaydın yöneticisi yine aynı tabloda:

```sql
SELECT e.name, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

Aynı tabloya iki farklı takma ad veriliyor ve sunucu onları iki ayrı tablo
gibi görüyor. `LEFT JOIN` kullanıldı, çünkü en üstteki kişinin yöneticisi
yok — onun satırında `manager` boş geliyor.

## JOIN ve gruplama bir arada

```sql
SELECT c.name, COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.name;
```

Burada bir tuzak daha var:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">COUNT(o.id)</span><span class="anat-body">Siparişi olmayan müşteri için <b>0</b>. Doğrusu bu.</span></div>
    <div class="anat-row"><span class="anat-label">COUNT(*)</span><span class="anat-body">Aynı müşteri için <b>1</b>. Çünkü <code>LEFT JOIN</code> o müşteri için boş sütunlu bir satır üretiyor ve <code>COUNT(*)</code> satırları sayıyor.</span></div>
  </div>
  <figcaption>Ölçüldü: Quiet Partners'ın hiç siparişi yok. COUNT(*) 1 diyor, COUNT(o.id) 0 diyor.</figcaption>
</figure>

Kural: **`LEFT JOIN`'den sonra sağ tablonun bir sütununu say**, `*` değil.

## Özet

- Veri tablolara bölünüyor; `JOIN` onları geçici olarak birleştiriyor.
- `ON` iki satırın hangi koşulda eşleştiğini söylüyor.
- `INNER JOIN` yalnızca eşleşenleri, `LEFT JOIN` soldaki her satırı
  getiriyor.
- İki tabloda aynı adlı sütun varsa takma ad **zorunlu**.
- **`LEFT JOIN` + sağ tabloya `WHERE` = `INNER JOIN`.** Koşul `ON` içine
  yazılıyor.
- Eşleşmeyenleri bulmak için `LEFT JOIN ... WHERE sag.sutun IS NULL`.
- Birleştirme satırları **çoğaltabiliyor**; sayarken `DISTINCT`
  gerekebiliyor.
- `LEFT JOIN`'den sonra `COUNT(*)` değil, sağ tablonun sütununu say.
