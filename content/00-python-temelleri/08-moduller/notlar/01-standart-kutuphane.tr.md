# Standart Kütüphaneden Sık Kullanılanlar

Bu not bir referans; baştan sona okumak zorunda değilsin. Alıştırma çözerken
"bunu yapan hazır bir şey var mıydı" diye aklına geldiğinde buraya bak.

## `math` — sayı işleri

```python
import math

math.sqrt(16)      # 4.0   karekök
math.floor(3.7)    # 3     aşağı yuvarla
math.ceil(3.2)     # 4     yukarı yuvarla
math.pi            # 3.141592653589793
math.gcd(12, 18)   # 6     en büyük ortak bölen
math.hypot(3, 4)   # 5.0   dik üçgende hipotenüs
```

`floor` ile `round` karıştırılıyor. `round` en yakına yuvarlar, `floor` her
zaman aşağı iner:

```python
round(3.7)         # 4
math.floor(3.7)    # 3
round(3.2)         # 3
math.floor(3.2)    # 3
```

## `random` — rastgelelik

```python
import random

random.randint(1, 6)          # 1 ile 6 arasında (6 dahil) tam sayı
random.choice(["a", "b"])     # listeden bir eleman
random.shuffle(my_list)       # listeyi karıştırır, yeni liste döndürmez
random.random()               # 0 ile 1 arasında ondalık
```

**Aynı sonucu tekrar almak** istiyorsan tohum veriyorsun:

```python
random.seed(42)
print(random.randint(1, 100))   # her çalıştırmada aynı sayı
```

Bu, hata ararken çok işe yarıyor: rastgele bir programda hatayı bulmak için
aynı rastgeleliği tekrar üretebilmen gerekiyor.

## `statistics` — özet sayılar

```python
from statistics import mean, median, stdev

scores = [70, 85, 90, 60, 95]

mean(scores)      # 80        ortalama
median(scores)    # 85        ortadaki değer
stdev(scores)     # 14.577...  standart sapma
```

Ortalama ile medyan arasındaki fark önemli. Listede bir tane çok uç değer
varsa ortalama kayar, medyan kaymaz:

```python
salaries = [30, 32, 35, 33, 900]
mean(salaries)     # 206
median(salaries)   # 33
```

Burada "tipik maaş" hangisi? Medyan. Veri biliminde bu soruyu çok
soracaksın.

## `datetime` — tarih ve saat

```python
from datetime import date, timedelta

start = date(2026, 3, 1)
end = date(2026, 3, 15)

(end - start).days      # 14
start + timedelta(days=30)   # 2026-03-31
start.strftime("%d/%m/%Y")   # "01/03/2026"
```

İki tarihi çıkarınca sayı değil, `timedelta` denen bir nesne çıkıyor; gün
sayısını ondan `.days` ile alıyorsun.

## `json` — metin ile nesne arasında

```python
import json

text = '{"name": "Ada", "age": 20}'
person = json.loads(text)       # metin  -> sözlük
person["name"]                  # "Ada"

back = json.dumps(person)       # sözlük -> metin
```

Bir API'den veri çektiğinde eline hep metin geçiyor; onu sözlüğe çeviren şey
bu modül.

## `os` ve `pathlib` — dosya yolları

```python
from pathlib import Path

Path("data") / "scores.csv"     # data/scores.csv
Path("scores.csv").exists()     # True / False
Path("scores.csv").suffix       # ".csv"
```

Yolları `"data/" + name` diye elle birleştirme; Windows'ta ayraç `\`,
Linux'ta `/` ve elle birleştirdiğin kod diğer bilgisayarda çalışmıyor.
`pathlib` bunu kendisi hallediyor.

Dosya okuma yazmayı bir sonraki bölümlerde ayrıntılı göreceğiz.

## Hangi modülde ne var?

Bir modülün içinde ne olduğunu Python'a sorabilirsin:

```python
import math
print(dir(math))       # modüldeki her şeyin listesi
help(math.sqrt)        # tek bir fonksiyonun açıklaması
```

`dir()` uzun bir liste basıyor ama aradığın şeyin adını hatırlamıyorsan işe
yarıyor.
