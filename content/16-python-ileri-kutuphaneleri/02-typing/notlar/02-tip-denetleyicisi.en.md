The real gain of hints is the errors caught **before** the code runs. A
**type checker** does this: it reads the code, follows the types and points
out what does not fit. The two most common are **mypy** (a command line tool:
`pip install mypy`, then `mypy file.py`) and **Pyright** (inside the Pylance
extension in VS Code, as underlined warnings while you type).

## What does it catch?

| Code | What the checker says |
|---|---|
| `area("ab", 2)` | a `str` given where a `float` is expected |
| `open_log("app.log", "x")` | `"x"` is not `Literal["r", "w", "a"]` |
| `MAX_SIZE = 5` (while `Final`) | `Final` cannot be reassigned |
| `name.upper()` (while <code>name: str &#124; None</code>) | `None` has no `upper` |
| `movie["ratng"]` (`TypedDict`) | there is no such key |
| a missing `return` in `-> int` | it can return `None` |

## Narrowing None

Before using a value of type `str | None`, you must show it is not `None`;
after checking with `if`, the checker **narrows** the type:

```python
def label(name: str | None) -> str:
    if name is None:
        return "anonymous"
    return name.upper()


print(label(None), label("ada"))
```

```text
anonymous ADA
```

After the `if name is None: return` line, the checker knows `name` is now a
`str`; `name.upper()` gets no warning. The same narrowing happens with
`isinstance`.

## Where to start?

- Hints are added **gradually** (gradual typing): unannotated code still runs
  and is checked; start with the important functions.
- **Function signatures** first (parameters and return): they catch the most
  errors. The checker usually infers the types of local variables itself.
- Describe outside data (JSON, CSV) with `TypedDict`.
- `Any` turns checking off; if you must use it, use it on purpose.
- A hint checks nothing at run time: still validate values from users
  yourself.
