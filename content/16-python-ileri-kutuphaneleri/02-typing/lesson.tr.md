# typing

Python patikasının Tip Belirtimleri bölümünde temelini gördün: `age: int`,
`list[str]`, `str | None`, `-> None`. Bu bölüm büyüyen projelerde gereken
ileri biçimleri anlatıyor: yalnızca belirli değerleri kabul eden türler
(`Literal`), tür takma adları, fonksiyon alan fonksiyonlar (`Callable`),
anahtarları belli sözlükler (`TypedDict`), her türle çalışan genel
fonksiyonlar (generics) ve belirtimin çalışma anında ne yaptığı, ne
yapmadığı.

## Belirtim çalışmayı değiştirmez

```python
from typing import get_type_hints


def area(width: float, height: float) -> float:
    return width * height


print(area(2, 3), area("ab", 2))
print(area.__annotations__)
print(get_type_hints(area))
```

```text
6 abab
{'width': <class 'float'>, 'height': <class 'float'>, 'return': <class 'float'>}
{'width': <class 'float'>, 'height': <class 'float'>, 'return': <class 'float'>}
```

`area("ab", 2)` hata vermedi, `"abab"` döndürdü: **Python belirtimleri
denetlemez**. Belirtimler fonksiyonun `__annotations__` sözlüğünde saklanır
(`get_type_hints` aynı bilgiyi çözerek verir); onları okuyan **editör** ve
**tip denetleyicileridir** (mypy, Pyright; VS Code'daki Pylance Pyright
kullanır). Kod çalışmadan önce, yazarken `area("ab", 2)` satırının altını
çizerler. Bir de bazı kütüphaneler (FastAPI, Pydantic) belirtimleri okuyup
gelen veriyi doğrular; API Yazmak modülünde bunu gördün.

## Literal ve Final

```python
from typing import Final, Literal, get_args

type Mode = Literal["r", "w", "a"]
MAX_SIZE: Final = 100


def open_log(path: str, mode: Mode = "r") -> str:
    return f"{path}:{mode}"


print(get_args(Mode.__value__))
print(open_log("app.log", "w"), open_log("app.log", "x"))
print(MAX_SIZE)
```

```text
('r', 'w', 'a')
app.log:w app.log:x
100
```

- **`Literal["r", "w", "a"]`** "yalnızca bu değerlerden biri" demek. `str`
  demekten daha kesin: editör `"x"`'i yanlış diye işaretler. Çalışma anında
  yine kimse durdurmadı; değerleri `get_args` ile okuyup kendin
  denetleyebilirsin.
- **`type Mode = ...`** (Python 3.12+) bir **tür takma adı** tanımlar: uzun
  bir türe kısa bir ad. Asıl tür `Mode.__value__`'da.
- **`Final`** "bu ad yeniden atanmayacak" demek; denetleyici `MAX_SIZE = 5`
  satırını hata sayar.

## Callable: fonksiyon alan fonksiyonlar

```python
from collections.abc import Callable

type Number = int | float
type Transform = Callable[[int], int]


def apply(func: Transform, values: list[int]) -> list[int]:
    return [func(v) for v in values]


def double(v: int) -> int:
    return v * 2


print(apply(double, [1, 2, 3]), apply(lambda v: v - 1, [5]))
print(Number.__value__, Transform.__value__)
```

```text
[2, 4, 6] [4]
int | float collections.abc.Callable[[int], int]
```

**`Callable[[int], int]`** "bir `int` alıp `int` döndüren fonksiyon" demek:
köşeli parantezin içinde önce argüman türlerinin listesi, sonra dönüş türü.
`sorted`'a verdiğin `key`, `map`'e verdiğin fonksiyon, bir düğmeye bağlanan
işlev hep birer `Callable`'dır. `Callable` `collections.abc`'den alınır.

## TypedDict ve NamedTuple

```python
from typing import NamedTuple, NotRequired, TypedDict


class Movie(TypedDict):
    title: str
    year: int
    rating: NotRequired[float]


m: Movie = {"title": "Up", "year": 2009}
print(m, type(m).__name__)
print(sorted(Movie.__required_keys__), sorted(Movie.__optional_keys__))


class Point(NamedTuple):
    x: float
    y: float = 0.0


p = Point(3.0)
print(p, p.x + p.y, p._fields)
```

```text
{'title': 'Up', 'year': 2009} dict
['title', 'year'] ['rating']
Point(x=3.0, y=0.0) 3.0 ('x', 'y')
```

- **`TypedDict`** bir sözlüğün **hangi anahtarları hangi türde** taşıdığını
  anlatır; JSON'dan gelen veriyi tarif etmek için idealdir. Çalışma anında
  sıradan bir `dict`'tir (`type(m)` → `dict`). **`NotRequired`** olmayabilen
  anahtar.
- **`NamedTuple`** sınıf biçimiyle yazılan `namedtuple`: alanların türü ve
  varsayılanı (`y = 0.0`) aynı yerde.

## Genel fonksiyonlar ve sınıflar (generics)

```python
def first[T](items: list[T]) -> T:
    return items[0]


class Box[T]:
    def __init__(self, item: T) -> None:
        self.item = item

    def get(self) -> T:
        return self.item


print(first([3, 1]), first(["a", "b"]), Box(42).get(), Box("hi").get())
print(first.__type_params__, Box.__type_params__)
```

```text
3 a 42 hi
(T,) (T,)
```

`first[T]` "her türle çalışır ama girdiyle çıktının türü **aynıdır**" der:
`list[int]` verilirse `int` döner, `list[str]` verilirse `str`. `T` bir **tür
değişkenidir**. `list[Any] -> Any` yazmak da çalışırdı, ama denetleyici
dönen değerin ne olduğunu unuturdu. `Box[T]` aynı fikrin sınıf hâli. Bu
köşeli parantezli yazım Python 3.12 ile geldi; eski kodda `T =
TypeVar("T")` görürsün.

## Çalışma anında denetlemek

```python
try:
    isinstance([1], list[int])
except TypeError as error:
    print("TypeError:", error)


def to_count(value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"expected int, got {type(value).__name__}")
    return value


print(to_count(3))
for bad in ["3", True]:
    try:
        to_count(bad)
    except TypeError as error:
        print("TypeError:", error)
```

```text
TypeError: isinstance() argument 2 cannot be a parameterized generic
3
TypeError: expected int, got str
TypeError: expected int, got bool
```

- `isinstance` köşeli parantezli türü (`list[int]`) kabul etmez: listenin
  içini tek tek gezmek gerekir.
- Dışarıdan (kullanıcı, dosya, API) gelen değeri gerçekten denetlemek
  gerekiyorsa `isinstance` ile kendin yaz. `bool`'un `int`'in alt türü olduğunu
  unutma: `True` ayrıca reddedildi.
- `object` "her şey olabilir, önce bakmam gerek" demek; **`Any`** ise
  "denetleme" demek. Bilmediğin bir türe `Any` yerine `object` yaz:
  denetleyici seni `isinstance`'a zorlar.

## Özet

- Belirtimler çalışmayı değiştirmez; editör ve tip denetleyicisi okur
  (`__annotations__`, `get_type_hints`).
- `Literal[...]` belirli değerler, `Final` yeniden atanmaz, `type Ad = ...`
  takma ad.
- `Callable[[argümanlar], dönüş]` fonksiyon türü.
- `TypedDict` sözlük şeması (`NotRequired`), `NamedTuple` türlü kayıt.
- Generics: `def f[T](x: list[T]) -> T`, `class Box[T]`.
- Gerçek denetim `isinstance` ile; bilinmeyene `Any` değil `object`.
