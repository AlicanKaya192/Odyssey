This module showed the standard tools needed to **grow** a program. From here
the road opens in two directions: data science libraries and the extra tools
used in real projects.

## Data Science and ML Libraries

The next two modules of this path leave the standard library: NumPy, pandas,
Matplotlib, seaborn, SciPy; then scikit-learn and model libraries. What you
learned here will help there too:

- **Types and dataclasses** keep model settings and experiment records clear.
- **logging** records what happens during long training runs.
- **argparse** makes experiment scripts configurable from the command line.
- **pickle** is the most common way to store trained models (and the same
  security rule applies: do not load a model file you do not trust).
- **concurrent.futures** and **cProfile** for speeding up and measuring big
  data jobs.
- **tracemalloc** for watching the memory of big tables (except pandas' Arrow
  columns).

## Extra tools common in real projects

These are separate packages; worth knowing:

| Tool | For |
|---|---|
| `pytest` | shorter tests (covered in the Writing APIs module) |
| `mypy`, `pyright` | checking type hints without running the code |
| `ruff`, `black` | format and style checks, automatic fixes |
| `httpx`, `aiohttp` | async HTTP clients |
| `SQLAlchemy` | a database layer, several databases |
| `cryptography` | encryption (hiding and opening again) |
| `click`, `typer` | command line tools shorter than argparse |

## Exploring on your own

- The "The Python Standard Library" documentation has the details of every
  module in this module and more (`enum`, `struct`, `ipaddress`,
  `zoneinfo`...).
- Reading a library's source teaches too: `import inspect;
  print(inspect.getsource(functools.wraps))`.
- Write your own small tool: a notebook or an expense tracker with argparse +
  logging + sqlite3 + unittest; the whole module together.
