# pathlib

In the previous section we handled paths as text with the `os.path`
functions. **`pathlib`** does the same job with an **object**: a path is a
`Path` object; its name, extension and folder are its attributes; reading,
writing and listing are its methods. The code gets shorter and more readable;
it has been in the standard library since Python 3.4 and is the recommended
way in new code.

## Building a path and looking at its parts

```python
from pathlib import Path

path = Path("data") / "raw" / "sales.csv"
print(path, path.as_posix())
print(path.name, path.stem, path.suffix)
print(path.parent, path.parent.name, path.parts)
print(path.with_suffix(".parquet").name, path.with_name("stock.csv").as_posix())
print(Path("archive.tar.gz").suffixes)
```

```text
data\raw\sales.csv data/raw/sales.csv
sales.csv sales .csv
data\raw raw ('data', 'raw', 'sales.csv')
sales.parquet data/raw/stock.csv
['.tar', '.gz']
```

- A path is joined with the **`/` operator**: `Path("data") / "raw"`. You
  write it like this on Windows too; Python puts in the right separator (`\`)
  by itself. `as_posix()` writes it with `/` everywhere (so it looks the same
  in output, in a report, in a web address).
- **`name`** is the file name, **`stem`** the name without the extension,
  **`suffix`** the extension, **`suffixes`** all the extensions.
- **`parent`** is the folder one level up (also a `Path`), `parts` the tuple
  of parts.
- **`with_suffix`** and **`with_name`** return a **new** path with the
  extension or name changed; nothing changes on disk.

## Reading, writing, deleting

```python
from pathlib import Path

folder = Path("project") / "data"
folder.mkdir(parents=True, exist_ok=True)
notes = folder / "notes.txt"
notes.write_text("first line\nsecond line\n", encoding="utf-8")
print(notes.exists(), notes.is_file(), folder.is_dir())
print(notes.read_text(encoding="utf-8").splitlines())
print(len(notes.read_text(encoding="utf-8").splitlines()))
renamed = notes.rename(folder / "todo.txt")
print(renamed.name, notes.exists())
renamed.unlink()
print(sorted(p.name for p in folder.iterdir()))
```

```text
True True True
['first line', 'second line']
2
todo.txt False
[]
```

- `mkdir(parents=True, exist_ok=True)`: the counterpart of `os.makedirs`.
- **`write_text`** opens the file, writes and closes it; **`read_text`**
  gives the whole content as text. No need to write `with open(...)`. Ideal
  for small files; to read a very large file line by line you still use
  `open`.
- **`encoding="utf-8"`** is always written (the reason is below).
- `rename` returns the new path; the old path no longer exists. `unlink`
  deletes the file **permanently**.
- `iterdir()` gives the folder's contents as `Path` objects; here the folder
  ended up empty.

## Finding files: glob and rglob

```python
from pathlib import Path

for name in ["shop/main.py", "shop/data/sales.csv", "shop/data/stock.csv",
             "shop/data/old/sales-2025.csv", "shop/src/app.py"]:
    path = Path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x", encoding="utf-8")
shop = Path("shop")
print(sorted(p.name for p in shop.iterdir()))
print(sorted(p.name for p in (shop / "data").glob("*.csv")))
print(sorted(p.relative_to(shop).as_posix() for p in shop.rglob("*.csv")))
print(sorted(p.as_posix() for p in shop.glob("*/*.py")))
```

```text
['data', 'main.py', 'src']
['sales.csv', 'stock.csv']
['data/old/sales-2025.csv', 'data/sales.csv', 'data/stock.csv']
['shop/src/app.py']
```

- **`glob("*.csv")`** searches only that folder; `*` means "any name".
- **`rglob("*.csv")`** goes down into subfolders too (the short way of
  `os.walk`).
- `glob("*/*.py")` is the `.py` files inside one subfolder: `main.py` did not
  come because it is directly in `shop`.
- **`relative_to(shop)`** makes the path relative to `shop`.
- Results come in no order; `sorted` keeps the screen stable.

Where the file path is built you also see the `parent.mkdir(...)` pattern:
"get the folder ready before writing the file".

## Relative and absolute paths

```python
from pathlib import Path

relative = Path("data") / "sales.csv"
full = relative.resolve()
print(relative.is_absolute(), full.is_absolute())
print(full.name, full.parent.name, full.parent.parent == Path.cwd())
```

```text
False True
sales.csv data True
```

`Path("data/sales.csv")` is **relative**: to the folder the program runs in
(`Path.cwd()`). **`resolve()`** turns it into a full (absolute) path. The
home folder is `Path.home()` (`C:\Users\name` or `/home/name`); programs
often put their settings file there.

To find a data file next to the program's own file, wherever it is run from,
write `Path(__file__).parent / "data.csv"`: `__file__` is the path of the file
running right now.

## Common mistakes

```python
from pathlib import Path

city = Path("city.txt")
city.write_text("Istanbul, İzmir, Muğla", encoding="utf-8")
print(city.read_text(encoding="utf-8"))
print(city.read_text(encoding="cp1252"))
try:
    print(Path("data") + "/sales.csv")
except TypeError as error:
    print("TypeError:", error)
try:
    Path("missing.txt").unlink()
except FileNotFoundError:
    print("FileNotFoundError")
Path("missing.txt").unlink(missing_ok=True)
print("done")
```

```text
Istanbul, İzmir, Muğla
Istanbul, Ä°zmir, MuÄŸla
TypeError: unsupported operand type(s) for +: 'WindowsPath' and 'str'
FileNotFoundError
done
```

- **Encoding:** a file written as UTF-8 and read with another encoding broke
  the Turkish letters (`İ` → `Ä°`). Without `encoding`, Python uses the
  computer's default, and on Windows that is often not UTF-8: the same code
  works on your computer and breaks on someone else's. Write
  **`encoding="utf-8"`** both when writing and when reading.
- Text is not added to a `Path` with `+`; use `/`.
- Deleting a missing file raises an error; for "delete if it exists" use
  `unlink(missing_ok=True)`.

## os.path or pathlib?

| Job | `os.path` / `os` | `pathlib` |
|---|---|---|
| Joining | `os.path.join(a, b)` | `Path(a) / b` |
| Name, extension | `basename`, `splitext` | `.name`, `.stem`, `.suffix` |
| Folder | `os.path.dirname(p)` | `p.parent` |
| Exists | `os.path.exists(p)` | `p.exists()` |
| Create a folder | `os.makedirs(p, exist_ok=True)` | `p.mkdir(parents=True, exist_ok=True)` |
| Reading | `open(p).read()` | `p.read_text(encoding=...)` |
| Searching a tree | `os.walk` + `splitext` | `p.rglob("*.csv")` |

The two replace each other; functions like `open` and `pandas.read_csv` also
accept a `Path` object. Use `pathlib` in the code you write from now on.

## Summary

- A path is `Path("a") / "b"`; the parts are `name`, `stem`, `suffix`,
  `parent`.
- `with_suffix`, `with_name` make a new path; `as_posix()` uses `/`
  everywhere.
- `read_text` / `write_text` (always `encoding="utf-8"`), `mkdir`, `rename`,
  `unlink`.
- `iterdir`, `glob` (in that folder), `rglob` (in subfolders too),
  `relative_to`.
- `resolve()` gives the absolute path; `Path.cwd()`, `Path.home()`,
  `Path(__file__).parent`.
