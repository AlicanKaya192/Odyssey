One of the most common small tools written with `pathlib` is a script that
tidies a messy folder: moving the files in the Downloads folder into
subfolders by type, for example. Code that moves files **is hard to undo if
it goes wrong**; that is why it is written with two habits.

## 1. A dry run first

The function first only **lists what it would do** and touches nothing; if
the list is right, it is really run.

```python
from pathlib import Path

inbox = Path("inbox")
inbox.mkdir()
names = ["photo.jpg", "report.pdf", "data.csv", "notes.txt", "scan.PDF", "README"]
for name in names:
    (inbox / name).write_text("x", encoding="utf-8")


def organize(folder, dry_run=True):
    moves = []
    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue
        kind = path.suffix.lower().lstrip(".") or "other"
        moves.append(f"{path.name} -> {kind}/")
        if not dry_run:
            (folder / kind).mkdir(exist_ok=True)
            path.rename(folder / kind / path.name)
    return moves


for line in organize(inbox):
    print(line)
organize(inbox, dry_run=False)
files = [p for p in inbox.rglob("*") if p.is_file()]
for name in sorted(p.relative_to(inbox).as_posix() for p in files):
    print(name)
```

```text
data.csv -> csv/
notes.txt -> txt/
photo.jpg -> jpg/
README -> other/
report.pdf -> pdf/
scan.PDF -> pdf/
csv/data.csv
jpg/photo.jpg
other/README
pdf/report.pdf
pdf/scan.PDF
txt/notes.txt
```

- `suffix.lower()`: `scan.PDF` and `report.pdf` went to the same folder.
- `"other"` for `README`, which has no extension: `suffix` is an empty
  string, so the `or` fallback kicks in.
- `lstrip(".")` drops the leading dot (`.pdf` → `pdf`).
- The first call only listed; the second (`dry_run=False`) moved.

## 2. Overwriting

If a file with the same name exists at the target, `rename` raises an error
on Windows but **silently overwrites** on Linux: the old file is lost. The
safe way is to find a free name:

```python
from pathlib import Path


def unique_path(path):
    candidate = path
    counter = 1
    while candidate.exists():
        candidate = path.with_stem(f"{path.stem}-{counter}")
        counter += 1
    return candidate


report = Path("report.txt")
report.write_text("v1", encoding="utf-8")
print(unique_path(report))
unique_path(report).write_text("v2", encoding="utf-8")
print(unique_path(report))
```

```text
report-1.txt
report-2.txt
```

`with_stem` changes the name and keeps the extension. While `report.txt`
exists, the free name is `report-1.txt`; once that is written too,
`report-2.txt`.

## Checklist

- A dry run first, then the real run.
- Create the target folder before moving (`mkdir(exist_ok=True)`).
- If the target name exists, find a new name; do not overwrite.
- Prefer moving to deleting (it can be brought back if wrong).
