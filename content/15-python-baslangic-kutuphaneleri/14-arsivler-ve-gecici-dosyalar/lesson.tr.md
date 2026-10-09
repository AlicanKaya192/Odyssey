# Arşivler ve Geçici Dosyalar

Birden çok dosyayı tek bir `.zip` olarak göndermek, büyük bir kayıt
dosyasını `.gz` ile küçültmek, indirilen bir arşivi açmak, bir işin ara
dosyalarını iş bitince iz bırakmadan silmek... Bunlar için standart
kütüphanede **`zipfile`**, **`gzip`**, **`shutil`**'in arşiv fonksiyonları ve
**`tempfile`** var. Bölümün sonunda arşiv açarken dikkat edilmesi gereken bir
güvenlik konusu var.

## zipfile: zip yazmak ve okumak

```python
import zipfile
from pathlib import Path

Path("report.txt").write_text("sales " * 1000, encoding="utf-8")
Path("notes.txt").write_text("short note", encoding="utf-8")
with zipfile.ZipFile("bundle.zip", "w", compression=zipfile.ZIP_DEFLATED) as zf:
    zf.write("report.txt")
    zf.write("notes.txt", arcname="docs/notes.txt")
    zf.writestr("readme.txt", "made by Python")
with zipfile.ZipFile("bundle.zip") as zf:
    print(zf.namelist())
    for info in zf.infolist():
        print(info.filename, info.file_size, info.compress_size)
    print(zf.read("docs/notes.txt").decode("utf-8"))
```

```text
['report.txt', 'docs/notes.txt', 'readme.txt']
report.txt 6000 35
docs/notes.txt 10 12
readme.txt 14 16
short note
```

- `ZipFile(ad, "w", compression=zipfile.ZIP_DEFLATED)` sıkıştırarak yazar;
  `compression` verilmezse dosyalar **sıkıştırılmadan** konur.
- `write(dosya)` diskteki dosyayı ekler; **`arcname`** arşivin içindeki adını
  (ve klasörünü) belirler. **`writestr(ad, metin)`** diskte dosya olmadan
  doğrudan içerik yazar.
- `namelist()` içindekilerin adları, `infolist()` her birinin bilgisi:
  `file_size` asıl boyut, `compress_size` arşivdeki boyut.
- `read(ad)` içeriği **bayt** olarak verir; metin için `.decode("utf-8")`.

Tekrarlı metin (6000 bayt) 35 bayta indi. Küçük dosyalar ise **büyüdü**
(10 → 12 bayt): sıkıştırmanın kendi ek bilgisi var, kısa metinde kazanılacak
tekrar yok.

## Arşivden çıkarmak

```python
import zipfile
from pathlib import Path

with zipfile.ZipFile("bundle.zip", "w") as zf:
    zf.writestr("readme.txt", "made by Python")
    zf.writestr("docs/notes.txt", "short note")
with zipfile.ZipFile("bundle.zip") as zf:
    zf.extract("readme.txt", "one")
    zf.extractall("all")
print(sorted(p.as_posix() for p in Path("one").rglob("*")))
print(sorted(p.as_posix() for p in Path("all").rglob("*") if p.is_file()))
```

```text
['one/readme.txt']
['all/docs/notes.txt', 'all/readme.txt']
```

`extract(ad, klasör)` tek bir dosyayı, `extractall(klasör)` hepsini çıkarır;
arşivdeki klasör yapısı (`docs/`) korunur.

## shutil ile tek satırda

```python
import shutil
from pathlib import Path

for name in ["site/index.html", "site/css/style.css"]:
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x", encoding="utf-8")
archive = shutil.make_archive("site-backup", "zip", root_dir="site")
print(Path(archive).name)
shutil.unpack_archive("site-backup.zip", "restored")
print(sorted(p.as_posix() for p in Path("restored").rglob("*") if p.is_file()))
print([name for name, _ in shutil.get_archive_formats()])
```

```text
site-backup.zip
['restored/css/style.css', 'restored/index.html']
['bztar', 'gztar', 'tar', 'xztar', 'zip', 'zstdtar']
```

Bütün bir klasörü arşivlemek **`shutil.make_archive(ad, biçim,
root_dir=klasör)`**, açmak **`shutil.unpack_archive`**. Uzantı biçimden
geliyor. `zip` dışında `tar` ailesi de var (`gztar` = `.tar.gz`); Python 3.14
ile Zstandard sıkıştırmalı `zstdtar` da geldi. Hangi dosyaların konacağını
tek tek seçmen gerekiyorsa `zipfile`, klasörün tamamıysa `shutil`.

