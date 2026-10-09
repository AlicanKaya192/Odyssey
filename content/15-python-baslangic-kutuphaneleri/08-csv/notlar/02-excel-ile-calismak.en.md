If Turkish letters look broken when you open a Python-written CSV in Excel,
or the first column name of a file from Excel looks strange, the reason is
usually the same: the **BOM**.

## What is a BOM?

The **BOM** (byte order mark) is a three-byte mark some programs put at the
very start of a UTF-8 file: `EF BB BF`. Excel **recognises from this mark**
that a CSV is UTF-8; without it, Excel opens the file with Windows' old
encoding and letters like `ş`, `ğ`, `İ` break. In Python this marked encoding
is called **`utf-8-sig`**.

```python
import csv

with open("excel.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerows([["name", "score"], ["Ada", "9,5"]])
print(open("excel.csv", "rb").read()[:12])
with open("excel.csv", newline="", encoding="utf-8") as f:
    print(next(csv.reader(f, delimiter=";")))
with open("excel.csv", newline="", encoding="utf-8-sig") as f:
    print(next(csv.reader(f, delimiter=";")))
```

```text
b'\xef\xbb\xbfname;scor'
['\ufeffname', 'score']
['name', 'score']
```

- The first three bytes of the file are `\xef\xbb\xbf`: the BOM.
- Read with `utf-8`, the BOM stuck to the first column name: `'﻿name'`.
  On screen it looks like `name`, but `row["name"]` raises **`KeyError`**; one
  of the sneakiest CSV bugs.
- Read with `utf-8-sig`, the BOM was dropped. This encoding reads fine when
  there is no BOM too; a safe choice for files from Excel.

## Checklist for Excel

| Situation | What to do |
|---|---|
| A Python-written CSV will be opened in Excel | `encoding="utf-8-sig"` |
| Turkish/European Excel | `delimiter=";"`, decimal comma |
| Reading a CSV from Excel | `encoding="utf-8-sig"`, check the separator |
| The first column name does not match | suspect the BOM |
| Numbers come as text | `float(x.replace(",", "."))` |

## csv or pandas?

| | `csv` | pandas |
|---|---|---|
| Installation | none, standard | a separate package |
| Memory | reads row by row | loads the whole table |
| Type conversion | by hand | automatic |
| Calculations, grouping | by hand | one line |

`csv` for a small script, a tool with no installation, or processing a file
too big for memory row by row; pandas for analysis on a table.
