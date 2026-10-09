# abc ve Protokoller

Python'da bir nesnenin ne olduğundan çok **ne yapabildiği** önemlidir:
`speak()` metodu varsa konuşabilir, `__len__` ve `__getitem__` varsa dizi
gibi kullanılabilir ("ördek gibi yürüyor ve ördek gibi ötüyorsa ördektir",
duck typing). Büyüyen bir projede bu sözleşmeyi **yazılı** hâle getirmek
gerekir: "her dışa aktarıcının bir `export` metodu olmalı". İki araç var:
**soyut temel sınıf** (`abc`) ve **protokol** (`typing.Protocol`).

## Soyut temel sınıf: ABC ve abstractmethod

```python
from abc import ABC, abstractmethod


class Exporter(ABC):
    @abstractmethod
    def export(self, rows: list[dict]) -> str:
        ...

    def save(self, rows: list[dict], path: str) -> int:
        text = self.export(rows)
        with open(path, "w", encoding="utf-8") as f:
            return f.write(text)


class CsvExporter(Exporter):
    def export(self, rows):
        header = ",".join(rows[0])
        lines = [",".join(str(v) for v in row.values()) for row in rows]
        return "\n".join([header, *lines])


class BrokenExporter(Exporter):
    def write(self, rows):
        return ""


rows = [{"name": "pen", "price": 1.5}, {"name": "ink", "price": 0.5}]
print(CsvExporter().export(rows))
print(CsvExporter().save(rows, "out.csv"))
for cls in (Exporter, BrokenExporter):
    try:
        cls()
    except TypeError as error:
        print("TypeError:", str(error).split(" without")[0])
```

```text
name,price
pen,1.5
ink,0.5
26
TypeError: Can't instantiate abstract class Exporter
TypeError: Can't instantiate abstract class BrokenExporter
```

- **`ABC`**'den türeyen ve **`@abstractmethod`** ile işaretli metodu olan
  sınıf **soyuttur**: kendisinden nesne kurulamaz.
- Alt sınıf soyut metodun hepsini yazmadıkça o da soyut kalır.
  `BrokenExporter` metodu yanlış adla (`write`) yazdı ve **nesne kurulurken**
  hata aldı; sözleşme bozukluğu kullanılmadan önce yakalandı.
- Soyut sınıf **ortak kodu** da taşıyabilir: `save`, alt sınıfın yazdığı
  `export`'u kullanıyor. Her yeni biçim (JSON, Excel) yalnızca `export`'u
  yazar, kaydetmeyi bedavaya alır.

## collections.abc: hazır sözleşmeler

```python
from collections.abc import Iterable, Mapping, Sequence

for value in [[1, 2], (1, 2), "ab", {"a": 1}, {1, 2}, 5, range(3)]:
    print(type(value).__name__, isinstance(value, Iterable),
          isinstance(value, Sequence), isinstance(value, Mapping))
```

```text
list True True False
tuple True True False
str True True False
dict True False True
set True False False
int False False False
range True True False
```

**`collections.abc`** yerleşik türlerin sözleşmelerini tanımlar:
**`Iterable`** dolaşılabilir, **`Sequence`** sıralı ve indekslenebilir
(liste, demet, metin, `range`), **`Mapping`** anahtar-değer (sözlük). Küme
dolaşılabilir ama sıralı değil; sayı hiçbiri değil. "Bu fonksiyon liste mi
istiyor, yoksa dolaşılabilir her şeyi mi?" sorusunu belirtimde de bunlarla
yanıtlarsın (`Iterable[int]`).

## Sözleşmeden bedava metotlar

```python
from collections.abc import Sequence


class Countdown(Sequence):
    def __init__(self, start: int):
        self.start = start

    def __len__(self):
        return self.start

    def __getitem__(self, index):
        if not 0 <= index < self.start:
            raise IndexError(index)
        return self.start - index


c = Countdown(5)
print(list(c), len(c), c[0], 3 in c)
print(list(reversed(c)), c.index(2), c.count(9))
```

```text
[5, 4, 3, 2, 1] 5 5 True
[1, 2, 3, 4, 5] 3 0
```

