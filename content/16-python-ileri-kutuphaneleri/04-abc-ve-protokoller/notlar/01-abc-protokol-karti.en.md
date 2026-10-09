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

| Code | What it does |
|---|---|
| `class Base(ABC)` | an abstract base class |
| `@abstractmethod` | subclasses must write it |
| `@property` + `@abstractmethod` | an abstract property |
| `Base.__abstractmethods__` | what must be filled in |
| `__init_subclass__` | runs when a subclass is defined |

## collections.abc

| Class | You must write | You get for free |
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

- No need to derive to fit; carrying the same methods is enough.
- `isinstance(x, Runner)` only with `@runtime_checkable`, and only by
  looking at names.
- The real check is done by the type checker.
