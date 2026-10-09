# logging

In a small script you see what happens with `print`. In a growing program
that is not enough: some messages are needed only while debugging, some
always; some should go to the screen, some to a file; every message's time
and the module it came from should be known. **`logging`** is the standard
tool for this: it splits records into **levels**, marks their source with
**named loggers** and writes them where wanted with **handlers**.

## Levels and basicConfig

```python
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(levelname)s %(name)s: %(message)s")
logging.debug("details only a developer needs")
logging.info("server started on port %d", 8000)
logging.warning("disk %d%% full", 91)
logging.error("could not save %s", "report.csv")
```

```text
INFO root: server started on port 8000
WARNING root: disk 91% full
ERROR root: could not save report.csv
```

- There are five levels: `DEBUG` < `INFO` < `WARNING` < `ERROR` <
  `CRITICAL`. With `level=logging.INFO`, `INFO` and above were written and
  `DEBUG` was skipped. While debugging it is enough to lower the level to
  `DEBUG`; no need to delete `print`s from the code.
- **`basicConfig`** does the simplest setup in one line: where to (`stream`,
  by default the error stream stderr), from which level, in which format.
- `%(levelname)s`, `%(name)s`, `%(message)s` in the format are fields of the
  record; real programs add `%(asctime)s` (the time) at the front too.
- Values in the message are given as **separate arguments** (`"port %d",
  8000`); why that matters is in the common mistakes part.

## Named loggers

```python
import logging
import sys

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(name)s [%(levelname)s] %(message)s"))
root = logging.getLogger()
root.addHandler(handler)
root.setLevel(logging.WARNING)

db = logging.getLogger("shop.db")
web = logging.getLogger("shop.web")
logging.getLogger("shop.db").setLevel(logging.DEBUG)
db.debug("query took 3 ms")
web.info("GET /home")
web.warning("slow response")
print(db.parent.name, web.getEffectiveLevel(), db.getEffectiveLevel())
```

```text
shop.db [DEBUG] query took 3 ms
shop.web [WARNING] slow response
root 30 10
```

- **`logging.getLogger(name)`** gives a named logger; every call with the
  same name returns the **same** object. In modules you write
  `log = logging.getLogger(__name__)`: the module a record came from can be
  read from its name.
- Names build a **tree** with dots: above `shop.db` would be `shop`; here no
  logger called `shop` was ever asked for, so its parent is the root itself.
  A logger without its own level uses the level above it: `shop.web`
  followed the root (`30` = `WARNING`) and its `INFO` was not written;
  `shop.db` was given `DEBUG` (`10`) and only it became talkative.
- Records **propagate** up the tree and the handler at the root wrote them
  all.

## Handlers: screen and file

```python
import logging
import sys
from pathlib import Path

log = logging.getLogger("app")
log.setLevel(logging.DEBUG)
screen = logging.StreamHandler(sys.stdout)
screen.setLevel(logging.WARNING)
screen.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
file = logging.FileHandler("app.log", encoding="utf-8")
file.setFormatter(logging.Formatter("%(levelname)s %(funcName)s: %(message)s"))
log.addHandler(screen)
log.addHandler(file)


def load():
    log.debug("reading config")
    log.warning("config missing, using defaults")


load()
file.close()
print(Path("app.log").read_text(encoding="utf-8"))
```

```text
WARNING: config missing, using defaults
DEBUG load: reading config
WARNING load: config missing, using defaults
```

A logger can have several **handlers**, each with its own level and format:
only warnings to the screen (the first line), everything to the file, in a
detailed format (`%(funcName)s` is the function that wrote the record). The
program's user sees a clean screen; when a problem occurs, the detail is in
the file. For long-running programs, `logging.handlers.RotatingFileHandler`
moves on to a new file at a given size so the file does not keep growing.

## Logging errors: exception

```python
import io
import logging

buffer = io.StringIO()
handler = logging.StreamHandler(buffer)
handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
log = logging.getLogger("calc")
log.addHandler(handler)


def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        log.exception("divide failed for a=%s b=%s", a, b)
        return None


print(divide(6, 0))
lines = buffer.getvalue().splitlines()
print(lines[0])
print(lines[1])
print(lines[-1])
```

```text
None
ERROR: divide failed for a=6 b=0
Traceback (most recent call last):
ZeroDivisionError: division by zero
```

**`log.exception(...)`** is called inside an `except` block: it writes the
message at the `ERROR` level and adds the **traceback**. The lines in between
say in which file and on which line the error occurred (we did not print them
here). Instead of catching an error and silently returning `None`, at least
logging it is the answer to "why was it empty" a week later.

## Common mistakes

```python
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
log = logging.getLogger("demo")
calls = 0


class Expensive:
    def __str__(self):
        global calls
        calls += 1
        return "expensive"


log.debug("value: %s", Expensive())
log.debug(f"value: {Expensive()}")
print(calls)
logging.basicConfig(level=logging.DEBUG)
log.debug("still hidden")
print(logging.getLogger().level == logging.INFO)
```

```text
1
True
```

- **Logging with an f-string:** even with `DEBUG` off, the f-string text is
  built **in advance**: `__str__` was called once. With `"%s", value` the
  text is built only if the record is really written. In often-called places
  the difference grows.
- **A second `basicConfig` does nothing:** it is ignored if the root logger
  already has a handler (the level stayed `INFO`). Set up once at the very
  start of the program; to change it, `force=True`.
- If you write a library, do not call `basicConfig`; only use
  `getLogger(__name__)` and let the program using it decide where to write.

## Summary

- Levels `DEBUG < INFO < WARNING < ERROR < CRITICAL`; those below are not
  written.
- `basicConfig(level=..., format=...)` once at the start of the program.
- `log = logging.getLogger(__name__)` in every module; names build a tree,
  levels and records flow upward.
- Handlers: the screen (`StreamHandler`), a file (`FileHandler`), each with
  its level and format.
- `log.exception` with the traceback; give values as `"%s", x`, not with an
  f-string.
