Everything from week 3 on one page.

## Kinds of error

| Error | When | Example |
|---|---|---|
| `SyntaxError` | the code cannot be read, no line runs | `print("hello)` |
| `ValueError` | the value is not suitable | `int("cat")`, `int("1.5")`, `int("")` |
| `NameError` | the name is not defined | printing an `x` that was never assigned |
| `ZeroDivisionError` | dividing by zero | `10 / 0` |
| `IndexError` | the list has no such position | `[1, 2][5]` |
| `KeyError` | the dict has no such key | `{"a": 1}["b"]` |
| `EOFError` | the input has ended (`Ctrl+D`, on Windows `Ctrl+Z` + Enter) | `input()` |

`int` accepts surrounding spaces and a minus sign: `int(" 42 ")` → `42`,
`int("-7")` → `-7`.

## try / except / else

```python
try:
    x = int(input("What's x? "))
except ValueError:
    print("x is not an integer")
else:
    print(f"x is {x}")
```

- `try`: attempt; only the fewest lines that could fail.
- `except Type:` runs if that type of error occurs; the rest of `try` is skipped.
- `else:` runs if no error occurred.
- Name the type; a bare `except:` swallows errors you did not expect.

## Several exceptions

| Code | What it does |
|---|---|
| `except ValueError:` + `except ZeroDivisionError:` | a separate answer for each type |
| `except (ValueError, ZeroDivisionError):` | the same answer for both |

## Asking again

```python
def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass
```

| Code | What it does |
|---|---|
| `else: break` | leaves the loop |
| `return ...` | leaves the loop and the function, giving the value |
| `pass` | does nothing, stands in for an empty block |
| `continue` | goes back to the top of the loop |

## Reading until the input ends

```python
while True:
    try:
        line = input()
    except EOFError:
        break
```
