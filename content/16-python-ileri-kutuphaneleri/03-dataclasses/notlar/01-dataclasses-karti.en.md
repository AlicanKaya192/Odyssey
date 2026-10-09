## Definition

```python
from dataclasses import dataclass, field


@dataclass
class Product:
    name: str
    price: float
    tags: list[str] = field(default_factory=list)
    stock: int = 0

    def total(self) -> float:
        return self.price * self.stock
```

## @dataclass options

| Option | What it does |
|---|---|
| `frozen=True` | immutable, hashable (set, dictionary key) |
| `order=True` | `<`, `>`, `sorted`, `max` (in field order) |
| `slots=True` | only the defined fields, less memory |
| `kw_only=True` | fields by name only |
| `eq=False` | do not produce `__eq__` (compare by identity) |

## field

| Code | What it does |
|---|---|
| `field(default_factory=list)` | a new list for each object |
| `field(init=False)` | not asked for in `__init__` |
| `field(repr=False)` | hidden when printed (like a password) |
| `field(compare=False)` | left out of comparisons |

## Helpers

| Code | What it gives |
|---|---|
| `asdict(obj)` | a dictionary (nested too) |
| `astuple(obj)` | a tuple |
| `replace(obj, field=value)` | a new object with a change |
| `fields(Class)` | field information |
| `Class(**dictionary)` | an object from a dictionary |

## Remember

- Fields with defaults come after those without.
- No `= []`; `field(default_factory=list)`.
- `__post_init__` for validation.
- `dataclass` does not check types.
