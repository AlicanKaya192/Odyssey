# os and sys

A program does not only calculate; it also talks to the computer it runs on:
it opens folders, lists file names, reads its settings from the environment,
checks which Python version it runs on and, when done, exits with an exit
code. Most of these jobs live in two modules:

- **`os`** (operating system): files, folders, paths, environment variables.
- **`sys`** (system): the Python interpreter itself: the version, command line
  arguments, the module search path, exiting.

## sys: asking the interpreter

```python
import sys

print(sys.version_info[:2] >= (3, 10), sys.version_info.major)
print(sys.platform)
print(sys.argv)
print(type(sys.path).__name__, len(sys.path) > 0)
```

```text
True 3
win32
['main.py']
list True
```

- **`sys.version_info`** gives the version like a tuple; comparing with
  `(3, 10)` asks "is it at least 3.10?". Comparing as text (`"3.9" < "3.10"`)
  gives the wrong answer, the tuple the right one.
- **`sys.platform`** is `win32` on Windows (on 64-bit too), `linux` on Linux,
  `darwin` on macOS.
- **`sys.argv`** holds the arguments the program got on the command line; the
  first element is the script's name. Had you typed `python main.py
  report.csv`, it would be `['main.py', 'report.csv']`.
- **`sys.path`** is the list of folders searched for modules when you write
  `import`.

## Paths: os.path

Building a file path by gluing strings with `+` invites mistakes: Windows
uses `\`, Linux and macOS use `/`. **`os.path.join`** puts the right
separator in by itself.

```python
import os

path = os.path.join("data", "raw", "sales.csv")
print(path)
print(os.path.basename(path), os.path.dirname(path))
print(os.path.splitext("sales.csv"), os.path.splitext("archive.tar.gz"))
print(os.path.exists(path), os.path.isabs(path))
```

```text
data\raw\sales.csv
sales.csv data\raw
('sales', '.csv') ('archive.tar', '.gz')
False False
```

- `basename` is the last part (the file name), `dirname` everything before it
  (the folder).
- `splitext` separates the name and the **last** extension: the extension of
  `archive.tar.gz` is `.gz`.
- `exists` checks whether the path really exists; there is no such file here.
  `isabs` says whether the path is absolute (`C:\...` or `/home/...`); this
  path is **relative**, meaning relative to the folder the program runs in.

On Windows you see `\` in the output; the same code writes
`data/raw/sales.csv` on Linux. `pathlib` in the next section does the same
jobs more readably; but you will see `os.path` a lot in older code and in
libraries.

## Working with folders and files

```python
import os

os.makedirs(os.path.join("project", "data"), exist_ok=True)
os.makedirs(os.path.join("project", "data"), exist_ok=True)
for name in ["a.txt", "b.csv"]:
    with open(os.path.join("project", name), "w") as f:
        f.write("hello")
print(sorted(os.listdir("project")))
os.rename(os.path.join("project", "a.txt"), os.path.join("project", "notes.txt"))
os.remove(os.path.join("project", "b.csv"))
print(sorted(os.listdir("project")))
notes = os.path.join("project", "notes.txt")
print(os.path.isfile(notes), os.path.isdir(notes), os.path.getsize(notes))
```

```text
['a.txt', 'b.csv', 'data']
['data', 'notes.txt']
True False 5
```

- **`os.makedirs(path, exist_ok=True)`** creates every folder along the way;
  if the folder already exists it raises no error (the second line shows
  this).
- **`os.listdir`** gives a folder's contents (files and folders) in **no
  order**; hence `sorted`.
- `os.rename` renames (or moves), `os.remove` deletes a file
  **permanently**; it does not go to the recycle bin.
- `isfile` / `isdir` check what it is, `getsize` how many bytes it has
  (`"hello"` is 5 bytes).

## Walking a tree: os.walk

To walk a folder **together with its subfolders**, use `os.walk`:

```python
import os

for folder in ["shop/data/old", "shop/src"]:
    os.makedirs(folder, exist_ok=True)
for name in ["shop/main.py", "shop/data/sales.csv",
             "shop/data/old/sales-2025.csv", "shop/src/app.py"]:
    open(name, "w").close()
for root, dirs, files in os.walk("shop"):
    dirs.sort()
    print(root, sorted(files))
```

```text
shop ['main.py']
shop\data ['sales.csv']
shop\data\old ['sales-2025.csv']
shop\src ['app.py']
```

For each folder `os.walk` gives three things: the folder's path (`root`), the
names of the subfolders in it (`dirs`) and the names of the files (`files`).
A file's full path is `os.path.join(root, name)`. `dirs.sort()` fixes the
order in which subfolders are walked; if a name is removed from the `dirs`
list, that folder is never entered (the way to skip folders like
`__pycache__` or `.git`).

## Environment variables

**Environment variables** are name = value settings given from outside the
program: which port it runs on, whether it is in test mode, an API key. A
common way to change behaviour without changing the code.

```python
import os

print(os.environ.get("ODYSSEY_MODE", "normal"))
os.environ["ODYSSEY_MODE"] = "test"
print(os.environ["ODYSSEY_MODE"], os.getenv("ODYSSEY_MODE"))
try:
    os.environ["ODYSSEY_PORT"] = 8080
except TypeError as error:
    print("TypeError:", error)
try:
    print(os.environ["ODYSSEY_MISSING"])
except KeyError as error:
    print("KeyError:", error)
```

```text
normal
test test
TypeError: str expected, not int
KeyError: 'ODYSSEY_MISSING'
```

- `os.environ` works like a dictionary. A variable that may be missing is
  read with **`get(name, default)`** or `os.getenv`; square brackets raise
  `KeyError` when it is missing.
- Values are **always text**: a number cannot be written, and the `"8080"`
  you read must be converted with `int(...)`.
- A variable changed inside the program affects only this program (and the
  ones it starts); the computer's setting does not change.

## Common mistakes and exiting

```python
import os
import sys

try:
    os.mkdir(os.path.join("a", "b"))
except OSError as error:
    print(type(error).__name__)
os.makedirs("logs")
try:
    os.makedirs("logs")
except OSError as error:
    print(type(error).__name__)
try:
    sys.exit("stopped: no input file")
except SystemExit as error:
    print("SystemExit:", error.code)
```

```text
FileNotFoundError
FileExistsError
SystemExit: stopped: no input file
```

- `os.mkdir` creates only **one** folder; asking for `a/b` while `a` does not
  exist gives `FileNotFoundError`. To create the ones in between too, use
  `makedirs`.
- `makedirs` raises `FileExistsError` when the folder exists and
  `exist_ok=True` is missing.
- **`sys.exit`** ends the program. It actually raises a `SystemExit` error;
  we caught it here, so the program went on. If given text, it is printed and
  the exit code becomes 1; `sys.exit(0)` means "finished successfully".
  Command line tools and automated jobs look at this code.

## Summary

- `sys.version_info` (compare with a tuple), `sys.platform`, `sys.argv`,
  `sys.path`, `sys.exit`.
- Build paths with `os.path.join`; `basename`, `dirname`, `splitext`,
  `exists`, `isfile`, `isdir`, `getsize`.
- `os.makedirs(..., exist_ok=True)`, `os.listdir` (unordered), `os.rename`,
  `os.remove` (permanent).
- Walk a tree with `os.walk`: `root`, `dirs`, `files`.
- An environment variable is `os.environ.get(name, default)`; values are
  text.
