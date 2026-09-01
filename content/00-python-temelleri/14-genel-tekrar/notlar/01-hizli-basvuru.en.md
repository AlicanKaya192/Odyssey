# Quick Reference

A one-page summary of everything you learned in Python Fundamentals. Not to
memorise — to look up when you think "how was that written again?"

## Variables and types

```python
name = "Ada"          # str
age = 36              # int
ratio = 3.14          # float
active = True         # bool
nothing = None        # NoneType
```

```python
int("42")             # text to number
str(42)               # number to text
float("3.5")          # to decimal
type(age)             # find out the type
```

## String operations

```python
text.strip()              # drop whitespace at both ends
text.lower()              # lower case
text.upper()              # upper case
text.split(",")           # split on a separator
text.split(",", 1)        # split at most once
"-".join(parts)           # join a list into text
text.replace("a", "b")    # replace
text.startswith("A")      # does it start with
len(text)                 # length
f"{name} is {age}"        # formatting
```

## Operators

```python
7 / 2       # 3.5   decimal division
7 // 2      # 3     floor division
7 % 2       # 1     remainder
2 ** 3      # 8     power
```

```python
==  !=  >  <  >=  <=
and  or  not
in  not in
is  is not          # only with None, True and False
```

**There is a surprise in rounding.** Python rounds an exact half to the
nearest **even** number, not upwards:

```python
round(0.5)     # 0
round(1.5)     # 2
round(2.5)     # 2
round(82.5)    # 82
```

It is not a bug, it is deliberate: across many roundings, always rounding up
inflates the total. But it catches you out if you are not expecting it. If you
always want to round up, there is `math.ceil`.

## Conditions

```python
if score >= 90:
    grade = "A"
elif score >= 50:
    grade = "B"
else:
    grade = "F"
```

```python
if 18 <= age < 65:        # chained
if not items:             # is it empty
if value is None:         # checking for None
```

## Loops

```python
for item in items:
    print(item)

for index, item in enumerate(items):
    print(index, item)

for key in scores:
    print(key, scores[key])

while count < 10:
    count = count + 1
```

```python
break          # end the loop
continue       # skip this step
range(5)       # 0 1 2 3 4
range(2, 8)    # 2 ... 7
range(0, 10, 2)   # 0 2 4 6 8
```

## Functions

```python
def greet(name, greeting="hello"):
    return greeting + " " + name

def stats(values):
    return min(values), max(values)     # two values come back

low, high = stats([3, 1, 5])
```

`print` shows, `return` gives. Do not mix them up.

```python
def total(*numbers):        # however many arrive, collected in a tuple
    return sum(numbers)


def describe(**details):    # named ones collected in a dictionary
    return details


sorted(people, key=lambda p: p["grade"], reverse=True)
```

## Comprehensions

```python
[x * 2 for x in items]                  # transform each element
[x for x in items if x > 0]             # filter
[x.upper() for x in names if len(x) < 5]   # both at once
{k: v for k, v in scores.items()}       # produces a dictionary
```

If it does not fit on one line, write a loop rather than a comprehension.

## Checking

```python
assert total([1, 2]) == 3
assert total([]) == 0, "an empty list should give zero"
```

`assert` raises an `AssertionError` when the condition does not hold. Handy in
small scripts for checking "is it right so far".

## Lists and tuples

```python
items = [10, 20, 30]

items[0]          # first
items[-1]         # last
items[1:3]        # a slice
items.append(40)
items.insert(0, 5)
items.remove(20)
items.pop()
items.sort()
items.reverse()
len(items)
```

```python
point = (3, 7)        # a tuple: cannot be changed
single = ("only",)    # a one-element tuple needs the comma
```

```python
sum(items)   max(items)   min(items)   sorted(items)
```

## Dictionaries

```python
scores = {"Ada": 90, "Alan": 70}

scores["Ada"]              # get a value
scores["Grace"] = 85       # add or change
scores.get("Nobody")       # None if absent, no error
scores.get("Nobody", 0)    # 0 if absent
del scores["Alan"]

"Ada" in scores            # is the key there
scores.keys()
scores.values()
scores.items()
```

```python
for name, value in scores.items():
    print(name, value)
```

## Modules

```python
import math
from datetime import date
import statistics as stats

math.sqrt(16)
math.floor(3.7)
math.pi

date(2026, 1, 1)
```

```python
if __name__ == "__main__":
    main()
```

## Handling errors

```python
try:
    number = int(text)
except ValueError:
    number = 0
except (KeyError, IndexError):
    number = -1
else:
    print("worked")
finally:
    print("done")
```

```python
raise ValueError("age cannot be negative")

except ValueError as error:
    print(error)
```

| Error | When |
|---|---|
| `ValueError` | Right type, impossible value |
| `TypeError` | Wrong type |
| `KeyError` | Not in the dictionary |
| `IndexError` | Not in the list |
| `FileNotFoundError` | The file is not there |
| `ZeroDivisionError` | Division by zero |

## Type annotations

```python
def repeat(text: str, count: int) -> str:
    return text * count

scores: list[int] = []
ages: dict[str, int] = {}
point: tuple[int, int] = (3, 7)

def find(name: str) -> int | None:
    return None

def greet(name: str) -> None:
    print(name)
```

## Files

```python
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("line\n")

with open("notes.txt", "a", encoding="utf-8") as file:
    file.write("more\n")

with open("notes.txt", encoding="utf-8") as file:
    content = file.read()
    # or
    lines = file.read().splitlines()
    # or
    for line in file:
        print(line.strip())
```

| Mode | What it does |
|---|---|
| `"r"` | Reads (the default) |
| `"w"` | **Wipes** and writes |
| `"a"` | Appends |
| `"x"` | Fails if the file exists |

## Classes

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def is_passing(self):
        return self.grade >= 50

    def __str__(self):
        return self.name + ": " + str(self.grade)

class Honours(Student):
    def __init__(self, name, grade):
        super().__init__(name, grade)
        self.honours = True
```

```python
ada = Student("Ada", 90)
ada.name
ada.is_passing()
```

## Databases

```python
import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("CREATE TABLE students (name TEXT, grade INTEGER)")
cursor.execute("INSERT INTO students VALUES (?, ?)", ("Ada", 90))
cursor.executemany("INSERT INTO students VALUES (?, ?)", rows)
connection.commit()

cursor.execute("SELECT name, grade FROM students WHERE grade >= ?", (50,))
rows = cursor.fetchall()
row = cursor.fetchone()

connection.close()
```

```sql
SELECT name FROM students WHERE grade >= 50 ORDER BY grade DESC LIMIT 3
SELECT city, AVG(grade) FROM students GROUP BY city
UPDATE students SET grade = ? WHERE name = ?
DELETE FROM students WHERE grade < ?
```
