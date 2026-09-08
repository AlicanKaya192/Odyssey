Toplama işlevlerinin tek sayfalık listesi. Sonuç sütunundaki sayılar bu
bölümün `products` tablosunda gerçekten ölçüldü.

## İşlevler

| İşlev | Ne yapıyor | Örnek sonuç |
|---|---|---|
| `COUNT(*)` | satır sayar | `12` |
| `COUNT(sütun)` | o sütunu **dolu** olan satırları sayar | `COUNT(supplier_code)` → `9` |
| `COUNT(DISTINCT sütun)` | **farklı** değerleri sayar | `COUNT(DISTINCT category)` → `4` |
| `SUM(sütun)` | toplar | `SUM(stock)` → `329` |
| `AVG(sütun)` | ortalama alır | `AVG(price)` → `5108.75` |
| `MIN` / `MAX` | en küçük / en büyük | `95.00` / `24500.00` |

`MIN` ve `MAX` metinlerde de çalışıyor: alfabetik olarak ilk ve son değeri
veriyor.

## Boş değerlerle nasıl davranıyorlar

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">Hepsi atlıyor</span><span class="anat-body"><code>SUM</code>, <code>AVG</code>, <code>MIN</code>, <code>MAX</code> ve <code>COUNT(sütun)</code> boş hücreleri hesaba katmıyor.</span></div>
    <div class="anat-row"><span class="anat-label">COUNT(*) istisna</span><span class="anat-body">Sütunlara hiç bakmadığı için boş hücrelerden etkilenmiyor.</span></div>
    <div class="anat-row"><span class="anat-label">AVG'de dikkat</span><span class="anat-body">Boş hücreler <b>paydadan da</b> düşüyor. On siparişin üçünde kargo boşsa ortalama yediye bölünüyor, ona değil.</span></div>
  </div>
</figure>

Boşluğu sıfır saymak istiyorsan açıkça yazıyorsun:
`AVG(ISNULL(kargo, 0))`.

## Hiç satır yoksa

| Sorgu | Sonuç |
|---|---|
| `COUNT(*)` | `0` |
| `SUM(price)` | `NULL` |
| `AVG(price)` | `NULL` |
| `MIN` / `MAX` | `NULL` |
| `GROUP BY` ile | **hiç satır dönmez** |

`COUNT` tek istisna: "sıfır satır saydım" diyebiliyor. Diğerleri
"toplayacak bir şey yoktu" diyor.

Raporda sıfır görmek istiyorsan `ISNULL(SUM(price), 0)` yazıyorsun.

## Tam sayı tuzağı AVG'de de var

```sql
SELECT AVG(stock) FROM products;                         -- 27
SELECT AVG(CAST(stock AS DECIMAL(10,2))) FROM products;  -- 27.41
```

`stock` bir `INT`; toplam da tam sayı, bölüm de. Ondalık kısım atılıyor ve
sorgu hata vermiyor.

Ortalama hesaplarken sütunun türüne bakma alışkanlığı edinmek gerekiyor.

## GROUP BY kuralı

**`SELECT` içindeki her sütun ya `GROUP BY` listesinde olmalı ya da bir
toplama işlevinin içinde.**

```sql
-- calismaz: Accessory grubunda alti ad var, hangisi?
SELECT category, name, COUNT(*) FROM products GROUP BY category;

-- calisir: hangisini istedigini soyledin
SELECT category, MAX(name), COUNT(*) FROM products GROUP BY category;
```

## Sıra ve hangi parçanın neyi gördüğü

```
FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY
```

| Parça | Toplama işlevi | Takma ad |
|---|---|---|
| `WHERE` | **hayır** | hayır |
| `HAVING` | evet | **hayır** |
| `ORDER BY` | evet | **evet** |

Üç satırın üçü de aynı sebepten: bir parça, kendinden **sonra** çalışan
bir şeyi göremiyor.

## Sık kullanılan kalıplar

```sql
-- bir sutunda kac bos hucre var
SELECT COUNT(*) - COUNT(supplier_code) FROM products;

-- her grupta kac farkli deger
SELECT category, COUNT(DISTINCT supplier_code)
FROM products GROUP BY category;

-- yalnizca tek urunu olan kategoriler
SELECT category FROM products
GROUP BY category HAVING COUNT(*) = 1;

-- tekrar eden kayitlari bulmak
SELECT name, COUNT(*) FROM products
GROUP BY name HAVING COUNT(*) > 1;
```

Sonuncusu sahada en sık kullanılan gruplama sorgusu: mükerrer kayıt
aramak.
