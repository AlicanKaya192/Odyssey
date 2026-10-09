## Copying

| Code | Outer container | Inner objects |
|---|---|---|
| `b = a` | the same | the same |
| `copy.copy(a)`, `a.copy()`, `list(a)`, `a[:]` | new | **shared** |
| `copy.deepcopy(a)` | new | new |

- `x is y`: is it the same object? `x == y`: are the values equal?
- `[[0] * 3] * 3` points to the same list three times; `[[0] * 3 for _ in range(3)]`.
- Immutable objects like tuples and strings have no copying problem.

## pprint

| Code | What it does |
|---|---|
| `pprint(data)` | prints split into lines |
| `pprint(data, width=60)` | the line width |
| `pprint(data, depth=1)` | only the first level, the rest `...` |
| `pprint(data, sort_dicts=False)` | do not sort the keys |
| `pformat(data)` | returns the same text |

## enum

| Code | What it gives |
|---|---|
| `class Status(Enum): PAID = "paid"` | the definition |
| `Status.PAID.name` / `.value` | `"PAID"` / `"paid"` |
| `Status("paid")` | a member from a value |
| `Status["PAID"]` | a member from a name |
| `list(Status)` | all members |
| `IntEnum` | like integers, can be sorted |
| `Flag` + `auto()` | options combining with <code>&#124;</code> |

- A member is not equal to plain text; write the `value` to JSON.
- An invalid value raises `ValueError`, a wrong name `AttributeError`.
