# copy, pprint and enum

This section has three small modules that are useful in every project.
**`copy`**: controlling whether the inner parts are **shared** when copying a
nested structure (like a dictionary holding lists). **`pprint`**: printing
large nested data readably. **`enum`**: keeping fixed options like `"paid"`
and `"shipped"` as named values instead of strings open to typos.

## Assignment, shallow copy, deep copy

```python
import copy

original = {"name": "Ada", "tags": ["math", "code"]}
alias = original
shallow = copy.copy(original)
deep = copy.deepcopy(original)
original["name"] = "Grace"
original["tags"].append("ships")
print(alias["name"], shallow["name"], deep["name"])
print(shallow["tags"], deep["tags"])
print(alias is original, shallow is original, shallow["tags"] is original["tags"])
```

```text
Grace Ada Ada
['math', 'code', 'ships'] ['math', 'code']
True False True
```

- **Assignment** (`alias = original`) is not a copy: both names point to the
  **same** dictionary. A change through one shows in the other (`Grace`).
- A **shallow copy** (`copy.copy`, `dict(d)`, `list(x)`, `x[:]`, `d.copy()`)
  rebuilds the outer container but **shares the inner objects**: the name
  change did not reach the copy (`Ada`), but `ships`, appended to the inner
  list, shows in the shallow copy too. Their `tags` are the same list (`is` →
  `True`).
- A **deep copy** (`copy.deepcopy`) rebuilds everything nested: no change
  reached it.

If a function will change the nested data it receives and the caller's data
must not be spoiled, `deepcopy` is needed. A deep copy is slow on large data
and takes memory; use it when nested changes really happen.

## A common mistake: [[0] * 3] * 3

```python
grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)
grid = [[0] * 3 for _ in range(3)]
grid[0][0] = 1
print(grid)
```

```text
[[1, 0, 0], [1, 0, 0], [1, 0, 0]]
[[1, 0, 0], [0, 0, 0], [0, 0, 0]]
```

Multiplying a list with `* 3` does **not copy** the inner list; it points to
the same list three times: changing one cell changed all three rows. A
comprehension that builds a **new** list for every row gives the right
result. This is a hidden form of the shallow copy.

## pprint: printing readably

```python
from pprint import pformat, pprint

data = {"version": "1.0.0", "name": "Odyssey",
        "tracks": [{"id": "python", "sections": 19, "tags": ["basics", "oop"]},
                   {"id": "sql", "sections": 20, "tags": ["joins"]}]}
print(len(repr(data)))
pprint(data, width=60)
pprint(data, depth=1)
pprint(data, depth=1, sort_dicts=False)
print(repr(pformat([1, 2, 3])))
```

```text
162
{'name': 'Odyssey',
 'tracks': [{'id': 'python',
             'sections': 19,
             'tags': ['basics', 'oop']},
            {'id': 'sql',
             'sections': 20,
             'tags': ['joins']}],
 'version': '1.0.0'}
{'name': 'Odyssey', 'tracks': [...], 'version': '1.0.0'}
{'version': '1.0.0', 'name': 'Odyssey', 'tracks': [...]}
'[1, 2, 3]'
```

- A plain `print(data)` dumps the whole structure on one line: here a line of
  162 characters, unreadable.
- **`pprint`** (pretty print) splits it into lines and aligns the nested
  levels; `width` is the line width.
- **`depth=1`** shows only the first level and turns deeper ones into
  `[...]`: for a quick look at what a big JSON response contains.
- `pprint` **sorts dictionary keys by default**; to see the original order,
  `sort_dicts=False`.
- **`pformat`** returns the same text without printing it (for writing to a
  log file).

## enum: named constants

```python
from enum import Enum


class Status(Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"


order = Status.PAID
print(order, order.name, order.value)
print(Status("shipped"), Status["PENDING"])
print(order == Status.PAID, order == "paid")
print([s.name for s in Status])
try:
    Status("lost")
except ValueError as error:
    print("ValueError:", error)
```

```text
Status.PAID PAID paid
Status.SHIPPED Status.PENDING
True False
['PENDING', 'PAID', 'SHIPPED']
ValueError: 'lost' is not a valid Status
```

- An **`Enum`** class lists the **fixed options** something can take: an
  order status, a user role, a colour.
- Every member has a `name` (`PAID`) and a `value` (`"paid"`). From a value
  coming from outside to a member: `Status("shipped")`; from a name:
  `Status["PENDING"]`.
- A member is **not equal** to plain text (`order == "paid"` → `False`):
  comparisons are always made with members.
- The class can be iterated; an invalid value raises `ValueError`. Validating
  a status from a file or an API happens by itself.

## IntEnum and Flag

```python
from enum import Flag, IntEnum, auto


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


print(Priority.HIGH > Priority.LOW, Priority.MEDIUM + 1)
print(sorted([Priority.HIGH, Priority.LOW, Priority.MEDIUM]))


class Perm(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()


p = Perm.READ | Perm.WRITE
print(p, Perm.WRITE in p, Perm.EXECUTE in p)
print(Perm.READ.value, Perm.WRITE.value, Perm.EXECUTE.value)
```

```text
True 3
[<Priority.LOW: 1>, <Priority.MEDIUM: 2>, <Priority.HIGH: 3>]
Perm.READ|WRITE True False
1 2 4
```

- **`IntEnum`** members are integers too: they are compared by size, sorted
  and used in arithmetic. For ordered options like priority or level.
- **`Flag`** is for options that can be combined: a file permission can be
  both read and write. Combined with `|`, asked with `in`.
- **`auto()`** gives the value itself; in a `Flag` 1, 2, 4... (each a separate
  bit), so combinations do not clash.

## Summary

- Assignment is not a copy; `copy.copy` is shallow (the inside is shared),
  `copy.deepcopy` deep.
- `[[0] * 3] * 3` points to the same list three times; use a comprehension.
- `pprint(data, width=, depth=, sort_dicts=)`, `pformat`.
- `Enum`: `name`, `value`, `Status("value")`, `Status["NAME"]`; not equal to
  text.
- `IntEnum` can be sorted, `Flag` combines with `|`; `auto()`.
