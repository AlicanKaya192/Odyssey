# abc and Protocols

In Python what an object **can do** matters more than what it is: if it has
a `speak()` method it can speak, if it has `__len__` and `__getitem__` it can
be used like a sequence ("if it walks like a duck and quacks like a duck, it
is a duck", duck typing). In a growing project this contract needs to be
**written down**: "every exporter must have an `export` method". There are
two tools: the **abstract base class** (`abc`) and the **protocol**
(`typing.Protocol`).

## Abstract base classes: ABC and abstractmethod

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

- A class deriving from **`ABC`** with a method marked **`@abstractmethod`**
  is **abstract**: no object can be built from it.
- A subclass stays abstract until it writes all the abstract methods.
  `BrokenExporter` wrote the method under the wrong name (`write`) and got
  an error **when the object was built**; the broken contract was caught
  before use.
- An abstract class can carry **shared code** too: `save` uses the `export`
  the subclass writes. Every new format (JSON, Excel) writes only `export`
  and gets saving for free.

## collections.abc: ready-made contracts

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

**`collections.abc`** defines the contracts of the built-in types:
**`Iterable`** can be walked, **`Sequence`** is ordered and indexable (list,
tuple, string, `range`), **`Mapping`** is key-value (dictionary). A set is
iterable but not ordered; a number is none of them. "Does this function want
a list, or anything iterable?" is answered with these in type hints too
(`Iterable[int]`).

## Free methods from a contract

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

The class deriving from `Sequence` wrote only `__len__` and `__getitem__`;
iteration, `in`, `reversed`, `index` and `count` came ready. Abstract base
classes say both "you must write these" and "if you write them, these are
free".

## Protocol: a contract without inheritance

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

- A **`Protocol`** says "anything with these methods"; classes **do not need
  to derive** from it. `Dog` and `Robot` never mentioned `Speaker`, yet both
  fit (`Speaker in Dog.__mro__` → `False`).
- A type checker catches `chorus([Rock()])`: `Rock` has no `speak`.
- With **`@runtime_checkable`**, `isinstance` works too; but it only checks
  that the **names** exist (there is a trap below).

A protocol suits classes outside your own code (another library's objects):
you cannot make them derive from your base class, but you can use them if
they fit the protocol.

## An abstract property and shared behaviour

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

`@property` together with `@abstractmethod`: each shape computes `area`
itself, `describe` is shared by all. `__abstractmethods__` lists what
subclasses must fill in.

## A trap: runtime_checkable only looks at names

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

`Fake` has a **string** called `close`; `isinstance` checked that the name
exists and said `True`, and calling it failed. A run-time protocol check is a
rough filter; the real check is done by the type checker.

## ABC or Protocol?

| | `ABC` | `Protocol` |
|---|---|---|
| To fit | you must derive from it | no need to derive |
| A missing method | `TypeError` when the object is built | the type checker warns |
| Carries shared code | yes (`save`, `describe`) | usually not |
| Fits when | you build your own family of classes | you accept other people's objects |

## Summary

- `class X(ABC)` + `@abstractmethod`: no object until a subclass writes it.
- An abstract class carries shared code; the subclass writes only the
  abstract part.
- `collections.abc`: `Iterable`, `Sequence`, `Mapping`...; deriving from
  `Sequence` gives `index`, `count`, `in` for free.
- `Protocol`: a structural contract without inheritance; `isinstance` with
  `@runtime_checkable` (it only looks at names).
