Python'un yazdığı CSV'yi Excel'de açınca Türkçe harfler bozuk çıkıyorsa ya da
Excel'den gelen dosyanın ilk sütun adı tuhafsa, sebep çoğu zaman aynı:
**BOM**.

## BOM nedir?

**BOM** (byte order mark), bazı programların UTF-8 dosyanın en başına koyduğu
üç baytlık işarettir: `EF BB BF`. Excel, CSV'nin UTF-8 olduğunu **bu işaretten
anlar**; işaret yoksa dosyayı Windows'un eski kodlamasıyla açar ve `ş`, `ğ`,
`İ` bozulur. Python'da bu işaretli kodlamanın adı **`utf-8-sig`**.

```python
import csv

with open("excel.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerows([["name", "score"], ["Ada", "9,5"]])
print(open("excel.csv", "rb").read()[:12])
with open("excel.csv", newline="", encoding="utf-8") as f:
    print(next(csv.reader(f, delimiter=";")))
with open("excel.csv", newline="", encoding="utf-8-sig") as f:
    print(next(csv.reader(f, delimiter=";")))
```

```text
b'\xef\xbb\xbfname;scor'
['\ufeffname', 'score']
['name', 'score']
```

- Dosyanın ilk üç baytı `\xef\xbb\xbf`: BOM.
- `utf-8` ile okununca BOM ilk sütun adına yapıştı: `'﻿name'`. Ekranda
  `name` gibi görünür ama `row["name"]` **`KeyError`** verir; en sinsi CSV
  hatalarından biri.
- `utf-8-sig` ile okununca BOM atıldı. Bu kodlama BOM yoksa da sorunsuz
  okur; Excel'den gelen dosyalarda güvenli seçim.

## Excel için kontrol listesi

| Durum | Ne yap |
|---|---|
| Python'un yazdığı CSV Excel'de açılacak | `encoding="utf-8-sig"` |
| Türkçe/Avrupa Excel'i | `delimiter=";"`, ondalık virgül |
| Excel'den gelen CSV okunacak | `encoding="utf-8-sig"`, ayıraca bak |
| İlk sütun adı tutmuyor | BOM'dan şüphelen |
| Sayılar metin geliyor | `float(x.replace(",", "."))` |

## csv mi, pandas mı?

| | `csv` | pandas |
|---|---|---|
| Kurulum | yok, standart | ayrı paket |
| Bellek | satır satır okur | bütün tabloyu yükler |
| Tür çevirme | elle | kendiliğinden |
| Hesap, gruplama | elle | tek satır |

Küçük bir betik, kurulumsuz bir araç ya da belleğe sığmayacak kadar büyük
bir dosyayı satır satır işlemek için `csv`; tablo üstünde analiz için pandas.
