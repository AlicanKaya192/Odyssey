A list of the annotations you will run into. Not to memorise — to look up when
you get stuck.

## Basic types

| Annotation | Meaning | Example value |
|---|---|---|
| `str` | Text | `"Ada"` |
| `int` | Whole number | `42` |
| `float` | Decimal number | `3.14` |
| `bool` | True / false | `True` |
| `bytes` | Raw bytes | `b"abc"` |
| `None` | No value | `None` |

A `float` may be passed where `int` is written; the other direction is usually
not intended. In Python `True` also counts as `1`, but in annotations `bool`
and `int` are kept apart.

## Containers

You write what is inside the container in square brackets.

| Annotation | Meaning |
|---|---|
| `list[str]` | A list of strings |
| `dict[str, int]` | A dictionary with string keys and number values |
| `set[str]` | A set of strings |
| `tuple[int, int]` | A tuple of **exactly two** whole numbers |
| `tuple[int, ...]` | A tuple of unknown length, all numbers |

There is a subtlety with tuples: `tuple[int, str]` means "the first element is
a number, the second is a string" — position matters. With `list[int]` the
type applies to every element.

## More than one possibility

| Annotation | Meaning |
|---|---|
| `int \| None` | Either a whole number or nothing |
| `int \| str` | Either a whole number or a string |
| `list[int \| str]` | A list whose elements are numbers or strings |

The form you will see most is `X | None`. When a function says "I return it if
I find it, nothing if I do not", its return type is written like this.

## Nested containers

You can put a container inside a container. They get long, but the rule does
not change:

| Annotation | Meaning |
|---|---|
| `list[list[int]]` | A list of lists of numbers |
| `dict[str, list[int]]` | Each key holds a list of numbers |
| `list[dict[str, str]]` | A list of dictionaries |
| `dict[str, dict[str, int]]` | A dictionary inside a dictionary |

The third one comes up constantly in data work: each row of a CSV file is a
dictionary, and the whole file is a list of those dictionaries.

## A function itself

A function can take another function as a parameter. In that case:

```python
from typing import Callable

def apply_twice(func: Callable[[int], int], value: int) -> int:
    return func(func(value))
```

`Callable[[int], int]` means "a function that takes a whole number and returns
a whole number". The first pair of brackets holds the parameters, the second
holds the return type.

Recognising it is enough for now; you will rarely need to write one.

## The escape hatch: `Any`

```python
from typing import Any

def dump(value: Any) -> str:
    return str(value)
```

`Any` means "this could be anything". It is easy to write, but it erases the
entire benefit of annotating — your editor can no longer tell you anything.

Do not use it unless you really are writing something that accepts every type.
Writing `Any` is not far from writing no annotation at all.

## The older equivalents

Before Python 3.9, containers came from the `typing` module. The form you will
see in older code is on the left:

| Old | New |
|---|---|
| `List[str]` | `list[str]` |
| `Dict[str, int]` | `dict[str, int]` |
| `Set[str]` | `set[str]` |
| `Tuple[int, int]` | `tuple[int, int]` |
| `Optional[str]` | `str \| None` |
| `Union[int, str]` | `int \| str` |

Use the right-hand one when writing new code. Being able to read the left-hand
one is enough.
