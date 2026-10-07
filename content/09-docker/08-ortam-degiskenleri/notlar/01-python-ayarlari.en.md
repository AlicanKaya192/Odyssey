A tidy way to read environment variables in Python: all settings in one
place, with their defaults and types.

## A single settings module

```python
# settings.py
import os

APP_ENV = os.environ.get("APP_ENV", "development")
PORT = int(os.environ.get("PORT", "8000"))
DEBUG = os.environ.get("DEBUG", "false").lower() in ("1", "true", "yes")
DB_URL = os.environ.get("DB_URL", "sqlite:///local.db")
```

The rest of the program says `from settings import PORT`; it does not read
`os.environ` separately everywhere.

## Watch the types

An environment variable is **always text**:

| Read | Wrong | Right |
|---|---|---|
| `PORT=8000` | `PORT + 1` → error (text + number) | `int(PORT) + 1` |
| `DEBUG=false` | `if DEBUG:` → **True** (non-empty text counts as true) | `DEBUG.lower() == "true"` |
| `RATE=0.5` | `RATE * 2` → `"0.50.5"` (the text written twice) | `float(RATE)` |

`if os.environ.get("DEBUG"):` is the most common mistake: the text `"false"`
also counts as true.

## Required settings

Some settings should have no default (e.g. the real database's password). If
one is missing, the program should stop at once with a clear message:

```python
import os
import sys

password = os.environ.get("DB_PASSWORD")
if not password:
    sys.exit("DB_PASSWORD is not set")
```

`sys.exit("message")` prints the message and exits with code 1;
`docker logs` shows the reason.

## The `.env` file

During development it is common to keep settings in a `.env` file:

```text
APP_ENV=development
DB_PASSWORD=local-only-password
```

- It is given with `docker run --env-file .env app`.
- **It is written in `.gitignore` and `.dockerignore`.** The `.env.example`
  that goes into the repository carries only the names and fake values.
