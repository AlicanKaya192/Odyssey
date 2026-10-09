# functools

Bu modül, standart kütüphanenin büyüyen programlarda işe yarayan yüzünü
anlatıyor. İlk durak **`functools`**: fonksiyonların üstünde çalışan
araçlar. Bir fonksiyonun sonuçlarını hatırlatmak (önbellek), bazı
argümanlarını önceden sabitlemek, bir listeyi tek değere indirmek ve
fonksiyonları **dekoratörle** sarmak.

## lru_cache: sonucu hatırlamak

```python
from functools import lru_cache

calls = 0


def fib(n):
    global calls
    calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print(fib(25), calls)
calls = 0


@lru_cache(maxsize=None)
def fast_fib(n):
    global calls
    calls += 1
    return n if n < 2 else fast_fib(n - 1) + fast_fib(n - 2)


print(fast_fib(25), calls)
print(fast_fib.cache_info())
print(fast_fib(100))
```

```text
75025 242785
75025 26
CacheInfo(hits=23, misses=26, maxsize=None, currsize=26)
354224848179261915075
```

- Özyinelemeli `fib(25)` aynı değerleri tekrar tekrar hesaplıyor: **242 785
  çağrı**.
- **`@lru_cache`** fonksiyonun her argüman için sonucunu saklar; aynı
  argümanla ikinci çağrıda hesaplamadan döndürür. Aynı sonuç **26 çağrıyla**
  geldi, `fib(100)` de anında.
- **`cache_info()`** önbelleğin karnesi: `hits` (önbellekten gelen),
  `misses` (hesaplanan), `currsize` (saklanan sonuç sayısı).
- `maxsize=None` sınırsız saklar; bir sayı verilirse en uzun süredir
  kullanılmayanı atar (LRU: least recently used).

Önbellek yalnızca **aynı girdiye hep aynı sonucu veren** fonksiyonlarda
doğrudur: dosya okuyan, saate bakan ya da rastgele sayı üreten bir
fonksiyonun sonucunu saklamak eski sonucu döndürür.

## Dekoratör nedir?

`@lru_cache` bir **dekoratör** (decorator): bir fonksiyonu alıp onu saran
yeni bir fonksiyon döndüren fonksiyon. `@ad` yazmak, tanımın hemen ardından
`f = ad(f)` yazmakla aynı şeydir.

```python
from functools import wraps


def shout(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper


def polite(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) + ", please"
    return wrapper


@shout
def greet(name):
    """Return a greeting."""
    return f"hello, {name}"


@polite
def ask(thing):
    """Ask for a thing."""
    return f"pass the {thing}"


print(greet("ada"))
print(greet.__name__, greet.__doc__)
print(ask("salt"))
print(ask.__name__, ask.__doc__)
```

```text
HELLO, ADA
wrapper None
pass the salt, please
ask Ask for a thing.
```

- `wrapper` asıl fonksiyonu çağırıyor ve sonucunu değiştiriyor;
  `*args, **kwargs` gelen bütün argümanları olduğu gibi aktarır.
- Sarılan `greet` artık `wrapper`: adı `wrapper`, açıklaması kayboldu. Hata
  mesajlarında ve belgelerde yanlış ad görünür.
- **`@wraps(func)`** sarmalayıcıya asıl fonksiyonun adını ve açıklamasını
  kopyalar. Kendi dekoratörünü yazarken her zaman kullan.

Dekoratörler kayıt tutmak, süre ölçmek, yetki denetlemek, yeniden denemek
gibi "her fonksiyona aynı ek iş" için kullanılır; ikinci not bunu örnekliyor.

## partial ve reduce

```python
import operator
from functools import partial, reduce


def power(base, exponent):
    return base ** exponent


square = partial(power, exponent=2)
cube = partial(power, exponent=3)
print(square(5), cube(2), list(map(square, [1, 2, 3])))
from_binary = partial(int, base=2)
print(from_binary("1010"), from_binary("11111111"))
print(reduce(operator.mul, [1, 2, 3, 4, 5]))
print(reduce(lambda a, b: a if a > b else b, [3, 9, 2]))
print(reduce(operator.add, [], 0))
```

```text
25 8 [1, 4, 9]
10 255
120
9
0
```

- **`partial(f, ...)`** bazı argümanları önceden doldurulmuş yeni bir
  fonksiyon üretir: `square` üssü 2'ye sabitlenmiş `power`. Bir fonksiyonu
  `map`'e, bir düğmeye ya da bir sıralamaya **tek argümanlı** vermek
  gerektiğinde işe yarar.
