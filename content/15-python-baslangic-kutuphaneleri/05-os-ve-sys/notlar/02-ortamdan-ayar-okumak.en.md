In real projects, settings like the port, the database address, debug mode
or an API key are not written in the code; they are read from **environment
variables**. The same code runs on your computer, on a test server and on the
real server with different settings.

## Reading with a default and a converted type

```python
import os


def load_settings():
    return {
        "mode": os.environ.get("APP_MODE", "production"),
        "port": int(os.environ.get("APP_PORT", "8000")),
        "debug": os.environ.get("APP_DEBUG", "0") in ("1", "true", "yes"),
    }


print(load_settings())
os.environ["APP_PORT"] = "9090"
os.environ["APP_DEBUG"] = "true"
print(load_settings())
print(bool("0"), bool("false"), bool(""))
```

```text
{'mode': 'production', 'port': 8000, 'debug': False}
{'mode': 'production', 'port': 9090, 'debug': True}
True True False
```

- Every setting has a **default**; if the variable is not defined, the
  program still runs.
- A number is converted with `int(...)`; values are always text.
- A yes/no setting is not converted with `bool(...)`: **every non-empty text
  is `True`**, even `"0"` and `"false"`. Write the accepted values
  explicitly.

## Giving an environment variable

In the terminal, before starting the program:

| Shell | Code |
|---|---|
| PowerShell (Windows) | `$env:APP_PORT = "9090"` |
| Command Prompt (cmd) | `set APP_PORT=9090` |
| Linux / macOS | `export APP_PORT=9090` |

This applies only in that terminal window; it ends when the window closes.

## Secrets are not written in code

If values like API keys and passwords are written inside the code, they go to
GitHub with the code and everyone sees them. They are read from an
environment variable:

```python
import os

api_key = os.environ.get("WEATHER_API_KEY")
if api_key is None:
    print("WEATHER_API_KEY is not set")
```

In projects these values are often kept in a file called `.env`, and the file
is kept out of the repository with `.gitignore`.

## Simple arguments with sys.argv

When you type `python resize.py photo.jpg 800`, `sys.argv` is `['resize.py',
'photo.jpg', '800']`. That is enough for small scripts with two or three
arguments; for tools with options and help text, `argparse` from the advanced
Python module is used.
