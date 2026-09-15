# Tarih ve Metin

Gerçek verinin çoğu ya bir tarih ya bir metin. Beşinci bölümde metnin
temel işlevlerini gördün: `LEN`, `UPPER`, `LEFT`, `SUBSTRING`, `REPLACE`,
`CONCAT`. Bu bölüm iki yeni şeye bakıyor: **tarihlerle hesap yapmak** ve
metinde **aramak ve toplamak**.

İkisinin ortak bir yanı var: sonuç sunucunun **ayarlarına** bağlı
olabiliyor. Aşağıdaki her şey ölçüldü, ve ayara bağlı olanlar ayrıca
belirtildi.

## Tarih tipleri

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">DATE</span><span class="anat-body">Yalnızca gün: <code>2026-03-14</code>. Sipariş tarihi, doğum günü.</span></div>
    <div class="anat-row"><span class="anat-label">DATETIME2</span><span class="anat-body">Gün ve saat: <code>2026-03-14 09:30:00</code>. Bir olayın anı.</span></div>
    <div class="anat-row"><span class="anat-label">DATETIME</span><span class="anat-body">Eski gün-saat tipi. Yeni tablolarda <code>DATETIME2</code> tercih ediliyor.</span></div>
  </div>
</figure>

Şu anki zaman `GETDATE()` ile `DATETIME`, `SYSDATETIME()` ile `DATETIME2`
olarak geliyor (ölçüldü). Yalnızca bugünün tarihi için:
`CAST(GETDATE() AS DATE)`.

## Tarihi güvenle yazmak

Bu, bölümün en sinsi tuzağı. Ölçüldü:

| Yazım | Ayar | `DATE` olarak | `DATETIME` olarak |
|---|---|---|---|
| `'2026-03-04'` | varsayılan | 4 Mart | 4 Mart |
| `'2026-03-04'` | `SET DATEFORMAT dmy` | 4 Mart | **3 Nisan** |
| `'03/04/2026'` | `SET DATEFORMAT dmy` | **3 Nisan** | — |
| `'03/04/2026'` | `SET DATEFORMAT mdy` | 4 Mart | — |
| `'20260304'` | her ayar | 4 Mart | 4 Mart |

Aynı metin, sunucunun tarih biçimi ayarına göre farklı bir güne dönüşüyor —
ve **hata vermiyor**. Eski `DATETIME` tipi tire ile yazılmış tarihi bile
yanlış okuyabiliyor.

Kural:

- **`DATE` sütunlarda `'YYYY-MM-DD'` güvenli.**
- **`DATETIME` ile çalışıyorsan bitişik yaz: `'20260304'`.**
- `'03/04/2026'` gibi eğik çizgili yazımı hiç kullanma.

## DATEADD: tarihe süre eklemek

```sql
SELECT DATEADD(day, 7, order_date) AS due_date FROM orders;
```

`DATEADD(birim, miktar, tarih)`. Birim `day`, `month`, `year`, `hour`
olabiliyor; eksi miktar geriye gidiyor.

Ay eklemek düşündüğünden ince bir iş — ölçüldü:

| İfade | Sonuç |
|---|---|
| 31 Ocak + 1 ay | **28 Şubat** |
| 31 Mart + 1 ay | **30 Nisan** |
| 31 Mart − 1 ay | 28 Şubat |
| 29 Şubat 2024 + 1 yıl | 28 Şubat 2025 |
| 31 Ocak + 30 gün | 2 Mart |

Hedef ayda o gün yoksa sunucu **ayın son gününe** kırpıyor. "1 ay sonra"
ile "30 gün sonra" aynı şey değil.

## DATEDIFF: iki tarih arası

```sql
SELECT DATEDIFF(day, o.order_date, s.shipped_date) AS days
FROM orders o JOIN shipments s ON s.order_id = o.id;
```

`DATEDIFF(birim, erken, geç)`. Sıra ters verilirse sonuç eksi çıkıyor
(`-2`, ölçüldü).

**Dikkat: `DATEDIFF` süre değil sınır sayıyor.** "Arada kaç tane yıl
başı var?" diye soruyor:

| Aralık | Birim | Sonuç |
|---|---|---|
| 31 Aralık 2025 → 1 Ocak 2026 (1 gün) | `year` | **1** |
| 1 Ocak 2025 → 31 Aralık 2025 (364 gün) | `year` | **0** |
| 31 Ocak → 1 Şubat (1 gün) | `month` | **1** |

Kıdem hesabında bu yanlış sonuç veriyor. 10 Ocak 2026 itibarıyla ölçüldü:

