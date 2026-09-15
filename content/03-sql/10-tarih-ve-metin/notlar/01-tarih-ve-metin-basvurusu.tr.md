Bu bölümün işlevleri tek sayfada. Sonuçların hepsi gerçek sunucuda
ölçüldü; ayara bağlı olanlar ikinci notta.

## Tarih işlevleri

| İşlev | Örnek | Sonuç |
|---|---|---|
| `GETDATE()` | şu an | `DATETIME` |
| `SYSDATETIME()` | şu an | `DATETIME2` |
| `CAST(GETDATE() AS DATE)` | bugün | yalnızca gün |
| `DATEADD(day, 7, d)` | 8 Ocak | 15 Ocak |
| `DATEADD(month, 1, '2026-01-31')` | | `2026-02-28` |
| `DATEDIFF(day, a, b)` | 8 → 10 Ocak | `2` |
| `YEAR(d)`, `MONTH(d)`, `DAY(d)` | | parçalar |
| `EOMONTH(d)` | Şubat 2024 | `2024-02-29` |
| `EOMONTH(d, -1)` | Mart | Şubat'ın son günü |
| `DATEFROMPARTS(2026, 3, 1)` | | `2026-03-01` |

## DATEADD'in kırpması

| İfade | Sonuç |
|---|---|
| 31 Ocak + 1 ay | 28 Şubat |
| 31 Mart + 1 ay | 30 Nisan |
| 31 Mart − 1 ay | 28 Şubat |
| 29 Şubat 2024 + 1 yıl | 28 Şubat 2025 |
| 31 Ocak + 30 gün | 2 Mart |

Hedef ayda o gün yoksa ayın son günü.

## DATEDIFF sınır sayar

| Aralık | Birim | Sonuç |
|---|---|---|
| 31 Aralık → 1 Ocak | `year` | 1 |
| 1 Ocak → 31 Aralık (aynı yıl) | `year` | 0 |
| 31 Ocak → 1 Şubat | `month` | 1 |
| 10 Ocak → 8 Ocak | `day` | −2 |

Tam yıl gerekiyorsa `DATEDIFF(day, a, b) / 365`.

`DATEDIFF` tam sayı döndürüyor; ortalamasını alırken önce `DECIMAL`'e
çevir. Kargo süresinde FastLine'ın ortalaması tam sayıyla **2**, doğrusu
**2,67**.

## Ay başı ve ay sonu

```sql
DATEADD(day, 1, EOMONTH(d, -1))   -- bu ayin ilk gunu
EOMONTH(d)                        -- bu ayin son gunu
DATEADD(day, 1, EOMONTH(d))       -- sonraki ayin ilk gunu
```

## Dönem süzmek

```sql
WHERE d >= '2026-03-01' AND d < '2026-04-01'
```

Başlangıç dahil, bitiş hariç. Saatli değerlerde `BETWEEN` son günün
saatlerini kaçırıyor (dört olaydan `BETWEEN` 2'sini, yarı açık aralık
3'ünü buldu).

## Metin işlevleri (bu bölümün)

| İşlev | Örnek | Sonuç |
|---|---|---|
| `CHARINDEX(' ', 'Ada Kilic')` | | `4` |
| `CHARINDEX(' ', 'Madonna')` | bulamazsa | `0` |
| `STRING_AGG(ad, ', ') WITHIN GROUP (ORDER BY ad)` | gruplu | `Cable, Headset, ...` |
| `STRING_SPLIT('red,green,,blue', ',')` | | 4 satır, boş parça dahil |
| `CONCAT_WS(' - ', 'A', NULL, 'C')` | | `A - C` |
| `RIGHT('000' + CAST(1 AS VARCHAR(10)), 3)` | | `001` |
| `FORMAT(12, 'D3')` | | `012` |

Temel metin işlevleri (`LEN`, `UPPER`, `LEFT`, `SUBSTRING`, `REPLACE`,
`TRIM`, `CONCAT`) beşinci bölümde.

## Adı ve soyadı ayırmak

```sql
LEFT(name, CHARINDEX(' ', name) - 1)                 -- ad
SUBSTRING(name, CHARINDEX(' ', name) + 1, LEN(name)) -- soyad
```

Boşluk yoksa `CHARINDEX` 0, `LEFT(name, -1)` de hata veriyor:
`Invalid length parameter passed to the left function.`

## Göstermek

| İfade | Sonuç |
|---|---|
| `FORMAT(d, 'dd.MM.yyyy')` | `14.03.2026` |
| `FORMAT(d, 'MMMM yyyy', 'tr-TR')` | `Mart 2026` |
| `FORMAT(d, 'MMMM yyyy', 'en-US')` | `March 2026` |
| `CONVERT(NVARCHAR(10), d, 104)` | `14.03.2026` |

Sonuç metin; sıralama ve hesap için değil, yalnızca göstermek için.
