## The problem with magic strings

Code that keeps statuses as plain text swallows a typo **silently**:

```python
import json
from enum import Enum


class Status(Enum):
    PAID = "paid"
    SHIPPED = "shipped"


def is_done(status):
    return status == "shiped"


print(is_done("shipped"))
try:
    print(Status.SHIPED)
except AttributeError as error:
    print("AttributeError:", error)
try:
    json.dumps({"status": Status.SHIPPED})
except TypeError as error:
    print("TypeError:", error)
record = json.dumps({"order": 7, "status": Status.SHIPPED.value})
print(record)
print(Status(json.loads(record)["status"]) is Status.SHIPPED)
```

```text
False
AttributeError: type object 'Status' has no attribute 'SHIPED'
TypeError: Object of type Status is not JSON serializable
{"order": 7, "status": "shipped"}
True
```

- The typo `"shiped"` raised no error; the function always returns `False`,
  and that is only noticed when an order looks "not done".
- The same mistake with an enum raised `AttributeError` **at once**: the
  misspelt member does not exist. Editors suggest the members too (a list
  opens when you type `Status.`).
- **When writing JSON**, write the member's `value`, not the member itself;
  the member cannot be written directly (`TypeError`). When reading, turn it
  back into a member with `Status(value)`.

## When an enum?

| Situation | Choice |
|---|---|
| A few fixed, known options (status, role, colour) | `Enum` |
| Ordered options (priority, level) | `IntEnum` |
| Options that combine (permissions) | `Flag` |
| Options keep changing, users add them | a database / file |
| A single constant (`MAX_SIZE = 100`) | a plain variable |

## Iterating and mapping an enum

```python
from enum import Enum


class Color(Enum):
    RED = "red"
    GREEN = "green"


LABELS = {Color.RED: "Red", Color.GREEN: "Green"}
for color in Color:
    print(color.value, LABELS[color])
```

Members can be dictionary keys: each option's on-screen name, colour or icon
is kept in a dictionary. If a new member is added and someone forgets to add
it to the dictionary, a `KeyError` reminds them at once.
