## With a class

```python
class Resource:
    def __enter__(self):
        # set up
        return self

    def __exit__(self, exc_type, exc, tb):
        # tidy up (with or without an error)
        return False   # True swallows the error
```

## With a function

```python
from contextlib import contextmanager


@contextmanager
def resource():
    # set up
    try:
        yield "value"
    finally:
        # tidy up
        ...
```

## contextlib

| Tool | What it does |
|---|---|
| `@contextmanager` | turns a generator function into a context manager |
| `suppress(Error)` | swallows that error |
| `redirect_stdout(f)` / `redirect_stderr(f)` | writes output elsewhere |
| `closing(obj)` | calls `obj.close()` at the end |
| `ExitStack()` | collects resources of unknown number |
| `nullcontext(value)` | a manager that does nothing |
| `chdir(folder)` | changes the working folder temporarily (3.11+) |

## Ready-made context managers

| Code | What it tidies up |
|---|---|
| `open(...)` | closes the file |
| `with conn:` (sqlite3) | commits or rolls back the transaction (does not close!) |
| `tempfile.TemporaryDirectory()` | deletes the folder |
| `threading.Lock()` | releases the lock |
| `decimal.localcontext()` | restores the precision setting |

## The rule

Tidy up inside **`finally`**; `yield` only once.
