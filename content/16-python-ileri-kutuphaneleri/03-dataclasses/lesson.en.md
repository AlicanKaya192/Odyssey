# dataclasses

In the Python path's OOP section you wrote classes: in `__init__` you
assigned every field one by one, `self.x = x`. Most classes actually **carry
data**: a product, a user, a coordinate. For these classes you have to write
the same `__init__` every time, a `__repr__` so it looks readable when
printed, and an `__eq__` for comparisons. **`dataclasses`** produces these
from the list of fields by itself.

## @dataclass

```python
from dataclasses import dataclass


class PlainPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


print("object at" in repr(PlainPoint(1, 2)), PlainPoint(1, 2) == PlainPoint(1, 2))


@dataclass
class Point:
    x: float
    y: float


p = Point(1, 2)
print(p, p == Point(1, 2), p.x + p.y)
```

```text
True False
Point(x=1, y=2) True 3
```

- The plain class prints as `<... object at 0x...>` (it says nothing), and
  two objects with the same values are **not equal** (`==` looks at
  identity).
- **`@dataclass`** read the class's type-hinted fields and wrote `__init__`,
  `__repr__` and `__eq__` itself: `Point(x=1, y=2)` is readable, and equal
  values are equal.
- Fields are written with type hints; the hint is not checked here either
  (`Point(1, 2)` was built with integers).

## Defaults and field

```python
from dataclasses import dataclass, field


@dataclass
class Cart:
    owner: str
    items: list[str] = field(default_factory=list)
    discount: float = 0.0


a = Cart("ada")
b = Cart("alan", discount=0.1)
a.items.append("pen")
print(a)
print(b)
try:
    @dataclass
    class Bad:
        items: list = []
except ValueError as error:
    print("ValueError:", str(error).split(":")[0])
```

```text
Cart(owner='ada', items=['pen'], discount=0.0)
Cart(owner='alan', items=[], discount=0.1)
ValueError: mutable default <class 'list'> for field items is not allowed
```

- Fields with a default are written **after** those without one.
- A **mutable** default like a list or a dictionary cannot be written as
  `= []`: every object would share the same list. `dataclass` does not allow
  it (`ValueError`) and the rest of the message gives the fix:
  **`field(default_factory=list)`** builds a new list for each object. The
  `pen` added to `a` did not reach `b`.

## frozen and order

```python
from dataclasses import FrozenInstanceError, dataclass


@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int = 0


v = Version(1, 2)
try:
    v.major = 3
except FrozenInstanceError as error:
    print("FrozenInstanceError:", error)
versions = sorted([Version(1, 10), Version(1, 2), Version(0, 9)])
print([f"{x.major}.{x.minor}" for x in versions])
print(len({v, Version(1, 2), Version(2)}), Version(2) > v)
```

```text
FrozenInstanceError: cannot assign to field 'major'
['0.9', '1.2', '1.10']
2 True
```

- **`frozen=True`** makes the object immutable: a field cannot be assigned.
  An immutable object can be **a set element and a dictionary key** (it has
  a hash): two of the three versions were the same, two stayed in the set.
- **`order=True`** produces `<`, `>` comparisons in field order (first
  `major`, then `minor`); `sorted` and `max` work. The order the fields are
  written in is the comparison order.

## Validation, asdict and replace

```python
from dataclasses import asdict, dataclass, field, replace


@dataclass
class Rect:
    width: float
    height: float
    area: float = field(init=False)

    def __post_init__(self):
        if self.width < 0 or self.height < 0:
            raise ValueError("negative size")
        self.area = self.width * self.height


r = Rect(3, 4)
print(r, asdict(r))
print(replace(r, width=10))
try:
    Rect(-1, 2)
except ValueError as error:
    print("ValueError:", error)
```

```text
Rect(width=3, height=4, area=12) {'width': 3, 'height': 4, 'area': 12}
Rect(width=10, height=4, area=40)
ValueError: negative size
```

- **`__post_init__`** runs right after the generated `__init__`: for
  **validation** and computed fields.
- **`field(init=False)`**: the field is not asked for in `__init__`;
  `__post_init__` fills it.
- **`asdict`** turns the object into a dictionary (before writing JSON);
  **`replace`** produces a **new** object with one field changed (this is how
  `frozen` objects are changed). The new object went through `__post_init__`
  again: the area became 40.

## slots and kw_only

```python
from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class User:
    name: str
    admin: bool = False


u = User(name="ada")
print(u)
try:
    User("ada")
except TypeError as error:
    print("TypeError:", error)
try:
    u.email = "ada@example.com"
except AttributeError as error:
    print(type(error).__name__)
```

```text
User(name='ada', admin=False)
TypeError: User.__init__() takes 1 positional argument but 2 were given
AttributeError
```

- **`kw_only=True`**: fields can only be given by name (`User(name="ada")`).
  In records with many fields it prevents mixing up the order.
- **`slots=True`**: the object carries only the defined fields. A misspelt
  name (`u.emial = ...`) raises an error instead of silently opening a new
  field; the object also uses less memory.

## To JSON and back

```python
import json
from dataclasses import asdict, dataclass


@dataclass
class User:
    name: str
    age: int
    tags: list[str]


users = [User("ada", 36, ["math"]), User("alan", 41, [])]
text = json.dumps([asdict(u) for u in users])
print(json.dumps(asdict(users[0])))
loaded = [User(**d) for d in json.loads(text)]
print(loaded == users, loaded[1])
```

```text
{"name": "ada", "age": 36, "tags": ["math"]}
True User(name='alan', age=41, tags=[])
```

When writing, `asdict`; when reading, `User(**dictionary)`: `**` passes the
dictionary's keys as named arguments. If the incoming JSON has extra or
missing keys, a `TypeError` follows; with data from outside, that needs to be
caught.

## Summary

- `@dataclass`: `__init__`, `__repr__`, `__eq__` from the fields.
- A mutable default is `field(default_factory=list)`.
- `frozen=True` is immutable and hashable, `order=True` sortable.
- `__post_init__` for validation and computed fields; `field(init=False)`.
- `asdict` to a dictionary, `replace` a changed copy, `Class(**d)` back.
- `slots=True` catches a wrong name, `kw_only=True` requires names.
