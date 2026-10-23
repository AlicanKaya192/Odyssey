Everything from week 4 on one page.

## Importing

| Code | Use |
|---|---|
| `import random` | `random.choice(...)` |
| `from random import choice` | `choice(...)` |
| `from random import choice, randint` | both at once |
| `from sayings import goodbye` | from your own `sayings.py` |

## random and statistics

| Function | What it does |
|---|---|
| `random.choice(["a", "b"])` | a random item from the list |
| `random.randint(1, 10)` | an integer from 1 to 10, **both ends included** |
| `random.shuffle(cards)` | shuffles the list in place, returns `None` |
| `statistics.mean([100, 90])` | the mean: `95` |
| `statistics.median([1, 3, 2])` | the median: `2` |
| `statistics.mode([1, 1, 2])` | the most common value: `1` |

## The command line

For `python name.py David Malan`:

| Code | Value |
|---|---|
| `sys.argv` | `['name.py', 'David', 'Malan']` |
| `sys.argv[0]` | `'name.py'` (the program's name) |
| `sys.argv[1]` | `'David'` (the first argument, a **string**) |
| `sys.argv[1:]` | `['David', 'Malan']` |
| `len(sys.argv)` | `3` |
| `sys.exit("message")` | prints the message and ends the program |

## Slices

| Code (`s = [1, 2, 3, 4]`) | Result |
|---|---|
| `s[1:]` | `[2, 3, 4]` |
| `s[:2]` | `[1, 2]` |
| `s[1:3]` | `[2, 3]` (start included, end excluded) |
| `s[-2:]` | `[3, 4]` (the last two) |
| `"hello"[1:3]` | `"el"` (works on strings too) |

## Packages and APIs

| Code | What it does |
|---|---|
| `pip install cowsay` | installs the package from PyPI (in the terminal) |
| `requests.get(url)` | sends a request to the address |
| `response.json()` | turns a JSON response into a dict/list |
| `json.dumps(data, indent=2)` | turns data into readable JSON text |
| `except requests.RequestException:` | catches connection errors |
