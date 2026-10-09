# os ve sys

Bir program yalnızca hesap yapmaz; çalıştığı bilgisayarla da konuşur:
klasör açar, dosya adlarını listeler, ayarlarını ortamdan okur, hangi Python
sürümünde çalıştığına bakar, işi bitince bir çıkış koduyla kapanır. Bu
işlerin çoğu iki modülde:

- **`os`** (operating system, işletim sistemi): dosyalar, klasörler, yollar,
  ortam değişkenleri.
- **`sys`** (system): Python yorumlayıcısının kendisi: sürüm, komut satırı
  argümanları, modül arama yolu, çıkış.

## sys: yorumlayıcıya sormak

```python
import sys

print(sys.version_info[:2] >= (3, 10), sys.version_info.major)
print(sys.platform)
print(sys.argv)
print(type(sys.path).__name__, len(sys.path) > 0)
```

```text
True 3
win32
['main.py']
list True
```

- **`sys.version_info`** sürümü demet gibi verir; `(3, 10)` ile karşılaştırmak
  "en az 3.10 mu?" sorusudur. Metin olarak (`"3.9" < "3.10"`) karşılaştırma
  yanlış sonuç verir, demet doğru.
- **`sys.platform`** Windows'ta `win32` (64 bitte de), Linux'ta `linux`,
  macOS'ta `darwin`.
- **`sys.argv`** programın komut satırında aldığı argümanlar; ilk eleman
  betiğin adı. `python main.py rapor.csv` yazılsaydı `['main.py',
  'rapor.csv']` olurdu.
- **`sys.path`** `import` yazınca modüllerin arandığı klasörlerin listesi.

## Yollar: os.path

Dosya yolunu metinleri `+` ile yapıştırarak kurmak hatalara açıktır:
Windows `\`, Linux ve macOS `/` kullanır. **`os.path.join`** doğru
ayıracı kendisi koyar.

```python
import os

path = os.path.join("data", "raw", "sales.csv")
print(path)
print(os.path.basename(path), os.path.dirname(path))
print(os.path.splitext("sales.csv"), os.path.splitext("archive.tar.gz"))
print(os.path.exists(path), os.path.isabs(path))
```

```text
data\raw\sales.csv
sales.csv data\raw
('sales', '.csv') ('archive.tar', '.gz')
False False
```

- `basename` son parça (dosya adı), `dirname` öncesi (klasör).
- `splitext` adı ve **son** uzantıyı ayırır: `archive.tar.gz`'nin uzantısı
  `.gz`.
- `exists` yolun gerçekten var olup olmadığına bakar; burada öyle bir dosya
  yok. `isabs` yolun mutlak (`C:\...` ya da `/home/...`) olup olmadığını
  söyler; bu yol **göreli**, yani programın çalıştığı klasöre göre.

Windows'ta çıktıda `\` görüyorsun; aynı kod Linux'ta `data/raw/sales.csv`
yazar. Bir sonraki bölümdeki `pathlib` aynı işleri daha okunaklı yapar; ama
`os.path`'i eski kodda ve kütüphanelerde çok göreceksin.

## Klasör ve dosya işleri

```python
import os

os.makedirs(os.path.join("project", "data"), exist_ok=True)
os.makedirs(os.path.join("project", "data"), exist_ok=True)
for name in ["a.txt", "b.csv"]:
    with open(os.path.join("project", name), "w") as f:
        f.write("hello")
print(sorted(os.listdir("project")))
os.rename(os.path.join("project", "a.txt"), os.path.join("project", "notes.txt"))
os.remove(os.path.join("project", "b.csv"))
print(sorted(os.listdir("project")))
notes = os.path.join("project", "notes.txt")
print(os.path.isfile(notes), os.path.isdir(notes), os.path.getsize(notes))
```

```text
['a.txt', 'b.csv', 'data']
['data', 'notes.txt']
True False 5
```

- **`os.makedirs(yol, exist_ok=True)`** aradaki bütün klasörleri açar; klasör
  zaten varsa hata vermez (ikinci satır bunu gösteriyor).
- **`os.listdir`** klasörün içindekileri (dosya ve klasör) **sırasız**
  verir; bu yüzden `sorted`.
- `os.rename` adını değiştirir (ya da taşır), `os.remove` dosyayı **kalıcı
  olarak** siler; geri dönüşüm kutusuna gitmez.
- `isfile` / `isdir` ne olduğuna, `getsize` kaç bayt olduğuna bakar
  (`"hello"` 5 bayt).

## Bir ağacı dolaşmak: os.walk

Bir klasörü **alt klasörleriyle birlikte** dolaşmak için `os.walk`:

```python
import os

