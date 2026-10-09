# shutil ve glob

`os` ve `pathlib` tek bir dosyayla ya da klasörle uğraşır: aç, oku, adını
değiştir, sil. **Kopyalamak**, **bütün bir klasörü taşımak** ya da **içi dolu
bir klasörü silmek** için **`shutil`** (shell utilities, kabuk araçları)
kullanılır; terminalde `cp`, `mv`, `rm -r` ile yapılan işlerin Python'daki
karşılığı. **`glob`** ise `*.csv` gibi kalıplarla dosya bulur. Yedek alan,
yayın klasörü hazırlayan, eski kayıtları arşive taşıyan küçük betiklerin
hepsi bu iki modülle yazılır.

## Dosya kopyalamak

```python
import os
import shutil
from pathlib import Path

Path("report.txt").write_text("sales 120", encoding="utf-8")
Path("backup").mkdir()
print(shutil.copy("report.txt", "backup"))
print(shutil.copy2("report.txt", "backup/report-old.txt"))
print(sorted(p.name for p in Path("backup").iterdir()))
os.utime("report.txt", (1_700_000_000, 1_700_000_000))
shutil.copy("report.txt", "a.txt")
shutil.copy2("report.txt", "b.txt")
source_time = Path("report.txt").stat().st_mtime
copy_time = Path("a.txt").stat().st_mtime
copy2_time = Path("b.txt").stat().st_mtime
print(copy_time == source_time, copy2_time == source_time)
```

```text
backup\report.txt
backup/report-old.txt
['report-old.txt', 'report.txt']
False True
```

- **`shutil.copy(kaynak, hedef)`**: hedef bir klasörse dosya aynı adla
  içine kopyalanır; bir dosya yoluysa o adla. Yeni dosyanın yolunu döndürür.
- **`shutil.copy2`** aynı işi yapar, ek olarak dosyanın **değiştirilme
  zamanını** da korur. `os.utime` ile kaynağın zamanını geçmişe aldık:
  `copy` ile yapılan kopyanın zamanı "şimdi" oldu (`False`), `copy2`'ninki
  kaynağınkiyle aynı kaldı (`True`). Yedek alırken `copy2` tercih edilir;
  "en son ne zaman değişti" bilgisi kaybolmaz.

## Klasörler: copytree, move, rmtree

```python
import shutil
from pathlib import Path

for name in ["app/main.py", "app/utils.py", "app/debug.log",
             "app/__pycache__/main.cpython-314.pyc", "app/data/config.json"]:
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x", encoding="utf-8")
skip = shutil.ignore_patterns("__pycache__", "*.log")
shutil.copytree("app", "release", ignore=skip)
files = Path("release").rglob("*")
print(sorted(p.relative_to("release").as_posix() for p in files))
Path("dist").mkdir()
print(shutil.move("release", "dist"))
shutil.rmtree("app")
print(Path("app").exists(), Path("dist/release/main.py").exists())
```

```text
['data', 'data/config.json', 'main.py', 'utils.py']
dist\release
False True
```

- **`copytree(kaynak, hedef)`** klasörü içindekilerle birlikte kopyalar.
  **`ignore=shutil.ignore_patterns(...)`** atlanacak adları ve kalıpları
  verir: önbellek klasörü ve kayıt dosyası yayın klasörüne girmedi.
- **`shutil.move`** dosyayı ya da klasörü taşır; hedef var olan bir klasörse
  içine taşır ve yeni yolu döndürür. Başka bir diske taşırken kopyalayıp
  siler.
- **`shutil.rmtree`** klasörü **içindeki her şeyle birlikte, kalıcı olarak**
  siler. Geri dönüşüm kutusu yok, onay sorusu yok. Yolu yanlış hesaplanmış
  bir `rmtree` bütün bir proje klasörünü götürebilir; silmeden önce yolu
  yazdırıp kontrol etmek iyi bir alışkanlıktır.

## glob: kalıpla dosya bulmak

```python
import glob
from pathlib import Path

for name in ["data/sales_2024.csv", "data/sales_2025.csv", "data/stock.csv",
             "data/old/sales_2023.csv", "data/notes.txt"]:
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x", encoding="utf-8")
print(sorted(glob.glob("data/*.csv")))
for path in sorted(glob.glob("data/**/*.csv", recursive=True)):
    print(path)
print(sorted(glob.glob("data/sales_202?.csv")))
print(sorted(glob.glob("data/[!s]*")))
```

```text
['data\\sales_2024.csv', 'data\\sales_2025.csv', 'data\\stock.csv']
data\old\sales_2023.csv
data\sales_2024.csv
data\sales_2025.csv
data\stock.csv
['data\\sales_2024.csv', 'data\\sales_2025.csv']
['data\\notes.txt', 'data\\old']
```

| Kalıp | Anlamı |
|---|---|
| `*` | herhangi bir sayıda karakter (`/` hariç) |
| `?` | tek bir karakter |
| `[abc]` / `[!s]` | bu karakterlerden biri / `s` olmayan |
| `**` | her derinlikte klasör (`recursive=True` ile) |

`glob.glob` eşleşen yolları **metin listesi** olarak, sırasız verir;
`Path.glob` ise `Path` nesneleri üretir. Kalıplar aynıdır. Eski kodda
`glob.glob` çok görülür; yeni kodda ikisi de kullanılır.

`[!s]*` "`s` ile başlamayan her şey" demek: `notes.txt` dosyasıyla birlikte
`old` klasörü de geldi, çünkü kalıp yalnızca ada bakar.

## Diskte ne kadar yer var?

```python
import shutil

usage = shutil.disk_usage(".")
print(type(usage).__name__, usage._fields)
print(usage.free > 0)
```

```text
usage ('total', 'used', 'free')
True
```

`disk_usage` toplam, kullanılan ve boş alanı **bayt** olarak verir;
gigabayta çevirmek için `usage.free / 1024**3`. Büyük bir dosya yazmadan ya
da bir veri setini indirmeden önce yer olup olmadığına bakmak için kullanılır.

## Sık hatalar

```python
import shutil
from pathlib import Path

Path("report.txt").write_text("sales 120", encoding="utf-8")
shutil.copy("report.txt", "archive")
print(Path("archive").is_file(), Path("archive").is_dir())
Path("site").mkdir()
try:
    shutil.copytree("site", "site")
except FileExistsError:
    print("FileExistsError")
shutil.copytree("site", "site-copy")
shutil.copytree("site", "site-copy", dirs_exist_ok=True)
print(Path("site-copy").is_dir())
```

```text
True False
FileExistsError
True
```

- `archive` klasörü yokken `copy("report.txt", "archive")` hata vermedi:
  **`archive` adlı bir dosya** oluşturdu. Hedef klasörse önce onu aç.
- `copytree` hedef klasör varken `FileExistsError` verir; var olan klasörün
  üstüne kopyalamak için **`dirs_exist_ok=True`**.

## Özet

- `shutil.copy` (içerik), `copy2` (içerik + zaman), `copytree` (klasör,
  `ignore` ve `dirs_exist_ok` ile), `move`, `rmtree` (kalıcı!).
- `glob.glob(kalıp)` metin listesi; `*`, `?`, `[...]`, `**` +
  `recursive=True`.
- `shutil.disk_usage(yol)`: toplam, kullanılan, boş (bayt).
- Kopyalamadan önce hedef klasörün var olduğundan emin ol; silmeden önce
  yolu kontrol et.
