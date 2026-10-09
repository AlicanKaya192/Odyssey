# typing

In the Python path's Type Hints section you saw the basics: `age: int`,
`list[str]`, `str | None`, `-> None`. This section covers the advanced forms
growing projects need: types that accept only certain values (`Literal`),
type aliases, functions that take functions (`Callable`), dictionaries with
known keys (`TypedDict`), generic functions that work with any type
(generics), and what a hint does and does not do at run time.

## A hint does not change how code runs

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

`area("ab", 2)` raised no error and returned `"abab"`: **Python does not
check hints**. Hints are stored in the function's `__annotations__`
dictionary (`get_type_hints` gives the same information resolved); the ones
that read them are the **editor** and **type checkers** (mypy, Pyright;
Pylance in VS Code uses Pyright). Before the code runs, while you type, they
underline the `area("ab", 2)` line. Some libraries (FastAPI, Pydantic) also
read hints and validate incoming data; you saw that in the Writing APIs
module.

## Literal and Final

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

- **`Literal["r", "w", "a"]`** means "only one of these values". More precise
  than `str`: the editor marks `"x"` as wrong. At run time nobody stopped it
  again; you can read the values with `get_args` and check them yourself.
- **`type Mode = ...`** (Python 3.12+) defines a **type alias**: a short name
  for a long type. The actual type is in `Mode.__value__`.
- **`Final`** means "this name will not be reassigned"; a checker reports a
  `MAX_SIZE = 5` line as an error.

## Callable: functions that take functions

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

**`Callable[[int], int]`** means "a function that takes an `int` and returns
an `int`": inside the square brackets, first the list of argument types,
then the return type. The `key` you give `sorted`, the function you give
`map`, a handler bound to a button are all `Callable`s. `Callable` comes from
`collections.abc`.

## TypedDict and NamedTuple

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

- **`TypedDict`** describes **which keys of which types** a dictionary
  carries; ideal for describing data from JSON. At run time it is an
  ordinary `dict` (`type(m)` → `dict`). **`NotRequired`** is a key that may
  be missing.
- **`NamedTuple`** is `namedtuple` written in class form: the fields' types
  and defaults (`y = 0.0`) in one place.

## Generic functions and classes (generics)

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

`first[T]` says "works with any type, but the input and output types are
**the same**": given `list[int]` it returns `int`, given `list[str]` it
returns `str`. `T` is a **type variable**. Writing `list[Any] -> Any` would
work too, but the checker would forget what the returned value is. `Box[T]`
is the class form of the same idea. This square-bracket syntax came with
Python 3.12; in older code you will see `T = TypeVar("T")`.

## Checking at run time

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

- `isinstance` does not accept a type with square brackets (`list[int]`):
  you have to walk through the list's contents one by one.
- If a value from outside (a user, a file, an API) really needs checking,
  write it yourself with `isinstance`. Do not forget that `bool` is a subtype
  of `int`: `True` was rejected separately.
- `object` means "could be anything, I must look first"; **`Any`** means "do
  not check". For an unknown type write `object` instead of `Any`: the
  checker pushes you to `isinstance`.

## Summary

- Hints do not change how code runs; editors and type checkers read them
  (`__annotations__`, `get_type_hints`).
- `Literal[...]` for specific values, `Final` is not reassigned, `type Name =
  ...` is an alias.
- `Callable[[arguments], return]` is a function type.
- `TypedDict` is a dictionary schema (`NotRequired`), `NamedTuple` a typed
  record.
- Generics: `def f[T](x: list[T]) -> T`, `class Box[T]`.
- Real checks with `isinstance`; for the unknown, `object`, not `Any`.
