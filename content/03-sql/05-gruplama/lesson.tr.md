# Gruplama

Şimdiye kadar hep **satır** getirdin: on iki ürün, altı ürün, üç ürün. Bu
bölümde satırları **özetleyeceksin**: kaç ürün var, ortalama fiyat ne,
hangi kategoride kaç tane.

İki yeni parça var: satırları toplayan **işlevler** ve onları gruplara
bölen **`GROUP BY`**.

## Toplama işlevleri

Bir sütunun bütün satırlarına bakıp **tek bir sayı** üretiyorlar:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">COUNT(*)</span><span class="anat-body">Satır sayısı.</span></div>
    <div class="anat-row"><span class="anat-label">SUM(sütun)</span><span class="anat-body">Toplam.</span></div>
    <div class="anat-row"><span class="anat-label">AVG(sütun)</span><span class="anat-body">Ortalama.</span></div>
    <div class="anat-row"><span class="anat-label">MIN / MAX</span><span class="anat-body">En küçük / en büyük.</span></div>
  </div>
</figure>

```sql
SELECT COUNT(*), MIN(price), MAX(price) FROM products;
```

Sonuç **tek satır**: 12, 95.00, 24500.00.

### COUNT'un üç hâli

Bunlar üç ayrı soru soruyor ve üç farklı sayı veriyor:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">COUNT(*)</span><span class="anat-body"><b>12</b> — tablodaki satır sayısı. Sütunlara hiç bakmıyor.</span></div>
    <div class="anat-row"><span class="anat-label">COUNT(supplier_code)</span><span class="anat-body"><b>9</b> — o sütunu <b>dolu</b> olan satırlar. <code>NULL</code> sayılmıyor.</span></div>
    <div class="anat-row"><span class="anat-label">COUNT(DISTINCT category)</span><span class="anat-body"><b>4</b> — sütundaki farklı değer sayısı.</span></div>
  </div>
  <figcaption>Aradaki fark bir kaza değil, bilgi: 12 eksi 9 demek, üç satırda tedarikçi kayıtlı değil demek. Bir sütunda ne kadar eksik veri olduğunu görmenin en hızlı yolu bu.</figcaption>
</figure>

### Toplama işlevleri NULL değerleri atlıyor

`AVG(price)` boş hücreleri hesaba **katmıyor** — ne paya ne paydaya.

Bu çoğu zaman istediğin şey, ama bazen değil: "ortalama kargo ücreti"
hesaplarken kargosu girilmemiş siparişleri saymamak ortalamayı yukarı
çekiyor. Boşluğu sıfır saymak istiyorsan açıkça yazman gerekiyor:

```sql
AVG(ISNULL(kargo, 0))
```

Karar senin; sunucu senin yerine karar vermiyor, sessizce atlıyor.

### Boş sonuçta COUNT ile SUM farklı davranıyor

```sql
SELECT COUNT(*)  FROM products WHERE price > 999999;   -- 0
SELECT SUM(price) FROM products WHERE price > 999999;  -- NULL
```

Hiç satır yoksa `COUNT` **sıfır** diyor ama `SUM` **NULL** diyor —
"toplayacak bir şey yoktu" demek.

Bu ayrım raporlarda boş hücreye yol açıyor. Sıfır görmek istiyorsan
`ISNULL(SUM(price), 0)` yazıyorsun.

### AVG içinde tam sayı tuzağı

Dördüncü bölümdeki kural burada da geçerli:

```sql
SELECT AVG(stock) FROM products;                         -- 27
SELECT AVG(CAST(stock AS DECIMAL(10,2))) FROM products;  -- 27.41
```

`stock` bir `INT` sütunu; `AVG` de tam sayı üretiyor ve ondalık kısmı
atıyor. Hata yok, sadece yanlış ortalama.

## GROUP BY: gruplara bölmek

```sql
SELECT category, COUNT(*) AS adet
FROM products
GROUP BY category;
```

Dört satır geliyor — her kategori için bir tane:

```
category    adet
----------  ----
Accessory   6
Computer    2
Display     2
Software    2
```

`GROUP BY` satırları kümelere ayırıyor ve toplama işlevleri artık **her
küme için ayrı** çalışıyor.

### En sık görülen hata

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Hata verir</h4>
      <pre><code>SELECT category, name, COUNT(*)
FROM products
GROUP BY category;</code></pre>
    </div>
    <div class="ok">
      <h4>Doğrusu</h4>
      <pre><code>SELECT category, COUNT(*)
FROM products
GROUP BY category;</code></pre>
    </div>
  </div>
  <figcaption>Accessory grubunda altı ürün var; sunucu hangisinin adını yazacağını bilemiyor. Hata mesajı da bunu söylüyor: "Column products.name is invalid in the select list".</figcaption>
</figure>

Kural tek cümle: **`SELECT` içindeki her sütun ya `GROUP BY` listesinde
olmalı ya da bir toplama işlevinin içinde.**

