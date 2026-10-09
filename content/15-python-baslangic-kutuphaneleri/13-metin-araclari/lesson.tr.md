# Metin Araçları

Metin metotlarını (`upper`, `split`, `replace`, `strip`...) Python
patikasında gördün. Standart kütüphanede metinle ilgili birkaç modül daha
var ve her biri belli bir işi tek satıra indiriyor: noktalama karakterleri
listesi (`string`), uzun metni satırlara sarmak (`textwrap`), iki metnin ne
kadar benzediğini ve farkını bulmak (`difflib`), aksanlı harfler ve Unicode
(`unicodedata`). Bölümün sonunda Türkçe harflerin özel bir tuzağı var.

## string: hazır karakter listeleri

```python
import string

print(string.ascii_lowercase)
print(string.digits, string.punctuation)
text = "Hello, world! 2026."
print("".join(ch for ch in text if ch not in string.punctuation))
print(text.translate(str.maketrans("", "", string.punctuation)))
```

```text
abcdefghijklmnopqrstuvwxyz
0123456789 !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
Hello world 2026
Hello world 2026
```

- `string.ascii_lowercase`, `ascii_uppercase`, `digits`, `punctuation`:
  elle yazılması hem uzun hem hataya açık listeler.
- Noktalamayı silmenin iki yolu: kavramayla tek tek elemek ya da
  **`str.translate`**. `str.maketrans("", "", silinecekler)` bir çeviri tablosu
  kurar; `translate` metni tek geçişte dönüştürür, uzun metinlerde daha
  hızlıdır.

## textwrap: satırlara sarmak

```python
import textwrap

text = ("Python's standard library has a module for almost every "
        "everyday job, from dates to files.")
for line in textwrap.wrap(text, width=30):
    print(line)
print(textwrap.shorten(text, width=40, placeholder="..."))
print(textwrap.indent("first\nsecond", "> "))


def usage():
    return textwrap.dedent("""\
        Usage:
          report.py FILE
    """)


print(usage())
```

```text
Python's standard library has
a module for almost every
everyday job, from dates to
files.
Python's standard library has a...
> first
> second
Usage:
  report.py FILE
```

- **`wrap(metin, width)`** metni en fazla `width` karakterlik satırlara
  **kelime bölmeden** sarar, satır listesi verir; **`fill`** aynısını tek
  metin olarak.
- **`shorten`** sığmayanı kelime sınırında kesip sonuna işaret koyar:
  listelerde önizleme metni için.
- **`indent`** her satırın başına önek koyar (alıntı, kod bloğu).
- **`dedent`** ortak baştaki boşluğu siler: fonksiyonun içinde girintili
  yazılmış çok satırlı metin, ekranda soldan başlar. `"""\` sonundaki ters
  bölü ilk satır sonunu yutar.

## difflib: benzerlik ve fark

```python
import difflib

print(round(difflib.SequenceMatcher(None, "kitten", "sitting").ratio(), 3))
commands = ["start", "stop", "status", "restart", "help"]
print(difflib.get_close_matches("stat", commands))
print(difflib.get_close_matches("hlep", commands, n=1))
old = ["a = 1", "b = 2", "print(a + b)"]
new = ["a = 1", "b = 3", "print(a + b)", "print('done')"]
for line in difflib.unified_diff(old, new, lineterm=""):
    print(line)
```

```text
0.615
['start', 'status', 'restart']
['help']
--- 
+++ 
@@ -1,3 +1,4 @@
 a = 1
-b = 2
+b = 3
 print(a + b)
+print('done')
```

- **`SequenceMatcher(...).ratio()`** iki metnin benzerliği, 0 ile 1 arası.
- **`get_close_matches(kelime, seçenekler)`** en benzer seçenekleri verir
  (varsayılan en çok 3, benzerlik en az 0,6). Yanlış yazılan bir komuta
  "bunu mu demek istediniz?" önerisi tam olarak budur: `hlep` → `help`.
- **`unified_diff`** iki satır listesinin farkını, `git diff`'in biçiminde
  verir: `-` çıkan, `+` eklenen, boşlukla başlayan aynı kalan satır.

## unicodedata: aksanlar ve Unicode

```python
import unicodedata

word = "İstanbul"
print(word.lower(), len(word), len(word.lower()))
print(word.lower() == "istanbul", "ISPARTA".lower())


def strip_accents(text):
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


print(strip_accents("Café Ünlü Şeker"), strip_accents("ılık"))
a = "é"
b = "e" + chr(0x301)
print(a == b, len(a), len(b))
print(unicodedata.normalize("NFC", a) == unicodedata.normalize("NFC", b))
```

```text
i̇stanbul 8 9
False isparta
Cafe Unlu Seker ılık
False 1 2
True
```

- **Türkçe tuzağı:** Python büyük/küçük harf çevirirken dil bilmez.
  `"İstanbul".lower()` `i` + **birleşen nokta** (iki karakter) oldu: ekranda
  `i̇stanbul`, uzunluk 9, `"istanbul"`'a eşit değil. `"ISPARTA".lower()`
  `isparta` verdi, Türkçede doğrusu `ısparta`. Türkçe metinde arama ve
  karşılaştırma yaparken bu çeviriyi kendin yaparsın (ikinci not).
- **NFD** (ayrıştırma) `é`'yi `e` + "üstüne aksan" diye iki karaktere ayırır;
  aksan işaretlerinin kategorisi **`Mn`**. Onları atınca `Café` → `Cafe`,
  `Ünlü` → `Unlu`, `Şeker` → `Seker`. Ama **`ı` bir aksanlı `i` değil**,
  ayrı bir harftir: olduğu gibi kaldı.
- Aynı görünen iki metin farklı yazılmış olabilir: tek karakterlik `é` ile
  `e` + birleşen aksan. Karşılaştırmadan önce ikisini de **`NFC`** ile aynı
  biçime getir; dosyalardan ve web'den gelen metinde bu sık olur.

## string.Template: basit şablon

```python
from string import Template

t = Template("Dear $name, your order $order is ready.")
print(t.substitute(name="Ada", order=42))
print(t.safe_substitute(name="Ada"))
try:
    t.substitute(name="Ada")
except KeyError as error:
    print("KeyError:", error)
```

```text
Dear Ada, your order 42 is ready.
Dear Ada, your order $order is ready.
KeyError: 'order'
```

`$ad` yer tutucuları `substitute` ile doldurulur; eksik değer `KeyError`
verir, **`safe_substitute`** eksikleri olduğu gibi bırakır. f-string kodun
içinde yazılır; `Template` ise metin **kullanıcıdan ya da bir dosyadan**
geldiğinde güvenli seçimdir: içine kod yazılamaz.

## Özet

- `string.punctuation`, `digits`...; silmek için `str.translate`.
- `textwrap.wrap`, `fill`, `shorten`, `indent`, `dedent`.
- `difflib.SequenceMatcher(...).ratio()`, `get_close_matches`,
  `unified_diff`.
- `unicodedata.normalize("NFD"/"NFC", ...)`; aksan kategorisi `Mn`.
- Türkçe `I`/`İ` için `lower()`'a güvenme.
- `string.Template` dışarıdan gelen şablonlar için.
