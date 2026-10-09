# contextlib

When you write `with open(...) as f:`, Python closes the file when the block
ends **no matter what**: whether the block ends normally or an error occurs
inside it. An object that makes this promise is called a **context
manager**. Beyond files, many places need "start, and always tidy up when
done": changing a setting temporarily and restoring it, measuring time,
taking and releasing a lock, entering and leaving a temporary folder. In this
section we write our own context managers and look at **`contextlib`**'s
ready-made tools.

## How does with work?

```python
class Tracker:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"enter {self.name}")
        return self

    def __exit__(self, exc_type, exc, tb):
        print(f"exit {self.name}", exc_type.__name__ if exc_type else None)
        return False


with Tracker("a") as t:
    print("inside", t.name)
try:
    with Tracker("b"):
        raise ValueError("boom")
except ValueError as error:
    print("caught", error)
```

```text
enter a
inside a
exit a None
enter b
exit b ValueError
caught boom
```

- **`__enter__`** is called when entering the block; the value it returns is
  bound to the name after `as`.
- **`__exit__`** is called in every case when leaving the block. If an error
  occurred, it receives its type, the error itself and its traceback
  (`ValueError`); with no error, all three are `None`.
- If `__exit__` returns `False`, the error goes on outward (it was caught
  outside); if it returns `True`, the error is swallowed. Swallowing is rarely
  right.

## @contextmanager: a context manager from a function

Writing a class is long; most of the time a generator function with
**`@contextmanager`** is enough:

```python
import time
from contextlib import contextmanager


@contextmanager
def timer(label, results):
    start = time.perf_counter()
    try:
        yield
    finally:
        results[label] = time.perf_counter() - start


@contextmanager
def temporary_setting(settings, key, value):
    old = settings[key]
    settings[key] = value
    try:
        yield settings
    finally:
        settings[key] = old


results = {}
with timer("sleep", results):
    time.sleep(0.05)
print(round(results["sleep"], 2))
settings = {"debug": False}
with temporary_setting(settings, "debug", True) as s:
    print(s)
print(settings)
try:
    with temporary_setting(settings, "debug", True):
        raise RuntimeError("fail")
except RuntimeError:
    print("after error", settings)
```

```text
0.05
{'debug': True}
{'debug': False}
after error {'debug': False}
```

- The part before **`yield`** works like `__enter__`, the part after like
  `__exit__`; the value `yield` gives goes to the name after `as`.
- The tidying up is inside **`finally`**: even with an error in the block,
  the setting went back (the `after error` line). This is the most important
  rule of the section; at the end we see the forgotten version.

## Ready-made tools: suppress, redirect_stdout

```python
import io
from contextlib import redirect_stdout, suppress
from pathlib import Path

with suppress(FileNotFoundError):
    Path("missing.txt").unlink()
print("still running")
buffer = io.StringIO()
with redirect_stdout(buffer):
    print("captured line")
print(repr(buffer.getvalue()))
```

```text
still running
'captured line\n'
```

- **`suppress(ErrorType)`** swallows that error silently: "delete the file if
  it exists, otherwise never mind". A short way of writing `try/except:
  pass` that states the intent. Give only the error type you expect.
- **`redirect_stdout(target)`** writes the `print`s somewhere other than the
  screen for the length of the block; useful when testing a function whose
  output you want to capture. `io.StringIO` behaves like a text file in
  memory.

## ExitStack: resources whose number is not known

```python
from contextlib import ExitStack
from pathlib import Path

for i in range(3):
    Path(f"part{i}.txt").write_text(f"line {i}\n", encoding="utf-8")
with ExitStack() as stack:
    paths = [f"part{i}.txt" for i in range(3)]
    files = [stack.enter_context(open(p, encoding="utf-8")) for p in paths]
    merged = [f.readline().strip() for f in files]
print(merged, all(f.closed for f in files))
```

```text
['line 0', 'line 1', 'line 2'] True
```

If the number of files to open is not known in advance, nested `with`
statements cannot be written. **`ExitStack`** remembers everything opened
with `enter_context` and closes them all (in reverse order) when the block
ends; even if opening one in the middle fails, the earlier ones are closed.

## chdir and nullcontext

```python
from contextlib import chdir, nullcontext
from pathlib import Path

Path("sub").mkdir()
before = Path.cwd().name
with chdir("sub"):
    print(Path.cwd().name)
print(Path.cwd().name == before)


def maybe(manager=None):
    return manager if manager is not None else nullcontext()


with maybe() as value:
    print("no manager needed", value)
```

```text
sub
True
no manager needed None
```

- **`chdir(folder)`** (Python 3.11+) changes the working folder for the
  length of the block, then goes back.
- **`nullcontext()`** is a context manager that does nothing: when code
  expects a `with` but sometimes there is no real resource, it is used instead
  of writing two versions of the code with `if`.

## A common mistake: tidying up without finally

```python
from contextlib import contextmanager


@contextmanager
def careless(log):
    log.append("open")
    yield
    log.append("close")


log = []
try:
    with careless(log):
        raise KeyError("x")
except KeyError:
    pass
print(log)
```

```text
['open']
```

When an error occurs in the block, it is raised again at the `yield` line and
the lines after it **do not run**: `close` was never written. In a real
program that means a file left open, a lock never released or a setting that
never goes back. Always put `yield` inside `try/finally`.

## Summary

- `with` = `__enter__` (at the start) + `__exit__` (at the end, in every
  case).
- `@contextmanager`: setup before `yield`, tidying up in `finally`.
- `suppress(Error)`: swallow an expected error; `redirect_stdout`: capture
  output.
- `ExitStack`: resources of unknown number; `chdir`, `nullcontext`.
- Write the tidying up in `finally`; otherwise it does not run when an error
  occurs.
