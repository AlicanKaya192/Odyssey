Everything from week 1 on one page.

## Comparison operators

They all give `True` or `False` (`bool`).

| Operator | Meaning | For `x = 3` |
|---|---|---|
| `x < 5` / `x > 5` | less / greater | `True` / `False` |
| `x <= 3` / `x >= 4` | less or equal / greater or equal | `True` / `False` |
| `x == 3` | equal | `True` |
| `x != 3` | not equal | `False` |
| `1 < x < 5` | chained: `1 < x and x < 5` | `True` |

## Logical operators

| Operator | `True` when | Example |
|---|---|---|
| `a and b` | both are true | `True and False` → `False` |
| `a or b` | either is true | `True or False` → `True` |
| `not a` | `a` is false | `not True` → `False` |

Both sides of `or` must be full conditions: `name == "Harry" or name == "Ron"`.

## if / elif / else

```python
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("F")
```

- A `:` after the condition, the block indented (4 spaces).
- The questions are asked in order; the block of **the first true** one runs,
  the rest are skipped.
- Any number of `elif`; at most one `else`, last, with no condition.

## Modulo

| Code | Result |
|---|---|
| `10 % 3` | `1` (the remainder) |
| `n % 2 == 0` | `True` when `n` is even |

## Functions returning a bool

| Code | When |
|---|---|
| `if ...: return True` / `else: return False` | the long form |
| `return True if n % 2 == 0 else False` | conditional expression |
| `return n % 2 == 0` | the shortest: a comparison is already a `bool` |

In general the conditional expression is `A if condition else B`: `A` when the
condition is true, otherwise `B`.

## match

```python
match name:
    case "Harry" | "Hermione" | "Ron":
        print("Gryffindor")
    case "Draco":
        print("Slytherin")
    case _:
        print("Who?")
```

- The value is compared with each `case` in turn; the first match runs.
- `|` joins several values in one case.
- `case _:` matches anything (like `else`); it goes last.

## String methods useful for the problem set

| Method | Result |
|---|---|
| `"hello, world".startswith("hello")` | `True` |
| `"cat.gif".endswith(".gif")` | `True` |
| `"1 + 1".split(" ")` | `['1', '+', '1']` |
| `x, y, z = "1 + 1".split(" ")` | unpacks the three parts into three variables |
| `"7:30".split(":")` | `['7', '30']` |
