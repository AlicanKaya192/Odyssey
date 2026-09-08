# Hesaplanan Sütunlar

Şimdiye kadar tabloda **duran** sütunları getirdin. Bu bölümde sonuçta
olmayan sütunlar üreteceksin: iki sütunu çarpacak, metni kısaltacak, sayıyı
yuvarlayacaksın.

`SELECT` yalnızca sütun seçmiyor — **ifade** de yazabiliyorsun.

## Aritmetik

```sql
SELECT ad, fiyat, stok, fiyat * stok AS stok_degeri
FROM urunler;
```

`fiyat * stok` diye bir sütun tabloda yok; sonuç üretilirken hesaplanıyor.
Tabloya hiçbir şey yazılmıyor.

Dört işlem ve kalan var: `+`, `-`, `*`, `/`, `%`. Öncelik matematikteki
gibi: `2 + 3 * 4` sonucu **14**.

### Tuzak: tam sayı bölmesi

Bu, SQL'e yeni gelenlerin en sık düştüğü yer.

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Beklenmeyen</h4>
      <pre><code>SELECT 7 / 2;
-- sonuc: 3</code></pre>
    </div>
    <div class="ok">
      <h4>Beklenen</h4>
      <pre><code>SELECT 7.0 / 2;
-- sonuc: 3.5</code></pre>
    </div>
  </div>
  <figcaption>İki tam sayıyı bölünce sonuç da tam sayı oluyor ve ondalık kısım atılıyor. Yuvarlama değil, kesme: 3,5 değil 3.</figcaption>
</figure>

Sütunlarla çalışırken de aynısı: `stok / 2` sütunu `INT` ise sonuç tam
sayı. Ondalıklı sonuç istiyorsan bir tarafı ondalıklı yapman gerekiyor:

```sql
SELECT stok / 2.0 AS yari
SELECT CAST(stok AS DECIMAL(10,2)) / 2 AS yari
```

Sorgu hata vermiyor, sessizce yanlış sayı veriyor. Bir raporda yüzde
hesabı tutmuyorsa ilk bakılacak yer burası.

### NULL bulaşıcı

```sql
SELECT 5 + NULL;   -- NULL
```

İçinde `NULL` geçen her aritmetik işlem `NULL` veriyor. `fiyat + kargo`
yazdığında kargo boşsa toplam da boş oluyor.

Çözüm boşluğa bir değer vermek: `fiyat + ISNULL(kargo, 0)`.

## Metin işlemleri

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">LEN(metin)</span><span class="anat-body">Karakter sayısı. <b>Sondaki boşlukları saymıyor</b> — aşağıda.</span></div>
    <div class="anat-row"><span class="anat-label">UPPER / LOWER</span><span class="anat-body">Büyük / küçük harfe çevirir.</span></div>
    <div class="anat-row"><span class="anat-label">TRIM(metin)</span><span class="anat-body">Baştaki ve sondaki boşlukları atar. Yalnızca bir tarafı için <code>LTRIM</code> / <code>RTRIM</code>.</span></div>
    <div class="anat-row"><span class="anat-label">LEFT(metin, n)</span><span class="anat-body">Baştan n karakter. Sondan almak için <code>RIGHT</code>.</span></div>
    <div class="anat-row"><span class="anat-label">SUBSTRING(metin, baslangic, uzunluk)</span><span class="anat-body">Ortadan parça alır. <b>Sayma 1'den başlıyor</b>, 0'dan değil.</span></div>
    <div class="anat-row"><span class="anat-label">REPLACE(metin, eski, yeni)</span><span class="anat-body">Geçen her yeri değiştirir.</span></div>
  </div>
</figure>

### Tuzak: LEN sondaki boşlukları saymıyor

```sql
SELECT LEN('abc   ');         -- 3
SELECT DATALENGTH('abc   ');  -- 6
SELECT LEN('   abc');         -- 6
```

`LEN` **sondaki** boşlukları görmezden geliyor ama **baştakileri**
sayıyor. Bu asimetri şaşırtıyor.

Gerçek uzunluk için `DATALENGTH` var; ama o da bayt sayıyor, karakter
değil — `NVARCHAR` sütunlarda karakter başına iki bayt.

## Metin birleştirme: + değil CONCAT

