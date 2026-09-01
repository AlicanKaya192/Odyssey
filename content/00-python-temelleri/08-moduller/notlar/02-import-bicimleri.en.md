# Import Forms and Common Mistakes

## Four forms, one job

```python
import math                      # math.sqrt(16)
from math import sqrt            # sqrt(16)
from math import sqrt, pi, floor # take several at once
import statistics as st          # st.mean(...)
from math import sqrt as root    # give what you took a nickname
```

They all bring in the same code; only the name in your file changes.

## Where do `import` lines go?

At the **top** of the file, all together:

```python
import math
import random

from statistics import mean


def main():
    ...
```

They can go inside a function too, but do not do that without a reason; what
a file depends on should be visible at a glance.

The usual order is: the standard library first, then packages you installed,
then your own files. A blank line between the groups.

## Mistake 1: `ModuleNotFoundError`

```
ModuleNotFoundError: No module named 'pandas'
```

It means the module is not on your computer. There are two reasons: either you
misspelled the name (`pandas`, not `panda`), or the module is not part of the
standard library and needs installing.

If you get the same error for one of your own files, that file is not in the
same folder as the file you are running.

## Mistake 2: Naming a file after a module

This is the trap beginners fall into most. If you name your own file
`math.py`:

```python
# math.py  <- your own file
import math
print(math.sqrt(16))
```

```
AttributeError: module 'math' has no attribute 'sqrt'
```

Python finds your file under the name `math` and brings it in instead of the
real `math` module. The same goes for `random.py`, `json.py`, `string.py`.

**Rule: do not name your files after things in the standard library.**

## Mistake 3: Circular imports

If `a.py` has `import b` and `b.py` has `import a`, Python leaves both half
finished and gives strange errors.

Usually this is a sign that the two files are really doing one job. Moving the
shared part into a third file that both import solves it.

## When does an `import` run?

A module is executed **once** per program. Even if two different files write
`import toolbox`, `toolbox.py` runs from top to bottom only once; the second
`import` hands back what is already there.

That is why putting slow work at the top of a module file is a bad idea: it
runs for whoever imports that module.

## What does `if __name__ == "__main__"` solve?

```python
# toolbox.py
def double(number):
    return number * 2

print(double(5))    # <- this is the problem
```

The moment another file writes `import toolbox`, `10` is printed on screen —
and you only wanted the function.

```python
if __name__ == "__main__":
    print(double(5))
```

That line means "if this was run directly". When the file is imported,
`__name__` holds `"toolbox"` rather than `"__main__"`, the condition fails and
the line is skipped.

## Small habits

- Do not import a module you are not using; the list at the top of a file is a
  document describing what the file depends on.
- Do not write `from module import *`.
- Do not invent your own nicknames; use the established ones like `pd`, `np`
  and `plt`, and spell out the full module name for everything else.