for folder in ["shop/data/old", "shop/src"]:
    os.makedirs(folder, exist_ok=True)
for name in ["shop/main.py", "shop/data/sales.csv",
             "shop/data/old/sales-2025.csv", "shop/src/app.py"]:
    open(name, "w").close()
for root, dirs, files in os.walk("shop"):
    dirs.sort()
    print(root, sorted(files))
```

```text
shop ['main.py']
shop\data ['sales.csv']
shop\data\old ['sales-2025.csv']
shop\src ['app.py']
```

`os.walk` her klasör için üç şey verir: klasörün yolu (`root`), içindeki alt
klasörlerin adları (`dirs`) ve dosyaların adları (`files`). Bir dosyanın tam
yolu `os.path.join(root, ad)`. `dirs.sort()` alt klasörlerin dolaşılma
sırasını sabitliyor; `dirs` listesinden bir ad silinirse o klasöre hiç
girilmez (`__pycache__` ya da `.git` gibi klasörleri atlamanın yolu).

## Ortam değişkenleri

**Ortam değişkenleri** (environment variables), programın dışından verilen
ad = değer ayarlarıdır: hangi portta çalışacağı, test kipinde olup olmadığı,
bir API anahtarı. Kodu değiştirmeden davranışı değiştirmenin yaygın yolu.

```python
import os

print(os.environ.get("ODYSSEY_MODE", "normal"))
os.environ["ODYSSEY_MODE"] = "test"
print(os.environ["ODYSSEY_MODE"], os.getenv("ODYSSEY_MODE"))
try:
    os.environ["ODYSSEY_PORT"] = 8080
except TypeError as error:
    print("TypeError:", error)
try:
    print(os.environ["ODYSSEY_MISSING"])
except KeyError as error:
    print("KeyError:", error)
```

```text
normal
test test
TypeError: str expected, not int
KeyError: 'ODYSSEY_MISSING'
```

- `os.environ` sözlük gibi çalışır. Olmayabilecek bir değişken
  **`get(ad, varsayılan)`** ya da `os.getenv` ile okunur; köşeli parantez
  yoksa `KeyError` verir.
- Değerler **her zaman metindir**: sayı yazılamaz, okunan `"8080"` de
  `int(...)` ile çevrilmelidir.
- Programın içinden değiştirilen değişken yalnızca bu programı (ve onun
  başlattıklarını) etkiler; bilgisayarın ayarı değişmez.

## Sık hatalar ve çıkış

```python
import os
import sys

try:
    os.mkdir(os.path.join("a", "b"))
except OSError as error:
    print(type(error).__name__)
os.makedirs("logs")
try:
    os.makedirs("logs")
except OSError as error:
    print(type(error).__name__)
try:
    sys.exit("stopped: no input file")
except SystemExit as error:
    print("SystemExit:", error.code)
```

```text
FileNotFoundError
FileExistsError
SystemExit: stopped: no input file
```

- `os.mkdir` yalnızca **bir** klasör açar; `a` yokken `a/b` istenince
  `FileNotFoundError`. Aradakileri de açmak için `makedirs`.
- `makedirs` klasör varken `exist_ok=True` olmadan `FileExistsError` verir.
- **`sys.exit`** programı bitirir. Aslında bir `SystemExit` hatası fırlatır;
  burada yakaladığımız için program sürdü. Metin verilirse ekrana yazılır ve
  çıkış kodu 1 olur; `sys.exit(0)` "başarıyla bitti" demektir. Komut
  satırı araçları ve otomatik işler bu koda bakar.

## Özet

- `sys.version_info` (demetle karşılaştır), `sys.platform`, `sys.argv`,
  `sys.path`, `sys.exit`.
- Yol `os.path.join` ile kurulur; `basename`, `dirname`, `splitext`,
  `exists`, `isfile`, `isdir`, `getsize`.
- `os.makedirs(..., exist_ok=True)`, `os.listdir` (sırasız), `os.rename`,
  `os.remove` (kalıcı).
- Ağacı dolaşmak `os.walk`: `root`, `dirs`, `files`.
- Ortam değişkeni `os.environ.get(ad, varsayılan)`; değerler metin.