## gzip: tek dosyayı sıkıştırmak

```python
import gzip
import random

text = "2026-03-15 INFO request ok\n" * 5000
data = text.encode("utf-8")
packed = gzip.compress(data)
print(len(data), len(packed), round(len(data) / len(packed)))
noise = random.Random(1).randbytes(100_000)
print(len(noise), len(gzip.compress(noise)))
with gzip.open("log.txt.gz", "wt", encoding="utf-8") as f:
    f.write(text)
with gzip.open("log.txt.gz", "rt", encoding="utf-8") as f:
    lines = f.read().splitlines()
print(lines[0], len(lines))
```

```text
135000 397 340
100000 100053
2026-03-15 INFO request ok 5000
```

- **`gzip`** tek bir dosyayı ya da bayt dizisini sıkıştırır (`.gz`);
  kayıt dosyaları ve büyük CSV'ler çoğunlukla böyle saklanır.
- Kendini tekrar eden kayıt metni **340 kat** küçüldü. Rastgele baytlar ise
  hiç küçülmedi, biraz büyüdü: sıkıştırma tekrarı kullanır, tekrar yoksa
  kazanç da yok. Zaten sıkıştırılmış dosyalar (`.zip`, `.png`, `.mp4`) da bu
  yüzden ikinci kez küçülmez.
- **`gzip.open(ad, "wt"/"rt", encoding=...)`** sıkıştırılmış dosyayı düz
  metin dosyası gibi yazar ve okur (`t` metin kipi). pandas da `.csv.gz`'yi
  doğrudan okur.

## tempfile: iz bırakmayan geçici dosyalar

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    work = Path(tmp)
    (work / "a.txt").write_text("x", encoding="utf-8")
    print(work.exists(), len(list(work.iterdir())))
print(work.exists())
with tempfile.NamedTemporaryFile(
        "w", suffix=".csv", delete=False, encoding="utf-8") as f:
    f.write("a,b\n")
    name = f.name
print(Path(name).suffix, Path(name).exists())
Path(name).unlink()
print(Path(name).exists(), Path(tempfile.gettempdir()).is_dir())
```

```text
True 1
False
.csv True
False True
```

- **`TemporaryDirectory()`** sistemin geçici klasöründe benzersiz adlı bir
  klasör açar; `with` bloğu bitince **içindekilerle birlikte siler**. Bir
  işin ara dosyaları, testler, indirip açıp işleyip atılan arşivler için.
- **`NamedTemporaryFile`** benzersiz adlı bir dosya; `delete=False` ile blok
  bitince silinmez (başka bir programa adını vermek için), sonra kendin
  silersin.
- Adı elle uydurmak (`temp.txt`) yerine bunları kullan: iki program aynı anda
  çalışınca birbirinin dosyasını ezmez.

## Güvenlik: arşivden dışarı yazan yollar

```python
import zipfile
from pathlib import Path

with zipfile.ZipFile("evil.zip", "w") as zf:
    zf.writestr("../outside.txt", "gotcha")
with zipfile.ZipFile("evil.zip") as zf:
    print(zf.namelist())
    zf.extractall("safe")
print(Path("../outside.txt").exists())
print(sorted(p.as_posix() for p in Path("safe").rglob("*")))
```

```text
['../outside.txt']
False
['safe/outside.txt']
```

Arşivdeki bir dosyanın adı `../outside.txt` gibi **klasörün dışını**
gösterebilir; buna "zip slip" denir ve kötü niyetli bir arşiv bilgisayardaki
başka dosyaların üstüne yazmaya çalışabilir. Python'un `zipfile`'ı `..`
parçalarını atıyor: dosya `safe/outside.txt` olarak çıktı, dışarıya bir şey
yazılmadı. `tarfile`'da Python 3.14'ten beri varsayılan `filter="data"` aynı
korumayı yapıyor. Yine de güvenmediğin arşivi her zaman **boş, ayrı bir
klasöre** aç.

## Özet

- `zipfile.ZipFile(..., "w", compression=ZIP_DEFLATED)`: `write`
  (`arcname`), `writestr`; okurken `namelist`, `infolist`, `read`, `extract`,
  `extractall`.
- `shutil.make_archive` / `unpack_archive`: bütün klasör tek satırda.
- `gzip.compress` / `gzip.open(..., "rt")`: tek dosya; tekrar varsa çok
  küçülür, yoksa küçülmez.
- `tempfile.TemporaryDirectory()`: blok bitince silinen klasör.
- Güvenmediğin arşivi boş bir klasöre aç.