Adı da görmek istiyorsan ne yapacağına karar etmen gerekiyor: hangisini?
En pahalısını mı (`MAX`), alfabetik ilkini mi (`MIN`), hepsini mi
(`STRING_AGG`)?

### NULL kendi grubunu kuruyor

```sql
SELECT supplier_code, COUNT(*) FROM products GROUP BY supplier_code;
```

Dört satır geliyor: `S1`, `S2`, `S3` ve bir de **NULL**.

Karşılaştırmada `NULL = NULL` "bilinmiyor" olduğu hâlde gruplamada iki
boş değer **aynı** gruba giriyor. Tutarsız görünüyor ama pratik: yoksa her
boş hücre kendi başına bir grup olurdu.

### Birden çok sütunla gruplamak

```sql
SELECT category, supplier_code, COUNT(*)
FROM products
GROUP BY category, supplier_code;
```

Artık grup, iki sütunun **birlikte** oluşturduğu her farklı çift. Sonuç
dokuz satır — kategori sayısından da tedarikçi sayısından da fazla.

## HAVING: grupları süzmek

"İkiden fazla ürünü olan kategoriler" demek istiyorsun. `WHERE` bunu
yapamıyor:

```sql
WHERE COUNT(*) > 2
-- hata: An aggregate may not appear in the WHERE clause
```

Çünkü `WHERE` **gruplar oluşmadan önce** çalışıyor; o sırada ortada
sayılacak bir grup yok.

Grupları süzen parça `HAVING`:

```sql
SELECT category, COUNT(*) AS adet
FROM products
GROUP BY category
HAVING COUNT(*) > 2;
```

<figure class="fig">
  <div class="versus">
    <div class="dim">
      <h4>WHERE</h4>
      <p>Gruplama <b>öncesi</b> çalışır, tek tek <b>satırları</b> eler.</p>
    </div>
    <div class="ok">
      <h4>HAVING</h4>
      <p>Gruplama <b>sonrası</b> çalışır, <b>grupları</b> eler.</p>
    </div>
  </div>
  <figcaption>İkisi birlikte de kullanılabiliyor: önce ilgilenmediğin satırları at, sonra kalanları grupla, sonra küçük grupları ele.</figcaption>
</figure>

```sql
SELECT category, COUNT(*) AS adet
FROM products
WHERE stock > 0
GROUP BY category
HAVING COUNT(*) >= 2;
```

Bu sorgu önce stokta olmayanları atıyor, sonra kategoriye göre gruplayıp
en az iki ürünü kalan kategorileri veriyor.

## Yeni işleme sırası

<figure class="fig">
  <div class="flow">
    <span class="node">FROM</span>
    <span class="arrow">-&gt;</span>
    <span class="node">WHERE<br>satır</span>
    <span class="arrow">-&gt;</span>
    <span class="node">GROUP BY</span>
    <span class="arrow">-&gt;</span>
    <span class="node">HAVING<br>grup</span>
    <span class="arrow">-&gt;</span>
    <span class="node">SELECT</span>
    <span class="arrow">-&gt;</span>
    <span class="node acc">ORDER BY</span>
  </div>
</figure>

Bu sıra üç şeyi birden açıklıyor:

- **`WHERE` içinde toplama işlevi olamıyor** — gruplar henüz yok.
- **`HAVING` içinde takma ad kullanılamıyor** — `SELECT` henüz
  çalışmamış. `HAVING adet > 2` yazarsan "Invalid column name" alıyorsun;
  `HAVING COUNT(*) > 2` yazman gerekiyor.
- **`ORDER BY` içinde takma ad kullanılabiliyor** — o en sonda.

```sql
SELECT category, COUNT(*) AS adet
FROM products
GROUP BY category
HAVING COUNT(*) > 1     -- takma ad burada olmaz
ORDER BY adet DESC;     -- burada olur
```

## Özet

- Toplama işlevleri satırları tek bir değere indiriyor: `COUNT`, `SUM`,
  `AVG`, `MIN`, `MAX`.
- `COUNT(*)` satırları, `COUNT(sütun)` **dolu** olanları,
  `COUNT(DISTINCT sütun)` **farklı** değerleri sayıyor.
- Toplama işlevleri boş değerleri atlıyor; hiç satır yoksa `COUNT` sıfır
  verirken `SUM` boş veriyor.
- `AVG` tam sayı sütununda tam sayı üretiyor — `CAST` gerekiyor.
- `GROUP BY` satırları kümelere ayırıyor; `SELECT`'teki her sütun ya
  gruplama listesinde ya bir işlevin içinde olmalı.
- Gruplamada bütün boş değerler **tek bir grup** oluyor.
- `WHERE` satırları gruplamadan **önce**, `HAVING` grupları **sonra**
  eliyor.
- `HAVING` takma adı göremiyor, `ORDER BY` görüyor.
