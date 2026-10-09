# csv

**CSV** (comma-separated values, virgülle ayrılmış değerler) en yaygın veri
dosyası biçimidir: her satır bir kayıt, değerler virgülle ayrılmış, ilk satır
genelde sütun adları. Excel'den, bir veritabanından, bir web sitesinden
indirilen verinin çoğu CSV gelir. Python'un standart kütüphanesindeki
**`csv`** modülü bu dosyaları güvenle okur ve yazar. pandas daha büyük işler
için var (Veri Bilimi patikasında); ama küçük bir betikte, pandas'ın kurulu
olmadığı bir yerde ya da satır satır işlemek gerektiğinde `csv` yeter.

Bu bölümdeki kod blokları birbirinin devamıdır: bir blokta yazılan dosya
sonrakinde okunuyor.

## Neden split(",") yetmez?

```python
import csv
from pathlib import Path

Path("one.csv").write_text('Ada,"London, UK",36\n', encoding="utf-8")
line = Path("one.csv").read_text(encoding="utf-8").strip()
print(line.split(","))
with open("one.csv", newline="", encoding="utf-8") as f:
    print(next(csv.reader(f)))
```

```text
['Ada', '"London', ' UK"', '36']
['Ada', 'London, UK', '36']
```

Değerin içinde virgül varsa (`London, UK`) değer **tırnak içine** alınır.
`split(",")` tırnakları bilmiyor: üç değeri dört parçaya böldü ve tırnaklar
değerde kaldı. `csv.reader` kuralları biliyor: üç değer, tırnaksız.

## Yazmak: csv.writer

```python
import csv

rows = [
    ["name", "city", "age"],
    ["Ada", "London, UK", 36],
    ["Alan", "Wilmslow", 41],
    ['Grace "Amazing"', "New York", 85],
]
with open("people.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)
with open("people.csv", encoding="utf-8") as f:
    print(f.read())
```

```text
name,city,age
Ada,"London, UK",36
Alan,Wilmslow,41
"Grace ""Amazing""",New York,85
```

- `writerows` bir liste listesini, `writerow` tek satırı yazar.
- Virgül içeren değeri yazıcı **kendisi** tırnağa aldı; içinde tırnak olan
  değerde tırnağı **ikiledi** (`""Amazing""`). Elle `",".join(...)` yazsaydık
  bu kurallar bozulurdu.
- Sayılar (`36`) metne çevrilip yazıldı.
- **`newline=""`** her zaman verilir; nedeni sık hatalar bölümünde.

## Okumak: csv.reader

```python
with open("people.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)
print(header)
for row in rows:
    print(row)
print(rows[0][2] + rows[1][2], int(rows[0][2]) + int(rows[1][2]))
```

```text
['name', 'city', 'age']
['Ada', 'London, UK', '36']
['Alan', 'Wilmslow', '41']
['Grace "Amazing"', 'New York', '85']
3641 77
```

- `csv.reader` her satırı bir **liste** olarak verir; `next(reader)` ilk
  satırı (başlığı) alıp ayırır.
- **Bütün değerler metindir**: `"36" + "41"` toplama değil yapıştırma
  (`3641`). Sayıyla işlem yapmadan önce `int(...)` ya da `float(...)`.
- Dosya `with` bloğunun içinde okunmalı; blok bitince dosya kapanır ve
  `reader` artık okuyamaz. `list(reader)` satırları blok içinde topladı.

## Sütun adıyla: DictReader ve DictWriter

Satırı `row[2]` gibi sırayla okumak, sütunların yeri değişince bozulur.
**`DictReader`** her satırı başlıktaki adlarla bir **sözlük** yapar:

```python
with open("people.csv", newline="", encoding="utf-8") as f:
    people = list(csv.DictReader(f))
print(people[0])
print(sum(int(p["age"]) for p in people) / len(people))
with open("seniors.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"], extrasaction="ignore")
    writer.writeheader()
    writer.writerows(p for p in people if int(p["age"]) > 40)
with open("seniors.csv", encoding="utf-8") as f:
    print(f.read())
```

```text
{'name': 'Ada', 'city': 'London, UK', 'age': '36'}
54.0
name,age
Alan,41
"Grace ""Amazing""",85
```

- `p["age"]` sütunun yeri değişse de çalışır; kod da daha okunaklı.
- **`DictWriter`** sözlükleri yazar: `fieldnames` hangi sütunların hangi
  sırayla yazılacağını söyler, `writeheader()` başlık satırını yazar.
- Sözlükte `fieldnames`'te olmayan bir anahtar (`city`) varsa `DictWriter`
  hata verir; **`extrasaction="ignore"`** fazlalığı atlar.

## Noktalı virgül ve ondalık virgül

Türkçe ve birçok Avrupa dilinde ondalık ayıracı virgül olduğu için Excel bu
bölgelerde CSV'yi **noktalı virgülle** yazar: `3,50` fiyatı sütun ayıracıyla
karışmasın diye.

```python
from pathlib import Path

text = "product;price\npen;3,50\nbook;12,90\n"
Path("prices.csv").write_text(text, encoding="utf-8")
with open("prices.csv", newline="", encoding="utf-8") as f:
    prices = list(csv.DictReader(f, delimiter=";"))
print(prices)
print(round(sum(float(p["price"].replace(",", ".")) for p in prices), 2))
```

```text
[{'product': 'pen', 'price': '3,50'}, {'product': 'book', 'price': '12,90'}]
16.4
```

`delimiter=";"` ayıracı değiştirir. `float("3,50")` hata verir; Python'da
ondalık ayıracı nokta olduğu için önce `replace(",", ".")`.

## Sık hata: newline="" unutmak

```python
with open("broken.csv", "w", encoding="utf-8") as f:
    csv.writer(f).writerows([["a", "b"], [1, 2]])
print(Path("broken.csv").read_bytes())
with open("fixed.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows([["a", "b"], [1, 2]])
print(Path("fixed.csv").read_bytes())
```

```text
b'a,b\r\r\n1,2\r\r\n'
b'a,b\r\n1,2\r\n'
```

`csv` yazıcısı satır sonunu kendisi yazar (`\r\n`). `newline=""` verilmezse
Windows metin kipi `\n`'yi bir kez daha `\r\n`'ye çevirir ve satırlar
`\r\r\n` ile biter: dosya Excel'de **satır aralarında boş satırlarla**
açılır. Okurken de `newline=""` verilir; tırnak içinde satır sonu olan
değerler ancak böyle doğru okunur.

## Özet

- CSV'yi `split(",")` ile değil `csv` modülüyle oku ve yaz; tırnak kurallarını
  o biliyor.
- `open(..., newline="", encoding="utf-8")` her zaman.
- `csv.reader` / `csv.writer` listelerle, `DictReader` / `DictWriter`
  sözlüklerle; `writeheader()`, `extrasaction="ignore"`.
- Okunan her değer metin: `int`, `float` ile çevir.
- Avrupa Excel'i: `delimiter=";"` ve ondalık virgül (`replace(",", ".")`).
