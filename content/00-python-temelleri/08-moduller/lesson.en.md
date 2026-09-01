# Modules

Everything you have written so far lived in a single file. For small programs
that is fine. But as a file grows, two problems appear: you want to use the
same function in another program, and past a certain point nobody can read
the file any more.

A **module** is the answer: you split the code into separate files and pull in
whatever you need.

There is something else, and it may matter more: Python ships with
**thousands of ready-made functions**. You do not have to write code from
scratch to take a square root, work with dates or generate a random number.
You only need to know how to reach that code.

## What is a module?

A module is a file with Python code in it. That is all.

There is a file called `math.py` with a square-root function inside. When you
write `import math`, Python finds that file, runs it, and makes its contents
available to you.

## `import` — bring in the module

```python
import math

print(math.sqrt(16))
print(math.floor(3.7))
print(math.ceil(3.2))
```

```
4.0
3
4
```

Notice that you cannot call `sqrt` on its own; you put `math.` in front of it.
That dot means "inside this module".

`math.sqrt(16)` gave `4.0`, not `4` — `sqrt` always returns a decimal number.

## `from ... import ...` — take only what you need

If you would rather not write `math.` every time, you can take the pieces you
use directly:

```python
from math import sqrt, pi

print(sqrt(25))
print(pi)
```

```
5.0
3.141592653589793
```

This time you called it with nothing in front.

Which one is right? Both. But there is a difference: once you write
`from math import sqrt`, the rest of your code no longer shows where `sqrt`
came from. `math.sqrt` explains itself. So if you use many functions from a
module, `import math` reads better; for one or two, `from math import ...` is
more comfortable.

## Don't: `from math import *`

There is a form that brings in **everything** from a module:

```python
from math import *   # don't do this
```

The problem is that you do not know what is in there. If you had your own
variable called `pi`, it is quietly overwritten and you find the bug hours
later. Say what you are taking.

## `as` — a nickname

When you want to shorten a long module name:

```python
import statistics as st

print(st.mean([10, 20, 30]))
```

```
20
```

You will see a lot of this on the data science side later: `import pandas as
pd`, `import numpy as np`. These are the abbreviations everyone uses; if you
use the same ones, other people recognise your code immediately.

## Your own module

A module is nothing magical: **a `.py` file you wrote is a module too.**

Say there is a file called `toolbox.py` in the same folder:

```python
# toolbox.py

def double(number):
    return number * 2

def greet(name):
    return "Hello, " + name
```

You call it from the file next to it:

```python
import toolbox

print(toolbox.double(21))
print(toolbox.greet("Ada"))
```

```
42
Hello, Ada
```

The file is `toolbox.py`, the module is `toolbox` — you leave out the
extension.

## A few familiar names from the standard library

The modules that ship with Python are called the **standard library**. None of
them need installing:

| Module | What it is for |
|---|---|
| `math` | Square roots, rounding, `pi`, trigonometry |
| `random` | Random numbers, picking from a list at random |
| `statistics` | Mean, median, standard deviation |
| `datetime` | Date and time arithmetic |
| `json` | Turning JSON text into Python objects |
| `os` | Folders and file paths |

A couple of examples:

```python
import random

random.seed(42)          # so you get the same result again
print(random.randint(1, 6))
```

```python
from datetime import date

today = date(2026, 3, 15)
print(today.year)
print(today.strftime("%d/%m/%Y"))
```

```
2026
15/03/2026
```

## What is not in the standard library

There are also modules you install yourself — `pandas`, `requests`,
`matplotlib` and so on. They do not come with Python; `pip install` downloads
them onto your computer.

The exercises in this application only use the standard library, so there is
nothing to install.

## `if __name__ == "__main__"`

A line you will often see in module files:

```python
# toolbox.py

def double(number):
    return number * 2

if __name__ == "__main__":
    print(double(5))
```

It means: "if this file was run **directly**, do this as well; if another file
imported me, don't."

Why is it needed? Because the moment you write `import toolbox`, Python runs
that file from top to bottom. Without that line, `10` would be printed on your
screen just because you wanted to use the `double` function.

For now keep it in the back of your mind as "this is where they put their test
code"; it will come back when we get to object-oriented programming.

## Summary

- A module is a `.py` file with code in it. Yours count too.
- `import math` → `math.sqrt(16)`
- `from math import sqrt` → `sqrt(16)`
- `import statistics as st` → `st.mean(...)`
- Don't write `from math import *`; make it clear what you are taking.
- The modules that ship with Python are the standard library; they need no
  installing.
