# shutil and glob

`os` and `pathlib` deal with a single file or folder: open, read, rename,
delete. To **copy**, to **move a whole folder** or to **delete a folder full
of files**, **`shutil`** (shell utilities) is used; it is Python's
counterpart of what `cp`, `mv` and `rm -r` do in a terminal. **`glob`** finds
files with patterns like `*.csv`. The small scripts that take backups,
prepare a release folder or move old logs to an archive are all written with
these two modules.

## Copying files

```python
import os
import shutil
from pathlib import Path

Path("report.txt").write_text("sales 120", encoding="utf-8")
Path("backup").mkdir()
print(shutil.copy("report.txt", "backup"))
print(shutil.copy2("report.txt", "backup/report-old.txt"))
print(sorted(p.name for p in Path("backup").iterdir()))
os.utime("report.txt", (1_700_000_000, 1_700_000_000))
shutil.copy("report.txt", "a.txt")
shutil.copy2("report.txt", "b.txt")
source_time = Path("report.txt").stat().st_mtime
copy_time = Path("a.txt").stat().st_mtime
copy2_time = Path("b.txt").stat().st_mtime
print(copy_time == source_time, copy2_time == source_time)
```

```text
backup\report.txt
backup/report-old.txt
['report-old.txt', 'report.txt']
False True
```

- **`shutil.copy(source, target)`**: if the target is a folder, the file is
  copied into it with the same name; if it is a file path, with that name. It
  returns the path of the new file.
- **`shutil.copy2`** does the same and also keeps the file's **modification
  time**. We moved the source's time into the past with `os.utime`: the copy
  made with `copy` got "now" as its time (`False`), the one from `copy2` kept
  the source's (`True`). For backups `copy2` is preferred; the "when did it
  last change" information is not lost.

## Folders: copytree, move, rmtree

```python
import shutil
from pathlib import Path

for name in ["app/main.py", "app/utils.py", "app/debug.log",
             "app/__pycache__/main.cpython-314.pyc", "app/data/config.json"]:
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x", encoding="utf-8")
skip = shutil.ignore_patterns("__pycache__", "*.log")
shutil.copytree("app", "release", ignore=skip)
files = Path("release").rglob("*")
print(sorted(p.relative_to("release").as_posix() for p in files))
Path("dist").mkdir()
print(shutil.move("release", "dist"))
shutil.rmtree("app")
print(Path("app").exists(), Path("dist/release/main.py").exists())
```

```text
['data', 'data/config.json', 'main.py', 'utils.py']
dist\release
False True
```

- **`copytree(source, target)`** copies a folder with everything in it.
  **`ignore=shutil.ignore_patterns(...)`** gives the names and patterns to
  skip: the cache folder and the log file did not go into the release folder.
- **`shutil.move`** moves a file or folder; if the target is an existing
  folder it moves into it and returns the new path. When moving to another
  disk it copies and then deletes.
- **`shutil.rmtree`** deletes a folder **with everything in it,
  permanently**. No recycle bin, no confirmation. An `rmtree` with a wrongly
  computed path can take a whole project folder away; printing and checking
  the path before deleting is a good habit.

## glob: finding files with a pattern

```python
import glob
from pathlib import Path

for name in ["data/sales_2024.csv", "data/sales_2025.csv", "data/stock.csv",
             "data/old/sales_2023.csv", "data/notes.txt"]:
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x", encoding="utf-8")
print(sorted(glob.glob("data/*.csv")))
for path in sorted(glob.glob("data/**/*.csv", recursive=True)):
    print(path)
print(sorted(glob.glob("data/sales_202?.csv")))
print(sorted(glob.glob("data/[!s]*")))
```

```text
['data\\sales_2024.csv', 'data\\sales_2025.csv', 'data\\stock.csv']
data\old\sales_2023.csv
data\sales_2024.csv
data\sales_2025.csv
data\stock.csv
['data\\sales_2024.csv', 'data\\sales_2025.csv']
['data\\notes.txt', 'data\\old']
```

| Pattern | Meaning |
|---|---|
| `*` | any number of characters (except `/`) |
| `?` | a single character |
| `[abc]` / `[!s]` | one of these characters / not `s` |
| `**` | folders at every depth (with `recursive=True`) |

`glob.glob` gives the matching paths as a **list of strings**, in no order;
`Path.glob` produces `Path` objects. The patterns are the same. `glob.glob`
is common in older code; in new code both are used.

`[!s]*` means "everything not starting with `s`": the `old` folder came along
with `notes.txt`, because the pattern only looks at the name.

## How much space is on the disk?

```python
import shutil

usage = shutil.disk_usage(".")
print(type(usage).__name__, usage._fields)
print(usage.free > 0)
```

```text
usage ('total', 'used', 'free')
True
```

`disk_usage` gives the total, used and free space in **bytes**; to convert to
gigabytes use `usage.free / 1024**3`. It is used to check whether there is
room before writing a large file or downloading a data set.

## Common mistakes

```python
import shutil
from pathlib import Path

Path("report.txt").write_text("sales 120", encoding="utf-8")
shutil.copy("report.txt", "archive")
print(Path("archive").is_file(), Path("archive").is_dir())
Path("site").mkdir()
try:
    shutil.copytree("site", "site")
except FileExistsError:
    print("FileExistsError")
shutil.copytree("site", "site-copy")
shutil.copytree("site", "site-copy", dirs_exist_ok=True)
print(Path("site-copy").is_dir())
```

```text
True False
FileExistsError
True
```

- With no `archive` folder, `copy("report.txt", "archive")` raised no error:
  it created **a file called `archive`**. If the target is a folder, create
  it first.
- `copytree` raises `FileExistsError` when the target folder exists; to copy
  over an existing folder use **`dirs_exist_ok=True`**.

## Summary

- `shutil.copy` (content), `copy2` (content + time), `copytree` (a folder,
  with `ignore` and `dirs_exist_ok`), `move`, `rmtree` (permanent!).
- `glob.glob(pattern)` gives a list of strings; `*`, `?`, `[...]`, `**` +
  `recursive=True`.
- `shutil.disk_usage(path)`: total, used, free (bytes).
- Make sure the target folder exists before copying; check the path before
  deleting.
