## shutil

| Code | What it does |
|---|---|
| `shutil.copy(s, t)` | copies the file's content |
| `shutil.copy2(s, t)` | content + modification time |
| `shutil.copytree(s, t)` | copies a folder with its contents |
| `copytree(..., ignore=shutil.ignore_patterns("*.log"))` | what to skip |
| `copytree(..., dirs_exist_ok=True)` | over an existing folder |
| `shutil.move(s, t)` | moves a file or folder |
| `shutil.rmtree(s)` | deletes a folder **with its contents, permanently** |
| `shutil.disk_usage(path)` | `total`, `used`, `free` (bytes) |
| `shutil.which("git")` | a program's path, or `None` |

## glob

| Code | What it gives |
|---|---|
| `glob.glob("*.csv")` | the `.csv` paths in this folder (strings) |
| `glob.glob("data/**/*.csv", recursive=True)` | at every depth |
| `glob.glob("log_202?.txt")` | `?` is one character |
| `glob.glob("[!_]*.py")` | the ones not starting with `_` |
| `glob.escape(name)` | so `*`, `?`, `[` in a name are searched as letters |

## Which one?

| Job | The shortest way |
|---|---|
| Copy one file | `shutil.copy2` |
| Copy a folder | `shutil.copytree` |
| Move / rename | `shutil.move` or `Path.rename` |
| Delete a file | `Path.unlink` |
| Delete an empty folder | `Path.rmdir` |
| Delete a full folder | `shutil.rmtree` |
| Search with a pattern | `Path.glob` / `glob.glob` |

## Careful

- `copy` creates a **file** with that name if the target folder is missing.
- Print and check the path before `rmtree`.
- `glob.glob` is unordered; `sorted`.
