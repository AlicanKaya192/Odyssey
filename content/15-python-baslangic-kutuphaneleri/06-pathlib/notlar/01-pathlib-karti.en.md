## Building

| Code | Result |
|---|---|
| `Path("data") / "sales.csv"` | a joined path |
| `Path.cwd()` | the working folder |
| `Path.home()` | the home folder |
| `Path(__file__).parent` | this file's folder |
| `p.resolve()` | the absolute path |

## Parts (no disk access)

| Attribute / method | For `Path("data/raw/sales.csv")` |
|---|---|
| `p.name` | `sales.csv` |
| `p.stem` | `sales` |
| `p.suffix` / `p.suffixes` | `.csv` / `['.csv']` |
| `p.parent` | `data/raw` |
| `p.parts` | `('data', 'raw', 'sales.csv')` |
| `p.with_suffix(".txt")` | `data/raw/sales.txt` |
| `p.with_stem("stock")` | `data/raw/stock.csv` |
| `p.as_posix()` | text with `/` |
| `p.relative_to("data")` | `raw/sales.csv` |

## Disk work

| Method | What it does |
|---|---|
| `p.exists()`, `is_file()`, `is_dir()` | does it exist, what is it |
| `p.read_text(encoding="utf-8")` | the whole content |
| `p.write_text(text, encoding="utf-8")` | writes (overwrites) |
| `p.read_bytes()`, `write_bytes()` | binary content |
| `p.mkdir(parents=True, exist_ok=True)` | a folder |
| `p.iterdir()` | the folder's contents |
| `p.glob("*.csv")` / `rglob("*.csv")` | search / with subfolders |
| `p.rename(new)` | rename, move |
| `p.unlink(missing_ok=True)` | delete the file |
| `p.rmdir()` | delete an empty folder |
| `p.stat().st_size` | bytes |

## Glob patterns

| Pattern | Matches |
|---|---|
| `*.csv` | the `.csv` files in this folder |
| `sales_*.csv` | the ones starting with `sales_` |
| `*/*.py` | the `.py` files in one subfolder |
| `**/*.py` | at every depth (same as `rglob("*.py")`) |
| `report_?.txt` | `?` is one character: `report_1.txt` |
