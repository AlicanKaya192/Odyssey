All the ready-made rules in one table, with the `type` names from the `422`
answer.

## Numbers

| Rule | Meaning | `type` when broken |
|---|---|---|
| `gt=0` | greater than 0 | `greater_than` |
| `ge=1` | 1 or more | `greater_than_equal` |
| `lt=100` | less than 100 | `less_than` |
| `le=5` | 5 or less | `less_than_equal` |
| `multiple_of=0.5` | a multiple of 0.5 | `multiple_of` |

A price with `Field(gt=0, multiple_of=0.5)` given `1.25` → `422` multiple_of
(we measured).

## Strings

| Rule | Meaning | `type` when broken |
|---|---|---|
| `min_length=1` | at least 1 character | `string_too_short` |
| `max_length=100` | at most 100 characters | `string_too_long` |
| `pattern=r"..."` | must match the regular expression | `string_pattern_mismatch` |

## Lists

`Field(max_length=3)` on a **list** limits the number of items: a field
`tags: list[str] = Field(default=[], max_length=3)` given four tags →
`422` too_long, message `List should have at most 3 items after
validation, not 4`.

## Common patterns (`pattern`)

| Pattern | What it wants | Example |
|---|---|---|
| `^[0-9]{13}$` | exactly 13 digits | `9780441013593` |
| `^[a-z0-9_]+$` | lowercase letters, digits, underscore | `ada_99` |
| `^[A-Z]{2}$` | two capital letters | `TR` |
| `^\d{4}-\d{2}-\d{2}$` | a date format | `2026-10-07` |

`^` anchors the start and `$` the end: without them the pattern only has to
appear **somewhere** in the text (`"abc9780441013593xyz"` matches too).
Always write the pattern as `r"..."`; that way a backslash (`\d`) isn't
mangled.

## What goes where?

| Place | How |
|---|---|
| Body (model field) | `year: int = Field(ge=1450)` |
| Query | `limit: Annotated[int, Query(ge=1)] = 10` |
| Path | `book_id: Annotated[int, Path(gt=0)]` |

The rule names are the same in all three.
