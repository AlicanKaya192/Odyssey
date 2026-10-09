# The Standard Library

When you install Python, you get more than the language: hundreds of ready
**modules** come with it — maths, dates and times, files, text processing,
compression, databases, networking, testing... Together they are called the
**standard library**, and none of them needs a separate install. The Python
community calls this "batteries included". In this module you will learn the
most used parts of the standard library one by one; in this first section we
see how to import a module, how to look inside it and how to tell whether it
belongs to the standard library.

## How many modules are there?

Python itself knows the names of the modules in the standard library:
`sys.stdlib_module_names`.

```python
import sys

names = sys.stdlib_module_names
print(sys.version.split()[0], len(names))
public = sorted(n for n in names if not n.startswith("_"))
print(len(public))
print(public[:8])
```

```text
3.14.7 297
194
['abc', 'annotationlib', 'antigravity', 'argparse', 'array', 'ast', 'asyncio', 'atexit']
```

The Python 3.14 on this computer has 297 names; those starting with an
underscore (like `_json`) are helper parts the modules use internally. The
remaining 194 modules are the ones you can use directly. There is no need to
memorise them: in this module we will learn the thirty or so that are most
useful in everyday work.

## Ways of importing

To use a module you first **import** it. There are four common forms:

```python
import math                      # the whole module: math.sqrt(...)
from math import sqrt, pi        # only two names: sqrt(...)
import statistics as st          # a short alias: st.mean(...)
from datetime import date as d   # an alias for a single name

print(math.sqrt(16), sqrt(16), round(pi, 4))
print(st.mean([2, 4, 9]), d(2026, 10, 9))
```

```text
4.0 4.0 3.1416
5 2026-10-09
```

With `import math` you write `math.` every time; longer, but the origin is
always clear. `from math import sqrt` is short, but a reader finds out where
`sqrt` comes from by looking at the top of the file. An alias (`as`) shortens
long module names; in data science everyone knows abbreviations like
`import numpy as np` and `import pandas as pd`.

**Do not write `from math import *`.** Every name in the module is poured into
your file; if your own variable has the same name, it is silently overwritten,
and nobody can tell which name came from where.

## Looking inside a module

There are two ways to learn what a module holds: `dir()` lists the names,
`help()` or `__doc__` shows the description.

```python
import math

public = [n for n in dir(math) if not n.startswith("_")]
print(len(public))
print(public[:6])
print(math.gcd.__doc__.splitlines()[0])
print(math.gcd(12, 18), math.comb(5, 2))
```

```text
62
['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2']
Greatest Common Divisor.
6 10
```

The `math` module has 62 public names. `__doc__` is a function's
documentation string; in the interactive shell `help(math.gcd)` shows the same
text more neatly. When you are not sure what a function does, this is the
first place to look, then the official documentation (docs.python.org).

## Where does a module come from?

There are three kinds of module: those compiled into Python itself
(**built-in**), the `.py` files of the standard library, and **third-party**
packages you install later with `pip` (such as NumPy and pandas).

```python
import sys
import importlib.util


def kind(name):
    if name in sys.builtin_module_names:
        return "built-in"
    if name in sys.stdlib_module_names:
        return "standard"
    if importlib.util.find_spec(name) is not None:
        return "third-party"
    return "missing"


for name in ("math", "json", "numpy", "nosuchmodule"):
    print(name, kind(name))
```

```text
math built-in
json standard
numpy third-party
nosuchmodule missing
```

`math` is written in C and compiled into Python, so it has no file of its own.
`json` is part of the standard library and comes with Python. `numpy` is
installed on this computer but is not in the standard library: a program
using it needs `pip install numpy` on another computer first. `find_spec`
checks whether a module can be found **without importing** it.

This distinction matters in practice: a script that uses only the standard
library runs on any computer with Python installed.

## Summary

- The standard library comes with Python; nothing to install.
- `import m`, `from m import a`, `import m as k`; do not write
  `from m import *`.
- `dir()` shows the names, `help()` and `__doc__` the description.
- `sys.stdlib_module_names` lists the standard library,
  `sys.builtin_module_names` the built-in modules; `importlib.util.find_spec`
  tells whether a module is installed without importing it.
