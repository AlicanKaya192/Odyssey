## abc

```python
from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def run(self) -> str:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...
```

| Yazım | Ne yapar |
|---|---|
| `class Base(ABC)` | soyut temel sınıf |
| `@abstractmethod` | alt sınıf yazmak zorunda |
| `@property` + `@abstractmethod` | soyut özellik |
| `Base.__abstractmethods__` | doldurulacaklar |
| `__init_subclass__` | alt sınıf tanımlanınca çalışır |

## collections.abc

| Sınıf | Yazman gereken | Bedava gelen |
|---|---|---|
| `Iterable` | `__iter__` | `for` |
| `Sized` | `__len__` | `len()` |
| `Container` | `__contains__` | `in` |
| `Sequence` | `__getitem__`, `__len__` | `in`, `for`, `reversed`, `index`, `count` |
| `Mapping` | `__getitem__`, `__iter__`, `__len__` | `get`, `keys`, `items`, `values`, `in` |
| `MutableSequence` | + `__setitem__`, `__delitem__`, `insert` | `append`, `extend`, `pop`, `remove` |

## typing.Protocol

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Runner(Protocol):
    def run(self) -> str:
        ...
```

- Uymak için türemek gerekmez; aynı metotları taşımak yeter.
- `isinstance(x, Runner)` yalnızca `@runtime_checkable` ile ve yalnızca adlara
  bakarak.
- Asıl denetimi tip denetleyicisi yapar.