| Çalışan | İşe giriş | `DATEDIFF(year, ...)` | `DATEDIFF(day, ...) / 365` |
|---|---|---|---|
| Deniz Kaya | 5 Şubat 2024 | **2** | 1 |
| Fulya Demir | 30 Mayıs 2025 | **1** | 0 |

Deniz Kaya 1 yıl 11 aydır çalışıyor; yıl farkı "2" diyor. Tam yıl
gerekiyorsa gün farkını 365'e bölmek çok daha yakın.

## Parçalar, ay başı, ay sonu

```sql
SELECT YEAR(order_date), MONTH(order_date), DAY(order_date) FROM orders;
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">EOMONTH(tarih)</span><span class="anat-body">Ayın son günü: Şubat 2026 → <code>2026-02-28</code>, Şubat 2024 → <code>2024-02-29</code>.</span></div>
    <div class="anat-row"><span class="anat-label">EOMONTH(tarih, -1)</span><span class="anat-body">Önceki ayın son günü. Bir gün eklenince bu ayın ilk günü: <code>2026-03-01</code>.</span></div>
    <div class="anat-row"><span class="anat-label">DATEFROMPARTS(y, a, g)</span><span class="anat-body">Parçalardan tarih: <code>DATEFROMPARTS(2026, 3, 1)</code>. Olmayan gün (30 Şubat) <b>hata</b> veriyor.</span></div>
  </div>
</figure>

## Bir ayı süzmek

Mart siparişlerini bulmanın üç yolu var:

```sql
-- 1. yari acik aralik
WHERE order_date >= '2026-03-01' AND order_date < '2026-04-01'

-- 2. islevle
WHERE MONTH(order_date) = 3

-- 3. BETWEEN
WHERE order_date BETWEEN '2026-03-01' AND '2026-03-31'
```

Bu veride üçü de aynı üç siparişi getiriyor. Ama farkları var:

- İkincisi **her yılın** Mart'ını getiriyor; yıl için ayrıca `YEAR(...)`
  yazmak gerekiyor. Ayrıca sütuna işlev uyguladığı için, ileri seviyede
  göreceğin dizinlerden yararlanamıyor.
- Üçüncüsü **saatli** değerlerde yanılıyor. Ölçüldü — dört olayın durduğu
  bir `DATETIME2` sütunda:

| Süzgeç | Bulunan |
|---|---|
| `BETWEEN '2026-03-01' AND '2026-03-31'` | **2** |
| `>= '2026-03-01' AND < '2026-04-01'` | **3** |

`'2026-03-31'` saatsiz yazılınca "31 Mart gece yarısı" demek; 31 Mart
14:30'daki olay dışarıda kaldı.

**Kural: bir dönemi yarı açık aralıkla süz** — başlangıç dahil, bitiş
hariç. Her tipte ve her dönemde doğru çalışıyor.

## Tarihe göre gruplamak

```sql
SELECT YEAR(order_date) AS y, MONTH(order_date) AS m, COUNT(*) AS n
FROM orders
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY y, m;
```

Ölçüldü: Ocak 2, Şubat 3, Mart 3, Nisan 2 sipariş.

## Tarihi göstermek

Tarihin **tabloda nasıl durduğu** ile **ekranda nasıl göründüğü** ayrı
şeyler. Göstermek için:

```sql
FORMAT(order_date, 'dd.MM.yyyy')          -- 14.03.2026
FORMAT(order_date, 'MMMM yyyy', 'tr-TR')  -- Mart 2026
FORMAT(order_date, 'MMMM yyyy', 'en-US')  -- March 2026
CONVERT(NVARCHAR(10), order_date, 104)    -- 14.03.2026
```

Dördü de ölçüldü. `DATENAME(month, ...)` de ay adını veriyor ama
**oturumun diline göre**: bu sunucuda `March` ve `Saturday` çıktı. Adın
belli bir dilde olması gerekiyorsa `FORMAT`'a kültürü açıkça ver.

Gösterim işlevlerinin sonucu **metin**; onunla sıralamak ya da tarih
hesabı yapmak artık doğru çalışmaz. Biçimlendirmeyi en sona bırak.

## Metinde aramak: CHARINDEX

```sql
SELECT CHARINDEX(' ', 'Ada Kilic');   -- 4
```

Aranan parçanın **kaçıncı karakterde** başladığını söylüyor; yoksa `0`.
Adı ve soyadı ayırmak için:

```sql
SELECT LEFT(name, CHARINDEX(' ', name) - 1)              AS first_name,
       SUBSTRING(name, CHARINDEX(' ', name) + 1, LEN(name)) AS last_name
