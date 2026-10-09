# Standart Kütüphane

Python'u kurduğunda yalnızca dil gelmez; yanında yüzlerce hazır **modül**
gelir: matematik, tarih ve saat, dosyalar, metin işleme, sıkıştırma,
veritabanı, ağ, test... Bunların hepsine **standart kütüphane** (standard
library) denir ve hiçbirini ayrıca kurman gerekmez. Python topluluğu bunu
"piller dahil" (batteries included) diye anlatır. Bu modülde standart
kütüphanenin en çok kullanılan parçalarını tek tek öğreneceksin; bu ilk
bölümde bir modülü nasıl içe aktaracağını, içine nasıl bakacağını ve standart
kütüphaneden olup olmadığını nasıl anlayacağını görüyoruz.

## Kaç modül var?

Python, standart kütüphanedeki modüllerin adlarını kendisi biliyor:
`sys.stdlib_module_names`.

```python
import sys

names = sys.stdlib_module_names
print(sys.version.split()[0], len(names))
public = sorted(n for n in names if not n.startswith("_"))
print(len(public))
print(public[:8])
```

```text
3.14.7 297
194
['abc', 'annotationlib', 'antigravity', 'argparse', 'array', 'ast', 'asyncio', 'atexit']
```

Bu bilgisayardaki Python 3.14'te 297 ad var; alt çizgiyle başlayanlar (`_json`
gibi) modüllerin içeride kullandığı yardımcı parçalar. Geriye kalan 194 modül
senin doğrudan kullanabileceklerin. Hepsini ezberlemek gerekmez: bu modülde
günlük işlerde en çok işe yarayan yaklaşık otuzunu öğreneceğiz.

## İçe aktarmanın biçimleri

Bir modülü kullanmak için önce **içe aktarırsın** (import). Dört yaygın yazım
var:

```python
import math                      # modülün tamamı: math.sqrt(...)
from math import sqrt, pi        # yalnızca iki ad: sqrt(...)
import statistics as st          # kısa takma ad: st.mean(...)
from datetime import date as d   # tek bir ada takma ad

print(math.sqrt(16), sqrt(16), round(pi, 4))
print(st.mean([2, 4, 9]), d(2026, 10, 9))
```

```text
4.0 4.0 3.1416
5 2026-10-09
```

`import math` ile her kullanımda `math.` yazarsın; uzun ama nereden geldiği
hep belli. `from math import sqrt` kısa, ama okuyan kişi `sqrt`'ün nereden
geldiğini dosyanın başına bakarak bulur. Takma ad (`as`) uzun modül adlarını
kısaltır; veri biliminde `import numpy as np`, `import pandas as pd` gibi
herkesin bildiği kısaltmalar kullanılır.

**`from math import *` yazma.** Modüldeki bütün adlar dosyana dökülür; kendi
değişkenin aynı adı taşıyorsa sessizce ezilir ve hangi adın nereden geldiği
anlaşılmaz.

## Modülün içine bakmak

Bir modülde ne olduğunu öğrenmenin iki yolu var: `dir()` adları listeler,
`help()` ya da `__doc__` açıklamayı gösterir.

```python
import math

public = [n for n in dir(math) if not n.startswith("_")]
print(len(public))
print(public[:6])
print(math.gcd.__doc__.splitlines()[0])
print(math.gcd(12, 18), math.comb(5, 2))
```

```text
62
['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2']
Greatest Common Divisor.
6 10
```

`math` modülünde 62 genel ad var. `__doc__` bir fonksiyonun belge metni;
etkileşimli kabukta `help(math.gcd)` aynı metni daha düzenli gösterir. Bir
fonksiyonun ne yaptığından emin değilsen ilk bakacağın yer burası, sonra
resmî belge (docs.python.org).

## Bir modül nereden geliyor?

Üç tür modül var: Python'un içine gömülü olanlar (**yerleşik**, built-in),
standart kütüphanenin `.py` dosyaları ve sonradan `pip` ile kurduğun
**üçüncü parti** paketler (NumPy, pandas gibi).

```python
import sys
import importlib.util


def kind(name):
    if name in sys.builtin_module_names:
        return "built-in"
    if name in sys.stdlib_module_names:
        return "standard"
    if importlib.util.find_spec(name) is not None:
        return "third-party"
    return "missing"


for name in ("math", "json", "numpy", "nosuchmodule"):
    print(name, kind(name))
```

```text
math built-in
json standard
numpy third-party
nosuchmodule missing
```

`math` C ile yazılıp Python'un içine gömülmüş, bu yüzden bir dosyası yok.
`json` standart kütüphanenin bir parçası, Python ile birlikte geliyor.
`numpy` bu bilgisayarda kurulu ama standart kütüphanede değil: onu kullanan
bir program başka bir bilgisayarda önce `pip install numpy` ister.
`find_spec` modülü **içe aktarmadan** bulunup bulunmadığına bakıyor.

Bu ayrım pratikte önemli: yalnızca standart kütüphane kullanan bir betik,
Python kurulu her bilgisayarda çalışır.

## Özet

- Standart kütüphane Python'la birlikte gelir; kurmak gerekmez.
- `import m`, `from m import a`, `import m as k`; `from m import *` yazma.
- `dir()` adları, `help()` ve `__doc__` açıklamayı gösterir.
- `sys.stdlib_module_names` standart kütüphanenin, `sys.builtin_module_names`
  yerleşik modüllerin listesi; `importlib.util.find_spec` bir modülün
  kurulu olup olmadığını içe aktarmadan söyler.