- **`reduce(f, dizi)`** diziyi soldan sağa tek değere indirir:
  `((((1×2)×3)×4)×5) = 120`. Üçüncü argüman başlangıç değeridir; boş dizide
  onsuz hata verir.
- **`operator`** modülü `+`, `*` gibi işleçlerin fonksiyon hâlini verir
  (`operator.mul`), `lambda` yazmaya gerek kalmaz. Toplam için zaten `sum`,
  en büyük için `max` var; `reduce` daha özel birikimler için.

## Sınıflar için: cached_property ve total_ordering

```python
from functools import cached_property, total_ordering


class Report:
    def __init__(self, values):
        self.values = values
        self.computed = 0

    @cached_property
    def total(self):
        self.computed += 1
        return sum(self.values)


r = Report([1, 2, 3])
print(r.total, r.total, r.computed)


@total_ordering
class Version:
    def __init__(self, major, minor):
        self.major, self.minor = major, minor

    def __eq__(self, other):
        return (self.major, self.minor) == (other.major, other.minor)

    def __lt__(self, other):
        return (self.major, self.minor) < (other.major, other.minor)


a, b = Version(1, 2), Version(1, 10)
print(a < b, a >= b, a != b, max(a, b).minor)
```

```text
6 6 1
True False True 10
```

- **`@cached_property`**: özellik ilk okunuşta hesaplanır ve nesnede saklanır;
  `r.total` iki kez okundu, hesap bir kez yapıldı.
- **`@total_ordering`**: `__eq__` ve `__lt__` yazmak yeter; `<=`, `>`, `>=`
  kendiliğinden gelir. `max` ve `sorted` da artık çalışır. `1.2 < 1.10`
  sürüm sırasında doğru: demet karşılaştırması `2 < 10`.

## singledispatch: türe göre davranmak

```python
from functools import singledispatch


@singledispatch
def describe(value):
    return f"something: {value!r}"


@describe.register
def _(value: int):
    return f"integer {value}"


@describe.register
def _(value: list):
    return f"list of {len(value)}"


print(describe(5))
print(describe([1, 2]))
print(describe("hi"))
print(describe(True))
```

```text
integer 5
list of 2
something: 'hi'
integer True
```

**`@singledispatch`** aynı adlı fonksiyonun ilk argümanın **türüne** göre
farklı sürümünü çalıştırır; tür belirtimiyle (`value: int`) kayıt yapılır.
Uzun bir `if isinstance(...)` zinciri yerine her tür ayrı bir fonksiyonda
durur. `True` "integer" çıktı: `bool`, `int`'in alt türüdür.

## Sık hatalar

```python
from functools import lru_cache


@lru_cache(maxsize=None)
def total(items):
    return sum(items)


try:
    total([1, 2])
except TypeError as error:
    print("TypeError:", error)
print(total((1, 2)))


@lru_cache(maxsize=2)
def square(n):
    return n * n


for n in [1, 2, 3, 1]:
    square(n)
print(square.cache_info())
```

```text
TypeError: unhashable type: 'list'
3
CacheInfo(hits=0, misses=4, maxsize=2, currsize=2)
```

- Önbellek argümanları sözlük anahtarı olarak saklar; **liste gibi
  değiştirilebilir argüman** kabul etmez. Demet kullan.
- `maxsize=2` ile 3 gelince 1 atıldı; sonraki `square(1)` yeniden hesaplandı
  (4 kaçırma, 0 isabet). Önbellek boyutu küçükse kazanç kaybolur.
- `maxsize=None` sınırsızdır: milyonlarca farklı argümanla çağrılan bir
  fonksiyonun önbelleği **belleği doldurur**. Bu, bu modülün bellek
  sızıntısı bölümündeki örneklerden biri.

## Özet

- `@lru_cache(maxsize=...)`: aynı girdiye aynı sonucu veren fonksiyonun
  sonuçlarını sakla; `cache_info()`, `cache_clear()`.
- Dekoratör = fonksiyonu saran fonksiyon; kendininkinde `@wraps(func)`.
- `partial` argümanları sabitler, `reduce` diziyi tek değere indirir,
  `operator` işleçlerin fonksiyon hâli.
- `@cached_property`, `@total_ordering`, `@singledispatch`.
