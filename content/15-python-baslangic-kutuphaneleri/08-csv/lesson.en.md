# csv

**CSV** (comma-separated values) is the most common data file format: every
line is a record, values are separated by commas, and the first line is
usually the column names. Most data downloaded from Excel, a database or a
website comes as CSV. The **`csv`** module in Python's standard library reads
and writes these files safely. pandas exists for bigger jobs (in the Data
Science path); but in a small script, somewhere pandas is not installed, or
when rows must be processed one by one, `csv` is enough.

The code blocks in this section continue one another: a file written in one
block is read in the next.

## Why split(",") is not enough

```python
import csv
from pathlib import Path

Path("one.csv").write_text('Ada,"London, UK",36\n', encoding="utf-8")
line = Path("one.csv").read_text(encoding="utf-8").strip()
print(line.split(","))
with open("one.csv", newline="", encoding="utf-8") as f:
    print(next(csv.reader(f)))
```

```text
['Ada', '"London', ' UK"', '36']
['Ada', 'London, UK', '36']
```

When a value contains a comma (`London, UK`), the value is put **in
quotes**. `split(",")` knows nothing about quotes: it split three values into
four pieces and the quotes stayed in the values. `csv.reader` knows the
rules: three values, without quotes.

## Writing: csv.writer

```python
import csv

rows = [
    ["name", "city", "age"],
    ["Ada", "London, UK", 36],
    ["Alan", "Wilmslow", 41],
    ['Grace "Amazing"', "New York", 85],
]
with open("people.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)
with open("people.csv", encoding="utf-8") as f:
    print(f.read())
```

```text
name,city,age
Ada,"London, UK",36
Alan,Wilmslow,41
"Grace ""Amazing""",New York,85
```

- `writerows` writes a list of lists, `writerow` a single row.
- The writer put the value with a comma in quotes **by itself**; in the value
  containing quotes it **doubled** the quotes (`""Amazing""`). Had we written
  `",".join(...)` by hand, these rules would break.
- Numbers (`36`) were turned into text and written.
- **`newline=""`** is always given; the reason is in the common mistakes part.

## Reading: csv.reader

```python
with open("people.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)
print(header)
for row in rows:
    print(row)
print(rows[0][2] + rows[1][2], int(rows[0][2]) + int(rows[1][2]))
```

```text
['name', 'city', 'age']
['Ada', 'London, UK', '36']
['Alan', 'Wilmslow', '41']
['Grace "Amazing"', 'New York', '85']
3641 77
```

- `csv.reader` gives every line as a **list**; `next(reader)` takes the
  first line (the header) apart.
- **All values are text**: `"36" + "41"` is gluing, not adding (`3641`).
  Use `int(...)` or `float(...)` before calculating with numbers.
- The file must be read inside the `with` block; when the block ends the file
  closes and the `reader` can no longer read. `list(reader)` collected the
  rows inside the block.

## By column name: DictReader and DictWriter

Reading a row by position like `row[2]` breaks when the columns move.
**`DictReader`** turns every row into a **dictionary** with the names in the
header:

```python
with open("people.csv", newline="", encoding="utf-8") as f:
    people = list(csv.DictReader(f))
print(people[0])
print(sum(int(p["age"]) for p in people) / len(people))
with open("seniors.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"], extrasaction="ignore")
    writer.writeheader()
    writer.writerows(p for p in people if int(p["age"]) > 40)
with open("seniors.csv", encoding="utf-8") as f:
    print(f.read())
```

```text
{'name': 'Ada', 'city': 'London, UK', 'age': '36'}
54.0
name,age
Alan,41
"Grace ""Amazing""",85
```

- `p["age"]` works even if the column moves; the code is more readable too.
- **`DictWriter`** writes dictionaries: `fieldnames` says which columns are
  written and in which order, `writeheader()` writes the header line.
- If a dictionary has a key not in `fieldnames` (`city`), `DictWriter`
  raises an error; **`extrasaction="ignore"`** skips the extra.

## Semicolons and decimal commas

Because the decimal separator is a comma in Turkish and many European
languages, Excel writes CSV with **semicolons** in these regions, so that a
price like `3,50` is not confused with the column separator.

```python
from pathlib import Path

text = "product;price\npen;3,50\nbook;12,90\n"
Path("prices.csv").write_text(text, encoding="utf-8")
with open("prices.csv", newline="", encoding="utf-8") as f:
    prices = list(csv.DictReader(f, delimiter=";"))
print(prices)
print(round(sum(float(p["price"].replace(",", ".")) for p in prices), 2))
```

```text
[{'product': 'pen', 'price': '3,50'}, {'product': 'book', 'price': '12,90'}]
16.4
```

`delimiter=";"` changes the separator. `float("3,50")` raises an error;
because the decimal separator in Python is a dot, first `replace(",", ".")`.

## A common mistake: forgetting newline=""

```python
with open("broken.csv", "w", encoding="utf-8") as f:
    csv.writer(f).writerows([["a", "b"], [1, 2]])
print(Path("broken.csv").read_bytes())
with open("fixed.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows([["a", "b"], [1, 2]])
print(Path("fixed.csv").read_bytes())
```

```text
b'a,b\r\r\n1,2\r\r\n'
b'a,b\r\n1,2\r\n'
```

The `csv` writer writes the line ending itself (`\r\n`). Without
`newline=""`, Windows text mode turns `\n` into `\r\n` once more and lines
end with `\r\r\n`: the file opens in Excel **with blank lines between the
rows**. Give `newline=""` when reading too; values containing a line break
inside quotes are only read correctly this way.

## Summary

- Read and write CSV with the `csv` module, not `split(",")`; it knows the
  quoting rules.
- Always `open(..., newline="", encoding="utf-8")`.
- `csv.reader` / `csv.writer` with lists, `DictReader` / `DictWriter` with
  dictionaries; `writeheader()`, `extrasaction="ignore"`.
- Every value read is text: convert with `int`, `float`.
- European Excel: `delimiter=";"` and decimal commas
  (`replace(",", ".")`).