FROM employees;
```

Altı çalışanın altısında doğru ayırdı (ölçüldü). Ama **boşluk yoksa**
`CHARINDEX` 0 veriyor, `LEFT(name, -1)` de hata:
`Invalid length parameter passed to the left function.` Gerçek veride tek
kelimelik bir ad varsa bunu önceden düşünmek gerekiyor.

## Satırları tek metinde toplamak: STRING_AGG

```sql
SELECT category_code,
       STRING_AGG(name, ', ') WITHIN GROUP (ORDER BY name) AS products
FROM products
GROUP BY category_code;
```

Ölçüldü: `ACC` için `Cable, Headset, Keyboard, Microphone, Mouse, Webcam`.

`WITHIN GROUP (ORDER BY ...)` yazılmayınca sıra alfabetik olmadı —
`Keyboard, Mouse, Headset, Webcam, Cable, Microphone`, yani tabloya
eklendikleri sıra geldi. Sıra önemliyse yazılması şart.

Tersini `STRING_SPLIT` yapıyor: `STRING_SPLIT('red,green,,blue', ',')`
dört satır döndürdü, aradaki boş parça da dahil.

## Birkaç küçük araç

| İfade | Sonuç (ölçüldü) |
|---|---|
| `CONCAT_WS(' - ', 'A', NULL, 'C')` | `A - C` — ayırıcıyı kendisi koyuyor, boş parçayı atlıyor |
| `RIGHT('000' + CAST(1 AS VARCHAR(10)), 3)` | `001` — başa sıfır |
| `FORMAT(12, 'D3')` | `012` |

## Türkçe I tuzağı

Türkçede iki ayrı "i" var: noktalı (`i` / `İ`) ve noktasız (`ı` / `I`).
Sunucu Türkçe ayarlıysa büyük/küçük harf dönüşümü buna uyuyor. Ölçüldü:

| İfade | Türkçe ayarlı sunucu | Latin ayarlı |
|---|---|---|
| `UPPER('istanbul')` | `İSTANBUL` | `ISTANBUL` |
| `LOWER('ISTANBUL')` | `ıstanbul` | — |
| `WHERE city = 'istanbul'` | **0 satır** | 2 satır |
| `WHERE city LIKE 'ist%'` | **0 satır** | — |

Tabloda iki müşterinin şehri `Istanbul`. Türkçe ayarlı sunucuda küçük
harfle yapılan arama **hiçbirini bulmadı**: `I`'nın küçüğü `ı`, `i` değil.

Bu makinedeki sunucu Türkçe ayarlı. Arama kutusundan gelen metni
karşılaştırırken dil ayarını açıkça vermek sonucu sabitliyor:

```sql
WHERE city COLLATE Latin1_General_CI_AS = 'istanbul'   -- 2 satir
```

(Bu uygulamadaki SQL alıştırmaları hem Türkçe hem Latin ayarlı sunucuda
denendi; sonuçları ayara bağlı değil.)

## Özet

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Tarih yazmak</span><span class="anat-body"><code>DATE</code>'e <code>'YYYY-MM-DD'</code>, <code>DATETIME</code>'a <code>'YYYYMMDD'</code></span></div>
    <div class="anat-row"><span class="anat-label">Süre eklemek</span><span class="anat-body"><code>DATEADD</code> — ay eklerken ay sonuna kırpar</span></div>
    <div class="anat-row"><span class="anat-label">Fark</span><span class="anat-body"><code>DATEDIFF</code> — sınır sayar; kıdem için gün / 365</span></div>
    <div class="anat-row"><span class="anat-label">Dönem süzmek</span><span class="anat-body">Yarı açık aralık: <code>&gt;= başlangıç AND &lt; sonraki başlangıç</code></span></div>
    <div class="anat-row"><span class="anat-label">Göstermek</span><span class="anat-body"><code>FORMAT</code>, kültürü açıkça vererek — en sonda</span></div>
    <div class="anat-row"><span class="anat-label">Aramak / toplamak</span><span class="anat-body"><code>CHARINDEX</code>, <code>STRING_AGG ... WITHIN GROUP</code></span></div>
    <div class="anat-row"><span class="anat-label">Türkçe I</span><span class="anat-body">Karşılaştırmada <code>COLLATE</code> ile dil ayarını sabitle</span></div>
  </div>
</figure>

Orta Seviye burada bitiyor. İleri Seviyede önce **pencere
fonksiyonlarını** göreceksin: satırları gruplamadan her satıra grubunun
bilgisini eklemek.
