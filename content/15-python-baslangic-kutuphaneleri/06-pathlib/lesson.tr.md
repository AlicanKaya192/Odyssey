# pathlib

Önceki bölümde yolları `os.path` fonksiyonlarıyla, metin olarak işledik.
**`pathlib`** aynı işi **nesneyle** yapar: yol bir `Path` nesnesidir; adı,
uzantısı, klasörü onun özellikleridir; okumak, yazmak, listelemek onun
metotlarıdır. Kod daha kısa ve okunaklı olur; Python 3.4'ten beri standart
kütüphanede ve yeni kodda önerilen yol bu.

## Yol kurmak ve parçalarına bakmak

```python
from pathlib import Path

path = Path("data") / "raw" / "sales.csv"
print(path, path.as_posix())
print(path.name, path.stem, path.suffix)
print(path.parent, path.parent.name, path.parts)
print(path.with_suffix(".parquet").name, path.with_name("stock.csv").as_posix())
print(Path("archive.tar.gz").suffixes)
```

```text
data\raw\sales.csv data/raw/sales.csv
sales.csv sales .csv
data\raw raw ('data', 'raw', 'sales.csv')
sales.parquet data/raw/stock.csv
['.tar', '.gz']
```

- Yol **`/` işleciyle** birleştirilir: `Path("data") / "raw"`. Windows'ta da
  böyle yazılır; Python doğru ayıracı (`\`) kendisi koyar. `as_posix()` her
  yerde `/` ile yazar (çıktıda, raporda, web adresinde aynı görünsün diye).
- **`name`** dosya adı, **`stem`** uzantısız adı, **`suffix`** uzantı,
  **`suffixes`** bütün uzantılar.
- **`parent`** bir üst klasör (o da bir `Path`), `parts` parçaların demeti.
- **`with_suffix`** ve **`with_name`** uzantısı ya da adı değişmiş **yeni**
  bir yol döndürür; diskte hiçbir şey değişmez.

## Okumak, yazmak, silmek

```python
from pathlib import Path

folder = Path("project") / "data"
folder.mkdir(parents=True, exist_ok=True)
notes = folder / "notes.txt"
notes.write_text("first line\nsecond line\n", encoding="utf-8")
print(notes.exists(), notes.is_file(), folder.is_dir())
print(notes.read_text(encoding="utf-8").splitlines())
print(len(notes.read_text(encoding="utf-8").splitlines()))
renamed = notes.rename(folder / "todo.txt")
print(renamed.name, notes.exists())
renamed.unlink()
print(sorted(p.name for p in folder.iterdir()))
```

```text
True True True
['first line', 'second line']
2
todo.txt False
[]
```

- `mkdir(parents=True, exist_ok=True)`: `os.makedirs`'in karşılığı.
- **`write_text`** dosyayı açar, yazar, kapatır; **`read_text`** bütün
  içeriği metin olarak verir. `with open(...)` yazmaya gerek kalmaz. Küçük
  dosyalar için ideal; çok büyük dosyayı satır satır okumak için yine
  `open` kullanılır.
- **`encoding="utf-8"`** her zaman yazılır (aşağıda nedeni var).
- `rename` yeni yolu döndürür; eski yol artık yok. `unlink` dosyayı **kalıcı**
  siler.
- `iterdir()` klasörün içindekileri `Path` olarak verir; burada klasör boş
  kaldı.

## Dosya aramak: glob ve rglob

```python
from pathlib import Path

for name in ["shop/main.py", "shop/data/sales.csv", "shop/data/stock.csv",
             "shop/data/old/sales-2025.csv", "shop/src/app.py"]:
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x", encoding="utf-8")
shop = Path("shop")
print(sorted(p.name for p in shop.iterdir()))
print(sorted(p.name for p in (shop / "data").glob("*.csv")))
print(sorted(p.relative_to(shop).as_posix() for p in shop.rglob("*.csv")))
print(sorted(p.as_posix() for p in shop.glob("*/*.py")))
```

```text
['data', 'main.py', 'src']
['sales.csv', 'stock.csv']
['data/old/sales-2025.csv', 'data/sales.csv', 'data/stock.csv']
['shop/src/app.py']
```

- **`glob("*.csv")`** yalnızca o klasörde arar; `*` "herhangi bir ad".
- **`rglob("*.csv")`** alt klasörlere de iner (`os.walk`'un kısa yolu).
- `glob("*/*.py")` bir alt klasörün içindeki `.py` dosyaları: `main.py`
  doğrudan `shop`'ta olduğu için gelmedi.
- **`relative_to(shop)`** yolu `shop`'a göre göreli yapar.
- Sonuçlar sırasız gelir; ekranda sabit görünsün diye `sorted`.

Dosya yolunu kuran yerde de `parent.mkdir(...)` kalıbını görüyorsun:
"dosyayı yazmadan önce klasörü hazır et".

## Göreli ve mutlak yol

```python
from pathlib import Path

relative = Path("data") / "sales.csv"
full = relative.resolve()
print(relative.is_absolute(), full.is_absolute())
print(full.name, full.parent.name, full.parent.parent == Path.cwd())
```

```text
False True
sales.csv data True
```

`Path("data/sales.csv")` **göreli**dir: programın çalıştığı klasöre
(`Path.cwd()`) göre. **`resolve()`** onu tam (mutlak) yola çevirir. Ev
klasörü `Path.home()` ile alınır (`C:\Users\ad` ya da `/home/ad`); bir
programın ayar dosyasını oraya koyması yaygındır.

Programın kendi dosyasının yanındaki bir veri dosyasını, nereden
çalıştırılırsa çalıştırılsın bulmak için `Path(__file__).parent / "veri.csv"`
yazılır: `__file__` o an çalışan dosyanın yoludur.

## Sık hatalar

```python
from pathlib import Path

city = Path("city.txt")
city.write_text("Istanbul, İzmir, Muğla", encoding="utf-8")
print(city.read_text(encoding="utf-8"))
print(city.read_text(encoding="cp1252"))
try:
    print(Path("data") + "/sales.csv")
except TypeError as error:
    print("TypeError:", error)
try:
    Path("missing.txt").unlink()
except FileNotFoundError:
    print("FileNotFoundError")
Path("missing.txt").unlink(missing_ok=True)
print("done")
```

```text
Istanbul, İzmir, Muğla
Istanbul, Ä°zmir, MuÄŸla
TypeError: unsupported operand type(s) for +: 'WindowsPath' and 'str'
FileNotFoundError
done
```

- **Kodlama:** UTF-8 yazılan dosya başka bir kodlamayla okununca Türkçe
  harfler bozuldu (`İ` → `Ä°`). `encoding` verilmezse Python bilgisayarın
  varsayılanını kullanır ve bu Windows'ta çoğu zaman UTF-8 değildir: aynı
  kod senin bilgisayarında çalışıp başkasınınkinde bozulur. Yazarken de
  okurken de **`encoding="utf-8"`**.
- `Path`'e metin `+` ile eklenmez; `/` kullanılır.
- Olmayan dosyayı silmek hata verir; "varsa sil" için
  `unlink(missing_ok=True)`.

## os.path mi, pathlib mi?

| İş | `os.path` / `os` | `pathlib` |
|---|---|---|
| Birleştirmek | `os.path.join(a, b)` | `Path(a) / b` |
| Ad, uzantı | `basename`, `splitext` | `.name`, `.stem`, `.suffix` |
| Klasör | `os.path.dirname(p)` | `p.parent` |
| Var mı | `os.path.exists(p)` | `p.exists()` |
| Klasör aç | `os.makedirs(p, exist_ok=True)` | `p.mkdir(parents=True, exist_ok=True)` |
| Okumak | `open(p).read()` | `p.read_text(encoding=...)` |
| Ağaçta aramak | `os.walk` + `splitext` | `p.rglob("*.csv")` |

İkisi birbirinin yerine geçer; `open`, `pandas.read_csv` gibi fonksiyonlar
`Path` nesnesini de kabul eder. Yeni yazdığın kodda `pathlib` kullan.

## Özet

- Yol `Path("a") / "b"`; parçalar `name`, `stem`, `suffix`, `parent`.
- `with_suffix`, `with_name` yeni yol üretir; `as_posix()` her yerde `/`.
- `read_text` / `write_text` (her zaman `encoding="utf-8"`), `mkdir`,
  `rename`, `unlink`.
- `iterdir`, `glob` (o klasörde), `rglob` (alt klasörlerde de),
  `relative_to`.
- `resolve()` mutlak yol; `Path.cwd()`, `Path.home()`,
  `Path(__file__).parent`.
