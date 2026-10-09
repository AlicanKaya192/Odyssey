`pathlib` ile en sık yazılan küçük araçlardan biri, dağınık bir klasörü
düzenleyen betiktir: İndirilenler klasöründeki dosyaları türlerine göre alt
klasörlere taşımak gibi. Dosya taşıyan kod **yanlış çalışırsa geri almak
zordur**; bu yüzden iki alışkanlıkla yazılır.

## 1. Önce prova (dry run)

Fonksiyon önce yalnızca **ne yapacağını listeler**, hiçbir şeye dokunmaz;
liste doğruysa gerçekten çalıştırılır.

```python
from pathlib import Path

inbox = Path("inbox")
inbox.mkdir()
names = ["photo.jpg", "report.pdf", "data.csv", "notes.txt", "scan.PDF", "README"]
for name in names:
    (inbox / name).write_text("x", encoding="utf-8")


def organize(folder, dry_run=True):
    moves = []
    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue
        kind = path.suffix.lower().lstrip(".") or "other"
        moves.append(f"{path.name} -> {kind}/")
        if not dry_run:
            (folder / kind).mkdir(exist_ok=True)
            path.rename(folder / kind / path.name)
    return moves


for line in organize(inbox):
    print(line)
organize(inbox, dry_run=False)
files = [p for p in inbox.rglob("*") if p.is_file()]
for name in sorted(p.relative_to(inbox).as_posix() for p in files):
    print(name)
```

```text
data.csv -> csv/
notes.txt -> txt/
photo.jpg -> jpg/
README -> other/
report.pdf -> pdf/
scan.PDF -> pdf/
csv/data.csv
jpg/photo.jpg
other/README
pdf/report.pdf
pdf/scan.PDF
txt/notes.txt
```

- `suffix.lower()`: `scan.PDF` ile `report.pdf` aynı klasöre gitti.
- Uzantısı olmayan `README` için `"other"`: `suffix` boş metin, `or` yedeği
  devreye giriyor.
- `lstrip(".")` baştaki noktayı atıyor (`.pdf` → `pdf`).
- İlk çağrı yalnızca listeledi; ikinci çağrı (`dry_run=False`) taşıdı.

## 2. Üzerine yazma

Hedefte aynı adlı dosya varsa `rename` Windows'ta hata verir, Linux'ta ise
**sessizce üzerine yazar**: eski dosya kaybolur. Güvenli yol, boş bir ad
bulmaktır:

```python
from pathlib import Path


def unique_path(path):
    candidate = path
    counter = 1
    while candidate.exists():
        candidate = path.with_stem(f"{path.stem}-{counter}")
        counter += 1
    return candidate


report = Path("report.txt")
report.write_text("v1", encoding="utf-8")
print(unique_path(report))
unique_path(report).write_text("v2", encoding="utf-8")
print(unique_path(report))
```

```text
report-1.txt
report-2.txt
```

`with_stem` uzantıyı koruyup adı değiştiriyor. `report.txt` varken boş ad
`report-1.txt`; o da yazılınca `report-2.txt`.

## Kontrol listesi

- Önce prova, sonra gerçek çalıştırma.
- Taşımadan önce hedef klasörü aç (`mkdir(exist_ok=True)`).
- Hedefte aynı ad varsa yeni ad bul; üzerine yazma.
- Silmek yerine taşımayı tercih et (yanlışsa geri getirilir).
