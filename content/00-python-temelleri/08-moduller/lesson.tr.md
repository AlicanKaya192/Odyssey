# Modüller

Buraya kadar yazdığın her şey tek bir dosyanın içindeydi. Küçük programlarda
bu yeter. Ama dosya büyüdükçe iki sorun çıkıyor: aynı fonksiyonu başka bir
programda da kullanmak istiyorsun ve dosyayı bir yerden sonra kimse
okuyamıyor.

**Modül**, bunun çözümü: kodu ayrı dosyalara bölüyorsun ve gerekeni çağırıp
kullanıyorsun.

Bir şey daha var, belki daha önemlisi: Python'la birlikte **hazır yazılmış
binlerce fonksiyon** geliyor. Karekök almak, tarih hesaplamak, rastgele sayı
üretmek için sıfırdan kod yazman gerekmiyor. Sadece o kodu çağırmayı bilmen
yeterli.

## Modül nedir?

Modül, içinde Python kodu olan bir dosyadır. Hepsi bu.

`math.py` diye bir dosya var, içinde karekök alan bir fonksiyon duruyor. Sen
`import math` yazınca Python o dosyayı bulup çalıştırıyor ve içindekileri
senin kullanımına açıyor.

## `import` — modülü getir

```python
import math

print(math.sqrt(16))
print(math.floor(3.7))
print(math.ceil(3.2))
```

```
4.0
3
4
```

Dikkat et: `sqrt` fonksiyonunu doğrudan çağıramıyorsun, önüne `math.`
koyuyorsun. Bu nokta "şu modülün içindeki" demek.

`math.sqrt(16)` sonucu `4` değil `4.0` verdi — `sqrt` her zaman ondalıklı
sayı döndürüyor.

## `from ... import ...` — sadece gerekeni al

Her seferinde `math.` yazmak istemiyorsan, kullanacağın şeyi doğrudan
alabilirsin:

```python
from math import sqrt, pi

print(sqrt(25))
print(pi)
```

```
5.0
3.141592653589793
```

Bu sefer önüne bir şey koymadan çağırdın.

Hangisi doğru? İkisi de. Ama bir farkı var: `from math import sqrt` yazınca,
kodun geri kalanında `sqrt` adının nereden geldiği görünmüyor. `math.sqrt`
ise kendini anlatıyor. Bu yüzden çok fonksiyon kullanacaksan `import math`,
bir iki tane kullanacaksan `from math import ...` daha rahat.

## Yapma: `from math import *`

Böyle bir yazım da var ve modüldeki **her şeyi** getiriyor:

```python
from math import *   # bunu yapma
```

Sorun şu: modülde ne olduğunu bilmiyorsun. İçinde senin `pi` adında bir
değişkenin varsa, o an sessizce eziliyor ve hatayı saatler sonra buluyorsun.
Neyi aldığını yaz.

## `as` — takma ad

Uzun bir modül adını kısaltmak istersen:

```python
import statistics as st

print(st.mean([10, 20, 30]))
```

```
20
```

İleride veri bilimi tarafında bunu çok göreceksin: `import pandas as pd`,
`import numpy as np`. Bunlar herkesin kullandığı kısaltmalar; sen de aynısını
kullanırsan kodunu başkası okuduğunda hemen tanıyor.

## Kendi modülün

Modül sihirli bir şey değil, **senin yazdığın bir `.py` dosyası da modüldür.**

Aynı klasörde `toolbox.py` diye bir dosya olsun:

```python
# toolbox.py

def double(number):
    return number * 2

def greet(name):
    return "Hello, " + name
```

Yanındaki dosyadan çağırıyorsun:

```python
import toolbox

print(toolbox.double(21))
print(toolbox.greet("Ada"))
```

```
42
Hello, Ada
```

Dosya adı `toolbox.py`, modül adı `toolbox` — uzantıyı yazmıyorsun.

## Standart kütüphaneden birkaç tanıdık

Python'la birlikte gelen bu modüllere **standart kütüphane** deniyor. Hiçbir
kurulum gerektirmiyorlar:

| Modül | Ne işe yarar |
|---|---|
| `math` | Karekök, yuvarlama, `pi`, trigonometri |
| `random` | Rastgele sayı, listeden rastgele seçim |
| `statistics` | Ortalama, medyan, standart sapma |
| `datetime` | Tarih ve saat hesapları |
| `json` | JSON metnini Python nesnesine çevirmek |
| `os` | Klasör ve dosya yolları |

Birkaç örnek:

```python
import random

random.seed(42)          # aynı sonucu tekrar almak için
print(random.randint(1, 6))
```

```python
from datetime import date

today = date(2026, 3, 15)
print(today.year)
print(today.strftime("%d/%m/%Y"))
```

```
2026
15/03/2026
```

## Standart kütüphanede olmayanlar

Bir de dışarıdan kurulan modüller var — `pandas`, `requests`, `matplotlib`
gibi. Onlar Python'la gelmiyor, `pip install` ile bilgisayarına iniyor.

Bu uygulamadaki alıştırmalarda yalnızca standart kütüphaneyi kullanacaksın;
kurulum derdi yok.

## `if __name__ == "__main__"`

Modül dosyalarında sık göreceğin bir satır:

```python
# toolbox.py

def double(number):
    return number * 2

if __name__ == "__main__":
    print(double(5))
```

Anlamı şu: "bu dosya **doğrudan** çalıştırıldıysa şunu da yap; başka bir
dosya beni import ettiyse yapma."

Neden gerekli? Çünkü `import toolbox` yazdığın anda Python o dosyayı baştan
sona çalıştırıyor. O satır olmasaydı, sırf `double` fonksiyonunu kullanmak
istediğin için ekrana `10` basılırdı.

Şimdilik "deneme kodunu buraya koyuyorlar" diye aklının bir köşesinde dursun;
nesne tabanlı programlamaya geldiğimizde tekrar karşına çıkacak.

## Özet

- Modül, içinde kod olan bir `.py` dosyası. Seninkiler de dahil.
- `import math` → `math.sqrt(16)`
- `from math import sqrt` → `sqrt(16)`
- `import statistics as st` → `st.mean(...)`
- `from math import *` yazma; neyi aldığını belli et.
- Python'la gelen modüllere standart kütüphane deniyor; kurulum istemiyorlar.
