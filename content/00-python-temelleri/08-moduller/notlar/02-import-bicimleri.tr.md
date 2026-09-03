## Dört biçim, tek iş

```python
import math                      # math.sqrt(16)
from math import sqrt            # sqrt(16)
from math import sqrt, pi, floor # birden fazlasını al
import statistics as st          # st.mean(...)
from math import sqrt as karekok # aldığın şeye takma ad ver
```

Hepsi aynı kodu getiriyor; değişen sadece koddaki adı.

## `import` satırları nereye yazılır?

Dosyanın **en üstüne**, hepsi bir arada:

```python
import math
import random

from statistics import mean


def main():
    ...
```

Fonksiyonun içine de yazılabiliyor ama gerekmedikçe yazma; dosyanın neye
bağlı olduğu tek bakışta görünsün.

Sıralama âdeti şöyle: önce standart kütüphane, sonra kurduğun paketler, en
sonda kendi dosyaların. Aralarına boş satır konur.

## Hata 1: `ModuleNotFoundError`

```
ModuleNotFoundError: No module named 'pandas'
```

Modül bilgisayarında yok demek. İki sebebi olur: ya adını yanlış yazmışsındır
(`panda` değil `pandas`), ya da o modül standart kütüphanede değildir ve
kurulması gerekir.

Kendi dosyan için aynı hatayı alıyorsan, dosya çalıştırdığın dosyayla aynı
klasörde değildir.

## Hata 2: Dosyaya modül adı vermek

Bu, yeni başlayanların en çok düştüğü tuzak. Kendi dosyana `math.py` adını
verirsen:

```python
# math.py  <- kendi dosyan
import math
print(math.sqrt(16))
```

```
AttributeError: module 'math' has no attribute 'sqrt'
```

Python `math` diye kendi dosyanı buluyor ve gerçek `math` modülü yerine onu
getiriyor. Aynısı `random.py`, `json.py`, `string.py` için de geçerli.

**Kural: dosyalarına standart kütüphanedeki adları verme.**

## Hata 3: Döngüsel import

`a.py` içinde `import b`, `b.py` içinde `import a` varsa Python ikisini de
yarım bırakıyor ve tuhaf hatalar veriyor.

Genelde bu, iki dosyanın aslında tek bir iş yaptığının işaretidir. Ortak
kısmı üçüncü bir dosyaya alıp ikisinin de oradan almasını sağlamak çözüyor.

## `import` ne zaman çalışıyor?

Bir modül program boyunca **bir kez** çalıştırılıyor. İki farklı dosyadan
`import toolbox` yazsan bile `toolbox.py` yalnızca bir kez baştan sona
koşuyor; ikinci `import` hazır olanı veriyor.

Bu yüzden modül dosyasının en üstüne uzun süren bir iş koymak kötü fikir:
o modülü kim import ederse etsin o iş çalışıyor.

## `if __name__ == "__main__"` neyi çözüyor?

```python
# toolbox.py
def double(number):
    return number * 2

print(double(5))    # <- burası problem
```

Başka bir dosyadan `import toolbox` yazdığın anda ekrana `10` basılıyor —
sen sadece fonksiyonu almak istemiştin.

```python
if __name__ == "__main__":
    print(double(5))
```

Bu satır, "doğrudan çalıştırıldıysa" demek. Import edildiğinde `__name__`
değeri `"toolbox"` oluyor, `"__main__"` değil; koşul tutmuyor ve satır
atlanıyor.

## Küçük alışkanlıklar

- Kullanmadığın modülü import etme; dosyanın başındaki liste, dosyanın neye
  bağlı olduğunu anlatan bir belge.
- `from module import *` yazma.
- Takma adı keyfine göre uydurma; `pd`, `np`, `plt` gibi yerleşmiş olanları
  kullan, gerisinde modülün tam adını yaz.
