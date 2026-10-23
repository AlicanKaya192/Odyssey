Everything from week 0 on one page.

## Terminal

| Command | What it does |
|---|---|
| `python hello.py` | runs the file `hello.py` |
| `python` | opens interactive mode (`>>>`); leave with `exit()` |
| up arrow | brings back the last command |

## Functions

| Code | What it does | Example |
|---|---|---|
| `print(a, b)` | prints the arguments with a space between, then a newline | `print("hello,", name)` |
| `print(a, end="")` | no newline at the end (and no space either) | `print("hello, ", end="")` |
| `print(a, b, sep="-")` | puts `-` in between | `a-b` |
| `input("prompt ")` | prints the prompt, returns what was typed **as text** | `name = input("Name: ")` |
| `int(x)` / `float(x)` | turns text into a number | `int("42")` → `42` |
| `round(x)` / `round(x, 2)` | rounds (returns a number) | `round(2/3, 2)` → `0.67` |

## String methods

All of them return a **new** string; assign the result to a variable.

| Method | Result (`s = " Hello, World "`) |
|---|---|
| `s.strip()` | `"Hello, World"` |
| `s.lower()` / `s.upper()` | `" hello, world "` / `" HELLO, WORLD "` |
| `s.title()` | first letter of every word capitalised |
| `s.replace(" ", "...")` | `...` in place of every space |
| `"$5".removeprefix("$")` | `"5"` |
| `"15%".removesuffix("%")` | `"15"` |

## Formatted strings (f-strings)

| Code | Result |
|---|---|
| `f"hello, {name}"` | the variable's value goes into the text |
| `f"{z:,}"` | thousands separator: `1,000` |
| `f"{z:.2f}"` | two digits after the point: `0.67` |

## Operators

| Operator | Meaning | `7 ? 2` |
|---|---|---|
| `+ - *` | add, subtract, multiply | `9`, `5`, `14` |
| `/` | division (always a float) | `3.5` |
| `//` | floor division (rounds down) | `3` |
| `%` | remainder of a division | `1` |
| `**` | exponent | `49` |

## Your own function

```python
def main():
    x = int(input("What's x? "))
    print("x squared is", square(x))


def square(n):
    return n * n


main()
```

- `def name(parameter):` defines it; the body is **indented**.
- `return` hands the value back to the caller; `print` only writes to the screen.
- Without the `main()` call at the end of the file, nothing runs.
- `def hello(to="world"):` uses the default value when no argument is given.
