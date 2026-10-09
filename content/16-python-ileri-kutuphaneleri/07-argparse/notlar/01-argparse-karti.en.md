## Skeleton

```python
import argparse
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(prog="tool", description="...")
    parser.add_argument("path")
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args(argv)
    ...
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## add_argument options

| Code | Meaning |
|---|---|
| `"path"` | positional, required |
| `"--top"`, `"-t", "--top"` | optional; short and long name |
| `type=int`, `type=float`, `type=Path` | a converter |
| `default=5` | if not given |
| `required=True` | makes an optional one required |
| `choices=["csv", "json"]` | only these |
| `nargs="+"` / `"*"` / `"?"` / `2` | one+, zero+, at most one, exactly two |
| `action="store_true"` | a switch |
| `action="append"` | add to a list each time it is written |
| `action="count"` | `-vvv` → 3 |
| `help="..."` | help text |
| `dest="name"` | the name inside `args` |

## Other

| Code | What it does |
|---|---|
| `parser.add_subparsers(dest="command")` | subcommands |
| `parser.format_help()` | returns the help text |
| `ArgumentParser(exit_on_error=False)` | `ArgumentError` instead of exiting |
| `parser.error("message")` | exit code 2 with your own error |

On bad input, by default: the usage line + the error to stderr, exit code 2.
