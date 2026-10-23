Everything from week 9 on one page.

## Sets

| Syntax | What it does |
|---|---|
| `houses = set()` | an empty set (`{}` is an empty **dictionary**) |
| `{"Gryffindor", "Slytherin"}` | a set with values |
| `houses.add("Ravenclaw")` | adds; if it is already there, nothing changes |
| `"Ravenclaw" in houses` | is it in there; very fast on a set |
| `sorted(houses)` | a sorted list (a set has no order) |

## Global variables and constants

| Syntax | What it does |
|---|---|
| `balance = 0` (at the top of the file) | a global variable; functions can read it |
| `global balance` | inside a function: this name is the global variable and may be changed |
| `MEOWS = 3` | a constant; capital letters are only a convention, Python does not protect it |
| `Cat.MEOWS` | a constant inside a class |

## Type hints and docstrings

```python
def meow(n: int) -> str:
    """Meow n times."""
    return "meow\n" * n


number: int = int(input("Number: "))
```

- `n: int` for a parameter, `-> str` for the return value, `number: int` for a variable
- Python stores the hint in `meow.__annotations__` but does **not check** it
- The separate program that checks: `pip install mypy`, then `mypy meows.py`
- A function that returns no value: `-> None`
- The docstring is on the first line of the body, in triple quotes; `meow.__doc__`

## argparse

```python
import argparse

parser = argparse.ArgumentParser(description="Meow like a cat")
parser.add_argument("-n", default=1, help="number of times to meow", type=int)
args = parser.parse_args()
```

| Syntax | What it does |
|---|---|
| `add_argument("-n", "--number")` | short and long name; the value is `args.number` |
| `default=1` | the value when not given (otherwise `None`) |
| `type=int` | converts; if invalid, prints the usage and exits (code 2) |
| `help="..."` | the explanation in the `-h` / `--help` output |

## Unpacking and gathering

| Syntax | What it does |
|---|---|
| `first, _ = "David Malan".split(" ")` | unpacks into two variables; `_` is the unused one |
| `total(*coins)` | unpacks a list into positional arguments |
| `total(**coins)` | unpacks a dictionary into `key=value` arguments |
| `def f(*args):` | gathers positional arguments in a **tuple** |
| `def f(**kwargs):` | gathers named arguments in a **dictionary** |

## map, filter, comprehensions, enumerate

| Syntax | What it does |
|---|---|
| `map(str.upper, words)` | applies to every item; a single-use `map` object |
| `filter(lambda s: s["house"] == "Gryffindor", students)` | keeps those that return `True` |
| `[w.upper() for w in words]` | a list comprehension |
| `[s["name"] for s in students if s["house"] == "Gryffindor"]` | a list comprehension with a condition |
| `{s: "Gryffindor" for s in names}` | a dictionary comprehension |
| `for i, s in enumerate(names):` | position (from zero) and item |
| `enumerate(names, start=1)` | count from one |

## Generators

```python
def sheep(n):
    for i in range(n):
        yield "🐑" * i
```

- `yield` hands out a value; the function pauses and remembers where it was
- Not all the data is held in memory; it starts right away even for a huge `n`
- `sheep(3)` does not run the body; it returns a generator object
- `next(g)` is the next value; when none are left, `StopIteration`
- A generator is used up once; call it again to go through it again
