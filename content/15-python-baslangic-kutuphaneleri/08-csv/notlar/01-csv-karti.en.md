## Opening

```python
open("data.csv", newline="", encoding="utf-8")          # reading
open("data.csv", "w", newline="", encoding="utf-8")     # writing
open("data.csv", newline="", encoding="utf-8-sig")      # from Excel
```

## Reading

| Code | What it gives |
|---|---|
| `csv.reader(f)` | every row as a list |
| `next(reader)` | the next row (to take the header apart) |
| `csv.DictReader(f)` | every row as a dictionary (header as keys) |
| `reader.fieldnames` | the column names in a `DictReader` |
| `csv.reader(f, delimiter=";")` | a semicolon-separated file |

## Writing

| Code | What it does |
|---|---|
| `csv.writer(f).writerow(list)` | one row |
| `writer.writerows(lists)` | many rows |
| `csv.DictWriter(f, fieldnames=[...])` | writes dictionaries |
| `writer.writeheader()` | the header row |
| `extrasaction="ignore"` | skip extra keys |
| `quoting=csv.QUOTE_ALL` | quote every value |

## Rules

- A value containing a comma, a quote or a line break is quoted; quotes are
  doubled (`""`). `csv` does this by itself.
- Every value read is **text**; convert with `int`, `float`.
- An empty cell comes as `""`; `int("")` raises an error, check first.
- Forgetting `newline=""` gives blank lines between rows on Windows.
