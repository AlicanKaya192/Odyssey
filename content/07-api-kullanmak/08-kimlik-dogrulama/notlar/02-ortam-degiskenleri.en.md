Practical ways to keep the key apart from the code.

## Environment variables

In the Windows command prompt (for that window only):

```text
set LIBRARY_KEY=your-real-key
python program.py
```

In PowerShell:

```text
$env:LIBRARY_KEY = "your-real-key"
python program.py
```

Reading it in Python:

```python
import os

key = os.environ.get("LIBRARY_KEY")
if key is None:
    raise SystemExit("LIBRARY_KEY is not defined")
```

In a real project do not set a default: if the key is missing, the program
should not quietly run with a wrong key; it should stop and say so.

## The `.env` file

In projects, keys are often kept in a `.env` file in the project folder:

```text
LIBRARY_KEY=your-real-key
LIBRARY_TOKEN=another-token
```

There are ready-made packages that read this file (such as `python-dotenv`).
You can also read it yourself:

```python
def load_env(path=".env"):
    values = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                name, value = line.split("=", 1)
                values[name.strip()] = value.strip()
    return values
```

## `.gitignore`

So that `.env` never enters git, add one line to the `.gitignore` file in the
project root:

```text
.env
```

If you want to share an example, add a `.env.example` file with empty values;
everyone fills in their own key.

## If it leaked

1. **Revoke the key at once** in the API's dashboard.
2. Get a new one and put it in the environment variable.
3. Trying to delete it from the git history is no substitute for revoking:
   copies may already be elsewhere.