İki yol var ve **aynı şeyi yapmıyorlar**:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">'a' + NULL</span><span class="anat-body"><b>NULL</b> — tek bir boş parça bütün sonucu siliyor</span></div>
    <div class="anat-row"><span class="anat-label">CONCAT('a', NULL, 'b')</span><span class="anat-body"><b>'ab'</b> — boş parçayı atlıyor</span></div>
    <div class="anat-row"><span class="anat-label">'a' + 1</span><span class="anat-body"><b>hata</b> — metni sayıya çevirmeye çalışıyor</span></div>
    <div class="anat-row"><span class="anat-label">CONCAT('a', 1)</span><span class="anat-body"><b>'a1'</b> — sayıyı kendisi metne çeviriyor</span></div>
  </div>
  <figcaption>Ad ve soyadı `+` ile birleştiren bir sorgu, soyadı boş olan kişilerde bomboş bir hücre üretiyor. CONCAT bunu yapmıyor.</figcaption>
</figure>

Kural basit: **birleştirirken `CONCAT` kullan.** `+` yalnızca iki tarafın
da dolu ve metin olduğundan eminken güvenli.

## Sayı işlemleri

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">ROUND(sayi, basamak)</span><span class="anat-body">Yuvarlar. <code>ROUND(2.5, 0)</code> → 3, <code>ROUND(2.345, 2)</code> → 2.35</span></div>
    <div class="anat-row"><span class="anat-label">CEILING / FLOOR</span><span class="anat-body">Yukarı / aşağı tam sayıya. <code>CEILING(2.1)</code> → 3, <code>FLOOR(2.9)</code> → 2</span></div>
    <div class="anat-row"><span class="anat-label">ABS(sayi)</span><span class="anat-body">Mutlak değer.</span></div>
  </div>
</figure>

`ROUND` yarımları **sıfırdan uzağa** yuvarlıyor: 2,5 → 3 ve 3,5 → 4.
Python'un `round` işlevi bunu yapmıyor (o çift sayıya yuvarlıyor, `round(2.5)`
= 2); aynı hesabın iki dilde farklı çıkmasının sebebi bu.

## Tür çevirme: CAST ve TRY_CAST

```sql
SELECT CAST(fiyat AS INT) FROM urunler;
```

Çevrilemeyen bir değerde `CAST` **hata veriyor** ve sorgunun tamamı
düşüyor:

```sql
SELECT CAST('abc' AS INT);      -- Conversion failed
SELECT TRY_CAST('abc' AS INT);  -- NULL
```

`TRY_CAST` çeviremediğinde `NULL` veriyor ve sorgu devam ediyor. Verinin
temiz olduğundan emin değilsen `TRY_CAST` daha güvenli — özellikle
kullanıcıdan gelmiş metin sütunlarında.

## Hesaplanan sütun WHERE içinde

Geçen bölümlerde "takma ad `WHERE`'de kullanılamıyor" demiştik. Ama
**ifadenin kendisi kullanılabiliyor**:

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Çalışmaz</h4>
      <pre><code>SELECT fiyat * stok AS deger
FROM urunler
WHERE deger &gt; 100000;</code></pre>
    </div>
    <div class="ok">
      <h4>Çalışır</h4>
      <pre><code>SELECT fiyat * stok AS deger
FROM urunler
WHERE fiyat * stok &gt; 100000;</code></pre>
    </div>
  </div>
  <figcaption>Sebep aynı: WHERE, SELECT'ten önce çalışıyor. Takma ad henüz yok ama sütunlar var, yani hesabı orada tekrar yazabiliyorsun.</figcaption>
</figure>

`ORDER BY` en sonda çalıştığı için orada takma adı kullanabiliyorsun —
tekrar yazmana gerek yok.

### Hız notu

`WHERE` içinde bir sütunu **işlevin içine sokmak** indeksin
kullanılmasını engelliyor:

```sql
WHERE YEAR(tarih) = 2026        -- indeks kullanılamaz
WHERE tarih >= '2026-01-01'
  AND tarih <  '2027-01-01'     -- kullanılabilir
```

İkisi aynı satırları getiriyor ama ikincisi büyük tablolarda kat kat
hızlı. `LIKE '%x'` deseninin sorunuyla aynı sebep: sunucu nereden
başlayacağını bilemiyor.

## Özet

- `SELECT` içinde ifade yazabiliyorsun; sonuç tabloya yazılmıyor.
- **İki tam sayının bölümü tam sayı**: `7/2` → 3. Ondalık istiyorsan bir
  tarafı ondalıklı yap.
- Aritmetikte `NULL` bulaşıcı; `ISNULL` ile boşluğa değer ver.
- `LEN` **sondaki** boşlukları saymıyor, baştakileri sayıyor.
- Birleştirmede `CONCAT` kullan: `NULL`'ı atlıyor ve sayıyı kendisi
  çeviriyor.
- `ROUND` yarımları sıfırdan uzağa yuvarlıyor (2,5 → 3).
- Temizliğinden emin olmadığın veride `CAST` yerine `TRY_CAST`.
- `WHERE` içinde **takma ad** kullanılamıyor ama **ifade** kullanılabiliyor.
