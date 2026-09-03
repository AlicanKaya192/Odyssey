Veriyi diskte tutmanın birden fazla yolu var. Hangisini ne zaman
kullanacağını bilmek, veri bilimine geçtiğinde işine yarayacak.

## Düz metin

En basit hâli: her satır bir kayıt.

```
Ada
Alan
Grace
```

```python
with open("names.txt", encoding="utf-8") as file:
    names = file.read().splitlines()
```

Tek bir bilgi listesi için yeterli. Birden fazla alan gerektiğinde yetmiyor.

## CSV — virgülle ayrılmış değerler

Veri biliminde en yaygın biçim. Her satır bir kayıt, alanlar virgülle ayrık,
ilk satır genelde başlık:

```
name,city,score
Ada,London,90
Alan,London,70
Grace,New York,85
```

Elle okumak öğretici:

```python
rows = []

with open("people.csv", encoding="utf-8") as file:
    lines = file.read().splitlines()

header = lines[0].split(",")

for line in lines[1:]:
    values = line.split(",")
    rows.append(dict(zip(header, values)))

print(rows[0])
```

```
{'name': 'Ada', 'city': 'London', 'score': '90'}
```

Sonuç `list[dict[str, str]]` — belirtim notunda çözdüğün biçimin ta kendisi.

**Dikkat:** bütün değerler **metin** olarak geliyor. `score` alanı `"90"`,
yani sayı değil. Hesap yapacaksan çevirmen gerekiyor:

```python
    row["score"] = int(row["score"])
```

### `csv` modülü

Python'un kendi modülü bu işi daha güvenli yapıyor:

```python
import csv

with open("people.csv", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

print(rows[0])
```

Neden daha güvenli? Çünkü bir alanın **içinde virgül** olabiliyor:

```
name,note
Ada,"born in London, England"
```

Elle `split(",")` yaparsan bu satır üç parçaya bölünüyor ve veri bozuluyor.
`csv` modülü tırnak içindeki virgülü görmezden geliyor.

`newline=""` argümanı Windows'ta satır sonlarının ikiye katlanmasını
engelliyor; `csv` ile birlikte hep yazılıyor.

## JSON — iç içe veri

CSV düz bir tablo. Verinin içinde liste ya da başka bir sözlük varsa CSV
yetmiyor. JSON o zaman devreye giriyor:

```json
{
  "name": "Ada",
  "languages": ["Python", "SQL"],
  "scores": {"math": 90, "logic": 95}
}
```

```python
import json

with open("profile.json", encoding="utf-8") as file:
    profile = json.load(file)

print(profile["languages"][0])
print(profile["scores"]["math"])
```

```
Python
90
```

Yazmak da aynı derecede kolay:

```python
with open("profile.json", "w", encoding="utf-8") as file:
    json.dump(profile, file, ensure_ascii=False, indent=2)
```

`ensure_ascii=False` Türkçe harflerin okunabilir kalmasını sağlıyor; olmadan
`ğ` gibi kaçış dizileri yazılıyor. `indent=2` de dosyayı insanın
okuyabileceği hâle getiriyor.

**JSON ile Python arasındaki karşılıklar:**

| JSON | Python |
|---|---|
| nesne `{}` | `dict` |
| dizi `[]` | `list` |
| metin | `str` |
| sayı | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

## Hangisini seçmeli?

| Biçim | Ne zaman |
|---|---|
| Düz metin | Tek sütunluk liste, kayıt dosyası |
| CSV | Düz tablo, çok satır, sayısal analiz |
| JSON | İç içe yapı, ayar dosyası, API cevabı |

Veri biliminde sıralama şöyle: veri çoğunlukla **CSV** gelir, ayarlar
**JSON** tutulur, kayıtlar **düz metne** yazılır.

## Bir uyarı

Bu bölümde dosyaları elle okuyorsun. Veri Bilimi patikasında pandas'ın
`read_csv` fonksiyonunu göreceksin ve tek satırda aynı işi yapacak:

```python
table = pandas.read_csv("people.csv")
```

O zaman "bunu neden elle öğrendim" diye düşünebilirsin. Cevabı şu: `read_csv`
bir gün bozuk bir satırda hata verdiğinde, ne olduğunu yalnızca burada
öğrendiğin şey sayesinde anlayabileceksin.
