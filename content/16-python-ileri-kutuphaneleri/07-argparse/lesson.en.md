# argparse

To turn a script into a **command line tool** that someone else (or you a
week later) will use, settings must come from outside instead of being
written in the code: `python report.py sales.csv --top 3 --verbose`.
`sys.argv` gives these as a plain list of strings; converting types, finding
what is missing and writing help text is left to you. **`argparse`** does
all of it: you define the arguments, and it reads, converts, checks and
writes `--help`.

The examples in this section pass the list to `parse_args` themselves; in a
real program no list is given and `sys.argv` is read.

## A first parser

```python
import argparse

parser = argparse.ArgumentParser(prog="report", description="Summarise a CSV file.")
parser.add_argument("path", help="the CSV file to read")
parser.add_argument("--top", type=int, default=5, help="how many rows to show")
parser.add_argument("--verbose", action="store_true", help="print details")
args = parser.parse_args(["sales.csv", "--top", "3"])
print(args)
print(args.path, args.top, args.verbose, type(args.top).__name__)
print(parser.parse_args(["data.csv", "--verbose"]))
```

```text
Namespace(path='sales.csv', top=3, verbose=False)
sales.csv 3 False int
Namespace(path='data.csv', top=5, verbose=True)
```

- A **positional** argument (`path`) is required and given in order.
- An **optional** argument starting with `--` (`--top`) may be left out; if
  it is, `default` is used.
- **`type=int`** converts the text to a number (`args.top` really is an
  `int`).
- **`action="store_true"`** is a switch that takes no value: `True` if
  written, `False` if not.
- The result is a `Namespace`: values are reached as attributes like
  `args.path`; dashes in names like `--top` become underscores.

## Several values, choices, short names

```python
import argparse

parser = argparse.ArgumentParser(prog="convert")
parser.add_argument("files", nargs="+")
parser.add_argument("-f", "--format", choices=["csv", "json"], default="csv")
parser.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("--tag", action="append", default=[])
argv = ["a.txt", "b.txt", "-f", "json", "--tag", "x", "--tag", "y"]
args = parser.parse_args(argv)
print(args.files, args.format, args.quiet, args.tag)
```

```text
['a.txt', 'b.txt'] json False ['x', 'y']
```

- **`nargs="+"`** takes one or more values as a list (`"*"` zero or more,
  `"?"` at most one).
- **`choices`** accepts only the values in the list.
- **`-f`, `--format`** are the short and long names of the same option.
- **`action="append"`** adds a value to a list each time the option is
  written.

## Help text for free

```python
import argparse

parser = argparse.ArgumentParser(prog="report", description="Summarise a CSV file.")
parser.add_argument("path", help="the CSV file to read")
parser.add_argument("--top", type=int, default=5, help="how many rows to show")
print(parser.format_help())
```

```text
usage: report [-h] [--top TOP] path

Summarise a CSV file.

positional arguments:
  path        the CSV file to read

options:
  -h, --help  show this help message and exit
  --top TOP   how many rows to show
```

On the command line, `python report.py --help` (or `-h`) prints this text.
The `help=` descriptions go into it; the usage line is built from the
definition by itself. Good help text is the tool's documentation.

## Bad input

```python
import argparse

parser = argparse.ArgumentParser(prog="report", exit_on_error=False)
parser.add_argument("--top", type=int, default=5)
parser.add_argument("--format", choices=["csv", "json"], default="csv")
for argv in (["--top", "ten"], ["--format", "xml"]):
    try:
        parser.parse_args(argv)
    except argparse.ArgumentError as error:
        print("ArgumentError:", error)
strict = argparse.ArgumentParser(prog="report")
strict.add_argument("path")
try:
    strict.parse_args([])
except SystemExit as error:
    print("SystemExit:", error.code)
```

```text
ArgumentError: argument --top: invalid int value: 'ten'
ArgumentError: argument --format: invalid choice: 'xml' (choose from 'csv', 'json')
SystemExit: 2
```

- `argparse` catches a wrong type, a choice not in the list and a missing
  required argument by itself and says what happened.
- The default behaviour: write the usage line and the error to the error
  stream and end the program with **exit code 2** (`SystemExit`). That is
  right for a command line tool.
- With **`exit_on_error=False`** it raises `ArgumentError` instead of
  exiting; for when you want to handle the error yourself.

## Subcommands

```python
import argparse

parser = argparse.ArgumentParser(prog="notes")
commands = parser.add_subparsers(dest="command", required=True)
add = commands.add_parser("add")
add.add_argument("text")
show = commands.add_parser("list")
show.add_argument("--limit", type=int, default=10)
print(parser.parse_args(["add", "buy milk"]))
print(parser.parse_args(["list", "--limit", "3"]))
```

```text
Namespace(command='add', text='buy milk')
Namespace(command='list', limit=3)
```

Tools with **subcommands**, like `git commit` and `git push`, are built with
`add_subparsers`: each subcommand has its own arguments, and the chosen one
is written to `args.command` with `dest="command"`.

## main(argv=None): a testable tool

```python
import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(prog="greet")
    parser.add_argument("name")
    parser.add_argument("--times", type=int, default=1)
    args = parser.parse_args(argv)
    for _ in range(args.times):
        print(f"hello {args.name}")
    return 0


print(main(["ada", "--times", "2"]))
```

```text
hello ada
hello ada
0
```

`parse_args(None)` reads `sys.argv`; given a list, it reads the list. Putting
the tool inside `main(argv=None)` lets you both run it from the command line
and call it with a list of arguments in a test. At the end of the file write
`if __name__ == "__main__": sys.exit(main())`; the return value becomes the
exit code (0 for success).

## Summary

- `ArgumentParser` + `add_argument` + `parse_args`; the result is a
  `Namespace`.
- Positional is required, `--option` is optional; `type`, `default`,
  `choices`, `nargs`, `action="store_true"` / `"append"`.
- `--help` comes from the definition; `help=` descriptions.
- Bad input: usage + exit code 2 (or `exit_on_error=False`).
- Subcommands with `add_subparsers`; the tool inside `main(argv=None)`.
