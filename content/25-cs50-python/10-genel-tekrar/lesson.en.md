# Overall Review

You have reached the end of CS50 Python's ten weeks. In the first week you
printed a line with `print`; now you can write programs that read files, take
options from the command line, check input with regular expressions, build
their own classes and come with tests you wrote. This section walks the path
once more; at the end there is a program that uses the weeks' tools together.
The quiz has four questions from each week, and the exercises are five
problems that combine several weeks.

<figure class="fig">
  <div class="flow">
    <span class="node">Basics<br><small>0–3</small></span><span class="arrow">→</span>
    <span class="node">Tools<br><small>4–5</small></span><span class="arrow">→</span>
    <span class="node">Data<br><small>6–7</small></span><span class="arrow">→</span>
    <span class="node">Classes<br><small>8</small></span><span class="arrow">→</span>
    <span class="node acc">Et Cetera<br><small>9</small></span>
  </div>
  <figcaption>The course's path: first the basics of the language, then using other people's code and testing your own, then files and text, and at the end your own types and small tools.</figcaption>
</figure>

## Week 0: Functions, variables

| Syntax | What it does |
|---|---|
| `name = input("What's your name? ")` | gets a **string** from the user |
| `int(...)`, `float(...)` | turns a string into a number |
| `print("a", "b", sep="-", end="")` | the separator and line ending can be chosen |
| `f"{x:.2f}"` | an f-string, two digits after the point |
| `def hello(to="world"):` | a parameter with a default value |
| `return` | the function's result; without it, `None` |

## Week 1: Conditionals

| Syntax | What it does |
|---|---|
| `if` / `elif` / `else` | the first branch that holds runs |
| `and`, `or`, `not` | combine conditions; `name == "a" or name == "b"` |
| `n % 2 == 0` | is it even |
| `match name:` / <code>case "Harry" &#124; "Ron":</code> / `case _:` | branching on a value |

## Week 2: Loops

| Syntax | What it does |
|---|---|
| `for i in range(3):` | 0, 1, 2 |
| `while True:` ... `break` | ask until a valid input comes |
| `for x in a_list:` | the items of a list |
| `for key in a_dict:` / `a_dict[key]` | a dictionary's keys and values |
| `a_list[-1]`, `len(a_list)` | the last item, the length |

## Week 3: Exceptions

```python
while True:
    try:
        x = int(input("What's x? "))
    except ValueError:
        print("x is not an integer")
    else:
        break
```

- `try` wraps only the line that can fail; `else` runs if no error happened.
- `except ValueError: pass` catches the error and does nothing.
- `raise ValueError("...")` raises an error in your own code.

## Week 4: Libraries

| Syntax | What it does |
|---|---|
| `import random` / `random.choice(...)` | brings in a module |
| `from random import choice` | brings in a single name |
| `sys.argv` | command-line arguments; `[0]` is the program's name |
| `sys.exit("message")` | prints the message and exits with code 1 |
| `pip install cowsay` | installs a package from PyPI |
| `requests.get(url).json()` | JSON from an API |

## Week 5: Unit Tests

```python
import pytest
from calculator import square


def test_square():
    assert square(2) == 4
    assert square(-3) == 9


def test_str():
    with pytest.raises(TypeError):
        square("cat")
```

- File and function names start with `test_`; `pytest test_calculator.py`.
- The function under test does not print, it **returns**.
- `if __name__ == "__main__": main()` keeps `main` from running when the
  module is imported.

## Week 6: File I/O

| Syntax | What it does |
|---|---|
| `with open("names.txt") as file:` | reads, and closes it by itself at the end |
| `open(..., "w")` / `open(..., "a")` | writes from scratch / appends to the end |
| `line.rstrip()` | removes the newline |
| `csv.DictReader(file)` | each row is a dictionary keyed by the header names |
| `csv.DictWriter(file, fieldnames=[...])` | writes dictionaries to a CSV |
| `sorted(rows, key=lambda r: r["name"])` | sorts by a key |
| `Image.open(...)` (Pillow) | image files |

## Week 7: Regular Expressions

