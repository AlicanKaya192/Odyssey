## Levels

| Level | Number | What for |
|---|---|---|
| `DEBUG` | 10 | the developer's detail |
| `INFO` | 20 | ordinary events (started, finished) |
| `WARNING` | 30 | unexpected but going on (the default threshold) |
| `ERROR` | 40 | a job could not be done |
| `CRITICAL` | 50 | the program cannot go on |

## Setup

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger(__name__)
```

## Logging

| Code | What it does |
|---|---|
| `log.info("x=%s", x)` | the value as a separate argument |
| `log.exception("...")` | inside `except`, with the traceback |
| `log.setLevel(logging.DEBUG)` | this logger's threshold |
| `log.getEffectiveLevel()` | the effective level from the tree |

## Handlers

| Class | Where to |
|---|---|
| `StreamHandler(sys.stdout)` | the screen |
| `FileHandler("a.log", encoding="utf-8")` | a file |
| `handlers.RotatingFileHandler(..., maxBytes=, backupCount=)` | a new file when it grows |
| `handlers.TimedRotatingFileHandler(..., when="midnight")` | a new file every day |

Give each handler `setLevel` and `setFormatter(logging.Formatter(...))`.

## Format fields

`%(asctime)s` time, `%(levelname)s` level, `%(name)s` logger, `%(message)s`
message, `%(funcName)s` function, `%(lineno)d` line, `%(module)s` module.
