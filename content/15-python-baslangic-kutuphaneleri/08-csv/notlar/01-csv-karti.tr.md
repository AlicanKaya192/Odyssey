## Açmak

```python
open("data.csv", newline="", encoding="utf-8")          # okumak
open("data.csv", "w", newline="", encoding="utf-8")     # yazmak
open("data.csv", newline="", encoding="utf-8-sig")      # Excel'den gelen
```

## Okumak

| Yazım | Ne verir |
|---|---|
| `csv.reader(f)` | her satır bir liste |
| `next(reader)` | sıradaki satır (başlığı ayırmak için) |
| `csv.DictReader(f)` | her satır bir sözlük (başlık anahtar) |
| `reader.fieldnames` | `DictReader`'da sütun adları |
| `csv.reader(f, delimiter=";")` | noktalı virgüllü dosya |

## Yazmak

| Yazım | Ne yapar |
|---|---|
| `csv.writer(f).writerow(liste)` | tek satır |
| `writer.writerows(listeler)` | çok satır |
| `csv.DictWriter(f, fieldnames=[...])` | sözlükleri yazar |
| `writer.writeheader()` | başlık satırı |
| `extrasaction="ignore"` | fazla anahtarları atla |
| `quoting=csv.QUOTE_ALL` | her değeri tırnağa al |

## Kurallar

- Değer virgül, tırnak ya da satır sonu içeriyorsa tırnağa alınır; tırnak
  ikilenir (`""`). `csv` bunu kendisi yapar.
- Okunan her değer **metin**; `int`, `float` ile çevir.
- Boş hücre `""` gelir; `int("")` hata verir, önce kontrol et.
- `newline=""` unutulursa Windows'ta satır araları boş çıkar.