`Sequence`'ten türeyen sınıf yalnızca `__len__` ve `__getitem__`'ı yazdı;
dolaşma, `in`, `reversed`, `index` ve `count` hazır geldi. Soyut temel
sınıflar hem "şunları yazmalısın" der hem de "onları yazarsan bunlar
bedava".

## Protocol: miras olmadan sözleşme

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Speaker(Protocol):
    def speak(self) -> str:
        ...


class Dog:
    def speak(self) -> str:
        return "woof"


class Robot:
    def speak(self) -> str:
        return "beep"


class Rock:
    pass


def chorus(items: list[Speaker]) -> str:
    return " ".join(item.speak() for item in items)


print(chorus([Dog(), Robot()]))
print(isinstance(Dog(), Speaker), isinstance(Rock(), Speaker))
print(Speaker in Dog.__mro__)
```

```text
woof beep
True False
False
```

- **`Protocol`** "şu metotları olan her şey" der; sınıfların ondan
  **türemesi gerekmez**. `Dog` ve `Robot` `Speaker`'ı hiç anmadı ama ikisi de
  uyuyor (`Speaker in Dog.__mro__` → `False`).
- Tip denetleyicisi `chorus([Rock()])`'u yakalar: `Rock`'ın `speak`'i yok.
- **`@runtime_checkable`** ile `isinstance` de çalışır; ama yalnızca
  **adların** varlığına bakar (aşağıda tuzağı var).

Kendi kodunun dışındaki sınıflar (başka bir kütüphanenin nesneleri) için
protokol uygundur: onları senin temel sınıfından türetemezsin, ama
protokole uyuyorlarsa kullanabilirsin.

## Soyut özellik ve ortak davranış

```python
from abc import ABC, abstractmethod


class Shape(ABC):
    @property
    @abstractmethod
    def area(self) -> float:
        ...

    def describe(self) -> str:
        return f"{type(self).__name__} with area {self.area:.2f}"


class Square(Shape):
    def __init__(self, side: float):
        self.side = side

    @property
    def area(self) -> float:
        return self.side ** 2


class Circle(Shape):
    def __init__(self, r: float):
        self.r = r

    @property
    def area(self) -> float:
        return 3.14159 * self.r ** 2


for shape in [Square(3), Circle(1)]:
    print(shape.describe())
print(sorted(Shape.__abstractmethods__))
```

```text
Square with area 9.00
Circle with area 3.14
['area']
```

`@property` ile `@abstractmethod` birlikte: her şekil `area`'yı kendi
hesaplar, `describe` hepsinde ortak. `__abstractmethods__` alt sınıfların
doldurması gerekenleri listeler.

## Tuzak: runtime_checkable yalnızca ada bakar

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Closer(Protocol):
    def close(self) -> None:
        ...


class Fake:
    close = "not a method"


print(isinstance(Fake(), Closer))
try:
    Fake().close()
except TypeError as error:
    print("TypeError:", error)
```

```text
True
TypeError: 'str' object is not callable
```

`Fake`'in `close` adında bir **metni** var; `isinstance` adın varlığına
baktı ve `True` dedi, çağırınca hata geldi. Çalışma anındaki protokol
denetimi kaba bir süzgeçtir; asıl denetimi tip denetleyicisi yapar.

## ABC mi, Protocol mü?

| | `ABC` | `Protocol` |
|---|---|---|
| Uymak için | ondan türemek gerekir | türemek gerekmez |
| Eksik metot | nesne kurulurken `TypeError` | tip denetleyicisi uyarır |
| Ortak kod taşır mı | evet (`save`, `describe`) | genelde hayır |
| Uygun olduğu yer | kendi sınıf aileni kuruyorsan | başkalarının nesnelerini kabul ediyorsan |

## Özet

- `class X(ABC)` + `@abstractmethod`: alt sınıf yazmadıkça nesne kurulmaz.
- Soyut sınıf ortak kodu taşır; alt sınıf yalnızca soyut kısmı yazar.
- `collections.abc`: `Iterable`, `Sequence`, `Mapping`...; `Sequence`'ten
  türeyene `index`, `count`, `in` bedava.
- `Protocol`: miras olmadan yapısal sözleşme; `@runtime_checkable` ile
  `isinstance` (yalnızca adlara bakar).
