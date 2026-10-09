Python has at least five ways to make "a record with a few fields". Let us
build the same point with four of them:

```python
from collections import namedtuple
from dataclasses import dataclass
from typing import TypedDict

PointT = namedtuple("PointT", "x y")


@dataclass
class PointD:
    x: int
    y: int


class PointTD(TypedDict):
    x: int
    y: int


for p in [{"x": 1, "y": 2}, PointT(1, 2), PointD(1, 2), PointTD(x=1, y=2)]:
    print(type(p).__name__, p)
```

```text
dict {'x': 1, 'y': 2}
PointT PointT(x=1, y=2)
PointD PointD(x=1, y=2)
dict {'x': 1, 'y': 2}
```

A `TypedDict` is a plain dictionary at run time; the difference exists only
in the eyes of the editor and the type checker.

## Which one when?

| Structure | Mutable | Field access | Best for |
|---|---|---|---|
| `dict` | yes | `p["x"]` | short-lived data of unclear shape |
| `TypedDict` | yes | `p["x"]` | a schema for a dictionary from outside, like JSON |
| `namedtuple` / `NamedTuple` | no | `p.x`, `p[0]` | a small, unchanging record; instead of a tuple |
| `@dataclass` | yes (no with `frozen`) | `p.x` | a record with methods, defaults, validation |
| Pydantic `BaseModel` | yes | `p.x` | **validating** data from outside (APIs) |

A short rule:

- If a function returns two or three values, `NamedTuple`.
- For the program's own objects (a product, an order, settings),
  `@dataclass`.
- If you carry JSON as it is, `TypedDict`.
- If the types of incoming data really must be checked, Pydantic (you saw it
  in the Writing APIs module); `dataclass` does not check types.
