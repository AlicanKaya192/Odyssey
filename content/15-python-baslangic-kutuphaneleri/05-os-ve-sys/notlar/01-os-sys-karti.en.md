## os.path

| Code | What it gives |
|---|---|
| `os.path.join("a", "b.txt")` | `a\b.txt` (Windows) / `a/b.txt` |
| `os.path.basename(p)` / `dirname(p)` | file name / folder |
| `os.path.splitext(p)` | `(name, last extension)` |
| `os.path.exists(p)` | does it exist |
| `os.path.isfile(p)` / `isdir(p)` | is it a file / a folder |
| `os.path.getsize(p)` | bytes |
| `os.path.abspath(p)` | the absolute path |
| `os.path.relpath(p, start)` | the path relative to `start` |

## os

| Code | What it does |
|---|---|
| `os.getcwd()` | the folder the program runs in |
| `os.listdir(d)` | the contents (unordered) |
| `os.makedirs(d, exist_ok=True)` | a folder + the ones in between |
| `os.mkdir(d)` | a single folder |
| `os.rename(old, new)` | rename / move |
| `os.remove(f)` | delete a file **permanently** |
| `os.rmdir(d)` | delete an **empty** folder |
| `os.walk(d)` | `(root, dirs, files)` along the tree |
| `os.environ.get(name, default)` | an environment variable (text) |
| `os.cpu_count()` | the number of cores |

To delete a folder with contents, use `shutil.rmtree` (two sections later).

## sys

| Code | What it gives |
|---|---|
| `sys.version_info >= (3, 10)` | a version check |
| `sys.platform` | `win32`, `linux`, `darwin` |
| `sys.argv` | command line arguments (the first is the script name) |
| `sys.path` | module search folders |
| `sys.executable` | the path of the running Python |
| `sys.exit(code_or_text)` | end the program |
| `print(..., file=sys.stderr)` | write to the error stream |

## Careful

- Do not glue paths with `+`; use `join`.
- `os.listdir` is unordered; sort with `sorted`.
- `os.remove` does not send to the recycle bin.
- Environment variables are text; convert numbers with `int`, yes/no with an
  explicit list.
