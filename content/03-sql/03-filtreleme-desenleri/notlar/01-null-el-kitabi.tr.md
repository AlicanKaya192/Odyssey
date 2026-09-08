`NULL` SQL'i başka dillerden ayıran şey. Bu not onunla ilgili her şeyi tek
yerde topluyor; bu bölümde gerekenden fazlası var ama ileride buraya
döneceksin.

## NULL nedir, ne değildir

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">NULL</span><span class="anat-body"><b>Değer bilinmiyor.</b> Hücrede bir şey yok.</span></div>
    <div class="anat-row"><span class="anat-label">0</span><span class="anat-body">Bir sayı. Bilinen bir değer, sadece sıfır.</span></div>
    <div class="anat-row"><span class="anat-label">''</span><span class="anat-body">Boş dize. Bilinen bir değer, sadece uzunluğu sıfır.</span></div>
  </div>
  <figcaption>Üçü üç ayrı şey. Bir ürünün stoğu 0 ise "stokta yok" demek; NULL ise "stok bilgisi girilmemiş" demek.</figcaption>
</figure>

## Üç değerli mantık

SQL'de bir koşulun üç olası sonucu var: **doğru**, **yanlış**,
**bilinmiyor**.

`WHERE` yalnızca **doğru** olan satırları alıyor. "Bilinmiyor" da
"yanlış" gibi eleniyor — bu yüzden `NULL` taşıyan satırlar sessizce
kayboluyor.

| İfade | Sonuç |
|---|---|
| `NULL = NULL` | bilinmiyor |
| `NULL <> NULL` | bilinmiyor |
| `NULL = 5` | bilinmiyor |
| `NULL > 5` | bilinmiyor |
| `NULL + 5` | `NULL` |
| `NULL IS NULL` | **doğru** |
| `NULL IS NOT NULL` | yanlış |

Son iki satır önemli: `IS NULL` bir karşılaştırma değil, **durum sorusu**.
Cevabı her zaman doğru ya da yanlış.

## `AND` ve `OR` bilinmeyenle nasıl davranıyor?

| İfade | Sonuç | Neden |
|---|---|---|
| `bilinmiyor AND yanlış` | **yanlış** | biri yanlışsa sonuç yanlış |
| `bilinmiyor AND doğru` | bilinmiyor | |
| `bilinmiyor OR doğru` | **doğru** | biri doğruysa sonuç doğru |
| `bilinmiyor OR yanlış` | bilinmiyor | |
| `NOT bilinmiyor` | bilinmiyor | bilinmeyenin tersi de bilinmiyor |

Son satır `NOT IN` tuzağının kaynağı.

## `NOT IN` tuzağı

```sql
WHERE kod NOT IN ('A', 'B', NULL)
```

**Hiçbir satır dönmüyor.** Sebebi:

```
kod <> 'A' AND kod <> 'B' AND kod <> NULL
                              ^^^^^^^^^^^^ her zaman bilinmiyor
```

Bir `AND` zincirinde bir parça bilinmiyorsa ve diğerleri doğruysa sonuç
"bilinmiyor" oluyor; "doğru" olamıyor.

`IN` (olumlu hâli) aynı sorunu yaşamıyor: orada `OR` zinciri var ve bir
parçanın doğru olması yetiyor.

**Korunma:** listeyi üreten sorguya `IS NOT NULL` ekle, ya da `NOT EXISTS`
kullan.

### Aynı tuzağın ikinci yüzü

`NOT IN` listesinde `NULL` olmasa bile, **sütunun kendisi `NULL` olan
satırlar düşüyor.**

Tabloda on iki ürün var; üçünün `tedarikci_kod` değeri `T1`, üçünün
`NULL`. Buna rağmen:

```sql
WHERE tedarikci_kod NOT IN ('T1')   -- 9 degil, 6 satir
```

Dokuz bekliyorsun (12 − 3), altı geliyor. Kayıp üç satır `NULL` olanlar:
`NULL <> 'T1'` karşılaştırmasının sonucu "bilinmiyor" ve `WHERE` onları
eliyor.

Aynısı `<>` için de geçerli: `WHERE tedarikci_kod <> 'T1'` de altı satır
veriyor.

Hepsini istiyorsan açıkça yazman gerekiyor:

```sql
WHERE (tedarikci_kod <> 'T1' OR tedarikci_kod IS NULL)
```

Bu, "olumsuz" bir koşul yazarken her seferinde sorulacak soru:
**sütunda `NULL` olabilir mi?** Olabiliyorsa o satırların ne olmasını
istediğine karar vermen gerekiyor.

## NULL'u değerle değiştirmek

| İşlev | Ne yapıyor |
|---|---|
| `ISNULL(sutun, 'yok')` | `NULL` ise ikinci değeri verir |
| `COALESCE(a, b, c)` | ilk `NULL` olmayanı verir |
| `NULLIF(a, b)` | a ile b eşitse `NULL`, değilse a |

`COALESCE` standart SQL, `ISNULL` SQL Server'a özgü. İkiden fazla seçenek
gerektiğinde `COALESCE` tek yol.

## NULL ve sıralama

SQL Server `NULL`'u **en küçük** sayıyor: `ASC` ile başta, `DESC` ile
sonda. PostgreSQL tersini yapıyor.

## İleride göreceklerin

- **Toplama işlevleri `NULL`'ları atlıyor.** `AVG(fiyat)` boş hücreleri
  hesaba katmıyor; `COUNT(*)` bütün satırları sayarken `COUNT(sutun)`
  yalnızca dolu olanları sayıyor.
- **`JOIN` sonucunda `NULL` üretiliyor.** `LEFT JOIN` eşleşme bulamadığı
  satırlar için sağ tablonun sütunlarını `NULL` yapıyor.
- **`UNIQUE` kısıtı birden çok `NULL`'a izin veriyor** (SQL Server'da bir
  taneye), çünkü iki bilinmeyen değerin eşit olup olmadığı bilinmiyor.
