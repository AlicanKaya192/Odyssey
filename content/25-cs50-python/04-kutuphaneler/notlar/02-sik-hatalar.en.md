The most common mistakes when working with libraries and their messages
(measured on Python 3.14). Read the **last line** of an error message first.

## sys.argv[1] with no argument

```python
import sys

print("hello, my name is", sys.argv[1])
```

```text
$ python name.py
Traceback (most recent call last):
  File "name.py", line 3, in <module>
    print("hello, my name is", sys.argv[1])
                               ~~~~~~~~^^^
IndexError: list index out of range
```

If the user typed no argument, the list holds only the program's name. Check
`len(sys.argv)` first and leave with `sys.exit` if need be.

## A misspelled or uninstalled module

```python
import cowsy
```

```text
$ python say.py
Traceback (most recent call last):
  File "say.py", line 1, in <module>
    import cowsy
ModuleNotFoundError: No module named 'cowsy'
```

Check the name; if it is right, the package is not installed: `pip install ...`.

## A name the module does not have

```python
import random

print(random.randomint(1, 10))
```

```text
$ python generate.py
Traceback (most recent call last):
  File "generate.py", line 3, in <module>
    print(random.randomint(1, 10))
          ^^^^^^^^^^^^^^^^
AttributeError: module 'random' has no attribute 'randomint'. Did you mean: 'randint'?
```

The function is called `randint`. Python suggests a close name if it finds one;
otherwise look at the module's documentation.

## Mistakes without an error

These produce no message; the program runs but does not do what you want.

| What you wrote | What happens | Instead |
|---|---|---|
| `cards = random.shuffle(cards)` | `cards` becomes `None` | just `random.shuffle(cards)` |
| `for arg in sys.argv:` | the program's name is handled too | `sys.argv[1:]` |
| `sys.argv[1] + 1` | a `TypeError`: the argument is a string | `int(sys.argv[1])` |
| "one argument" as `len(sys.argv) == 1` | true when there are none | one argument: `len(sys.argv) == 2` |
| expecting 1–9 from `random.randint(1, 10)` | 10 can come too | both ends of `randint` are included |
| naming your own file `random.py` | `import random` takes yours | do not use library names |
