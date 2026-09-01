# Commonly Used Parts of the Standard Library

This note is a reference; you do not have to read it end to end. Come back
when you are working on an exercise and think "wasn't there something ready
made for this?".

## `math` — number work

```python
import math

math.sqrt(16)      # 4.0   square root
math.floor(3.7)    # 3     round down
math.ceil(3.2)     # 4     round up
math.pi            # 3.141592653589793
math.gcd(12, 18)   # 6     greatest common divisor
math.hypot(3, 4)   # 5.0   hypotenuse of a right triangle
```

`floor` and `round` get mixed up. `round` goes to the nearest value, `floor`
always goes down:

```python
round(3.7)         # 4
math.floor(3.7)    # 3
round(3.2)         # 3
math.floor(3.2)    # 3
```

## `random` — randomness

```python
import random

random.randint(1, 6)          # whole number from 1 to 6 (6 included)
random.choice(["a", "b"])     # one element from a list
random.shuffle(my_list)       # shuffles in place, returns nothing
random.random()               # decimal between 0 and 1
```

When you want **the same result again**, you set a seed:

```python
random.seed(42)
print(random.randint(1, 100))   # the same number on every run
```

This helps a great deal while hunting bugs: to find a problem in a random
program you need to be able to reproduce the same randomness.

## `statistics` — summary numbers

```python
from statistics import mean, median, stdev

scores = [70, 85, 90, 60, 95]

mean(scores)      # 80         average
median(scores)    # 85         the middle value
stdev(scores)     # 14.577...  standard deviation
```

The difference between the mean and the median matters. One extreme value in
the list drags the mean away; the median stays put:

```python
salaries = [30, 32, 35, 33, 900]
mean(salaries)     # 206
median(salaries)   # 33
```

Which of these is the "typical salary"? The median. You will be asking this
question a lot in data science.

## `datetime` — dates and times

```python
from datetime import date, timedelta

start = date(2026, 3, 1)
end = date(2026, 3, 15)

(end - start).days           # 14
start + timedelta(days=30)   # 2026-03-31
start.strftime("%d/%m/%Y")   # "01/03/2026"
```

Subtracting two dates does not give a number but an object called a
`timedelta`; you take the number of days out of it with `.days`.

## `json` — between text and objects

```python
import json

text = '{"name": "Ada", "age": 20}'
person = json.loads(text)       # text -> dictionary
person["name"]                  # "Ada"

back = json.dumps(person)       # dictionary -> text
```

When you pull data from an API what arrives is always text; this module is
what turns it into a dictionary.

## `os` and `pathlib` — file paths

```python
from pathlib import Path

Path("data") / "scores.csv"     # data/scores.csv
Path("scores.csv").exists()     # True / False
Path("scores.csv").suffix       # ".csv"
```

Do not build paths by hand with `"data/" + name`; the separator is `\` on
Windows and `/` on Linux, and code you joined by hand does not run on the
other machine. `pathlib` takes care of it.

Reading and writing files is covered in detail in a later section.

## What is inside a module?

You can ask Python what a module contains:

```python
import math
print(dir(math))       # a list of everything in the module
help(math.sqrt)        # the description of one function
```

`dir()` prints a long list, but it helps when you cannot remember the name of
the thing you are looking for.
