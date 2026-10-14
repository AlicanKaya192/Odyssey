| Gate | Tool | Command in the pipeline | Closes when |
|---|---|---|---|
| Syntax | Python | `python -m py_compile file.py` | The code cannot be read. |
| Format | ruff, black | `ruff format --check .` | A file is not formatted. |
| Lint | ruff, flake8, pylint | `ruff check .` | A rule is broken (prints the file, line and rule code). |
| Types | mypy | `mypy .` | The types are inconsistent. |
| Tests | pytest | `python -m pytest` | A test failed. |
| Coverage | coverage.py, pytest-cov | `python -m pytest --cov=package --cov-fail-under=80` | Coverage is below the threshold. |

**Reminders**

- In a pipeline the formatter always runs with `--check`; the developer
  makes the fix (`ruff format .`).
- A gate's decision comes from the exit code: `0` passed, any other
  number closed.
- Cheap gates first: syntax → format → lint → tests → coverage.
- Run the same commands on your own computer before pushing. The way to
  do it automatically is hooks that run before a commit (pre-commit).

**Static analysis versus tests**

| | Static analysis | Tests |
|---|---|---|
| Does it run the code? | No, it reads it | Yes |
| What does it see? | Every path of the program | Only the paths tried |
| What can it not see? | What happens while it runs | The paths not tried |
| Speed | Seconds | Seconds to minutes |