| Pattern | Meaning |
|---|---|
| `.` / `\.` | any character / an actual dot |
| `*`, `+`, `?`, `{2}`, `{2,4}` | how many times |
| `^`, `$` | start and end of the text |
| `[A-Z]`, `[^@]`, `\d`, `\w`, `\s` | character sets |
| `(...)`, `(?:...)`, <code>&#124;</code> | group, non-capturing group, or |

- `re.search` looks anywhere in the text, `re.fullmatch` at the whole text.
- `matches.group(1)` gives the first group; if it fails, `re.search` returns
  `None`.
- `re.sub(pattern, new, text)` replaces; patterns are raw strings `r"..."`.

## Week 8: Object-Oriented Programming

| Syntax | What it does |
|---|---|
| `class Student:` / `Student("Harry", "Gryffindor")` | a new type / an object |
| `def __init__(self, name):` / `self.name = name` | initializes the object |
| `def __str__(self): return ...` | `print(obj)` uses it |
| `@property` / `@house.setter` | a check on assignment |
| `@classmethod` / `cls` | a method called without an object |
| `class Student(Wizard):` / `super().__init__(name)` | inheritance |
| `def __add__(self, other):` | gives the `+` operator a meaning |

## Week 9: Et Cetera

| Syntax | What it does |
|---|---|
| `set()`, `add` | each value once |
| `global balance` | change a global variable |
| `def meow(n: int) -> str:` | type hints; mypy checks them |
| `argparse` | command-line options, `-h` |
| `f(*a_list)`, `f(**a_dict)`, `def f(*args, **kwargs)` | unpacking and gathering |
| `map`, `filter`, `[... for ... if ...]`, `{k: v for ...}` | transform, drop, comprehensions |
| `enumerate(a_list, start=1)` | position and item |
| `yield` | a generator that hands out values one at a time |

## All together

A list of students, `students.csv`:

```text
name,house
Hermione,Gryffindor
Harry,Gryffindor
ron,Gryffindor
Draco,Slytherin
Luna,Ravenclaw
Cedric,Hufflepuff
```

The program below takes the file's name from the command line (week 4),
reads the CSV (week 6), builds each student with a class that checks the
name with a regular expression (weeks 7 and 8), catches an invalid row with
an exception and skips it (week 3), hands out the students with a generator,
numbers them with `enumerate` and collects the houses with a set
comprehension (week 9):

```python
import csv
import re
import sys


class Student:
    def __init__(self, name, house):
        if not re.fullmatch(r"[A-Z][a-z]+", name):
            raise ValueError(f"Invalid name: {name}")
        self.name = name
        self.house = house

    def __str__(self):
        return f"{self.name} from {self.house}"


def read_students(path):
    with open(path) as file:
        for row in csv.DictReader(file):
            try:
                yield Student(row["name"], row["house"])
            except ValueError as e:
                print(e)


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python roster.py FILE")
    students = list(read_students(sys.argv[1]))
    for i, student in enumerate(sorted(students, key=lambda s: s.name), start=1):
        print(i, student)
    houses = {student.house for student in students}
    print(*sorted(houses), sep=", ")


if __name__ == "__main__":
    main()
```

```text
$ python roster.py students.csv
Invalid name: ron
1 Cedric from Hufflepuff
2 Draco from Slytherin
3 Harry from Gryffindor
4 Hermione from Gryffindor
5 Luna from Ravenclaw
Gryffindor, Hufflepuff, Ravenclaw, Slytherin
```

`ron` starts with a lowercase letter, so `Student` rejected it and the
program skipped it and carried on. If no file name is given:

```text
$ python roster.py
Usage: python roster.py FILE
```

Every line of this code comes from one of the ten weeks. `{student.house for
student in students}` is a **set comprehension**: curly braces but no
`key: value`; each house goes in once.

## After this

In CS50 the last step of the course is a **final project**: solving a
problem of your own choosing, one that interests you, with Python. The What
Comes Next note lists the paths you can continue on in Odyssey.

---

*This section is adapted from Harvard University's [CS50's Introduction to
Programming with Python](https://cs50.harvard.edu/python/) as a whole; the
questions and exercises are Odyssey's. The original and this adaptation are
licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
Harvard does not endorse this adaptation.*
