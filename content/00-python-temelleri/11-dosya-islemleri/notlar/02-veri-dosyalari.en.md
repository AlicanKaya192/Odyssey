There is more than one way to keep data on disk. Knowing which to use when
will pay off once you move on to data science.

## Plain text

The simplest form: one record per line.

```
Ada
Alan
Grace
```

```python
with open("names.txt", encoding="utf-8") as file:
    names = file.read().splitlines()
```

Enough for a single list of one kind of thing. Not enough once you need more
than one field.

## CSV — comma-separated values

The most common format in data science. One record per line, fields separated
by commas, and usually a header on the first line:

```
name,city,score
Ada,London,90
Alan,London,70
Grace,New York,85
```

Reading it by hand is instructive:

```python
rows = []

with open("people.csv", encoding="utf-8") as file:
    lines = file.read().splitlines()

header = lines[0].split(",")

for line in lines[1:]:
    values = line.split(",")
    rows.append(dict(zip(header, values)))

print(rows[0])
```

```
{'name': 'Ada', 'city': 'London', 'score': '90'}
```

The result is `list[dict[str, str]]` — exactly the shape you decoded in the
annotations note.

**Watch out:** every value arrives as **text**. The `score` field is `"90"`,
which is not a number. If you are going to do arithmetic you have to convert:

```python
    row["score"] = int(row["score"])
```

### The `csv` module

Python's own module does this job more safely:

```python
import csv

with open("people.csv", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

print(rows[0])
```

Why safer? Because a field can contain **a comma inside it**:

```
name,note
Ada,"born in London, England"
```

If you `split(",")` by hand, that line breaks into three parts and the data is
corrupted. The `csv` module ignores commas inside quotes.

The `newline=""` argument stops line endings from being doubled on Windows;
it is always written together with `csv`.

## JSON — nested data

CSV is a flat table. When the data contains a list or another dictionary, CSV
is not enough. That is where JSON comes in:

```json
{
  "name": "Ada",
  "languages": ["Python", "SQL"],
  "scores": {"math": 90, "logic": 95}
}
```

```python
import json

with open("profile.json", encoding="utf-8") as file:
    profile = json.load(file)

print(profile["languages"][0])
print(profile["scores"]["math"])
```

```
Python
90
```

Writing is just as easy:

```python
with open("profile.json", "w", encoding="utf-8") as file:
    json.dump(profile, file, ensure_ascii=False, indent=2)
```

`ensure_ascii=False` keeps non-English letters readable; without it they are
written as escape sequences. `indent=2` makes the file readable by a person.

**How JSON maps onto Python:**

| JSON | Python |
|---|---|
| object `{}` | `dict` |
| array `[]` | `list` |
| string | `str` |
| number | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

## Which one should you pick?

| Format | When |
|---|---|
| Plain text | A single-column list, a log file |
| CSV | A flat table, many rows, numeric analysis |
| JSON | Nested structure, a config file, an API response |

In data science the split is roughly this: data usually arrives as **CSV**,
settings are kept as **JSON**, and logs are written as **plain text**.

## One warning

In this section you read files by hand. On the Data Science path you will meet
the `read_csv` function in pandas, which does the same job in one line:

```python
table = pandas.read_csv("people.csv")
```

You may then wonder why you learned to do it by hand. The answer: the day
`read_csv` raises an error on a broken row, what you learned here is the only
reason you will understand what happened.
