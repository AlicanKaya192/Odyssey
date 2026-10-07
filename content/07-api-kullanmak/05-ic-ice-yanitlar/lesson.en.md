# Turning Nested Responses into Tables

The point of pulling data from an API is very often to get a **table**: one
where every row is a record and every column a field, that you can open in
Excel, load into pandas and chart.

But APIs do not send data as tables. The response is nested: the records sit
inside a list, the list sits inside a dictionary, and the records themselves
hold more dictionaries and lists. In this section you will learn to turn
that tree into **flat rows**. That is exactly the bulk of the work a data
scientist does with APIs.

## A typical response

The response of a book API's `/books`:

```json
{
  "data": [
    {"id": 1, "title": "Emma", "price": "12.50",
     "author": {"name": "Austen", "country": "UK"}, "tags": ["classic", "novel"]},
    {"id": 2, "title": "Dune", "price": "9.99",
     "author": {"name": "Herbert"}, "tags": ["scifi"]},
    {"id": 3, "title": "Ulysses", "price": "15.00",
     "author": {"name": "Joyce", "country": "IE"}, "tags": []}
  ],
  "meta": {"page": 1, "per_page": 3, "total": 42}
}
```

Our target is this table:

```text
id  title    price  author_name  author_country  tags
1   Emma     12.5   Austen       UK              classic|novel
2   Dune     9.99   Herbert      unknown         scifi
3   Ulysses  15.0   Joyce        IE
```

We will walk the way there in five steps.

<figure class="fig">
  <div class="flow">
    <span class="node">1. Envelope</span><span class="arrow">→</span>
    <span class="node">2. Columns</span><span class="arrow">→</span>
    <span class="node">3. Flatten</span><span class="arrow">→</span>
    <span class="node">4. Lists</span><span class="arrow">→</span>
    <span class="node acc">5. Types</span>
  </div>
  <figcaption>Five steps from a nested response to a flat table. You follow the same order with every new API.</figcaption>
</figure>

## Step 1: Open the envelope

We can call the outermost dictionary of the response the **envelope**. The
records sit inside the envelope under one key; here, `data`. In other APIs it
may be `items`, `results`, `records` or `books`. You find out which from the
documentation or by looking at a response.

```python
items = response["data"]
print(len(items))              # 3
print(response["meta"]["total"])  # 42
```

The rest of the envelope is useful too: `meta` says "there are 42 books in
total and you are on page 1". So the 3 records you hold are not all of the
data. We will see how to fetch every page in Section 10.

## Step 2: Which columns do you want?

A record may have dozens of fields. Instead of pouring all of them into the
table, pick the ones you need. From every record you build a new, flat
dictionary:

```python
rows = []
for item in items:
    rows.append({"id": item["id"], "title": item["title"]})
```

`rows` is now **a list of dictionaries**: each dictionary a row, each key a
column. This is the most common form of a table in Python.

## Step 3: Flatten nested fields

The `author` field is itself a dictionary. You cannot put a dictionary in a
table cell; you pull its values out into separate columns. The column name is
built by joining the path: `author` + `name` → `author_name`.

```python
for item in items:
    author = item["author"]
    row = {
        "id": item["id"],
        "author_name": author["name"],
        "author_country": author.get("country", "unknown"),
    }
```

Herbert's record has no `country`. `author["country"]` would raise a
`KeyError` here; with `get` we put in a default value. The habit from the
previous section pays off: **do not trust an API to send every field in every
record.**

### Flattening at any depth

Nesting can go several levels deep (`author.address.city`). Instead of
writing each level by hand, you can write a small function that does the
same job for every nested dictionary:

```python
def flatten(obj, prefix=""):
    flat = {}
    for key, value in obj.items():
        name = prefix + key
        if isinstance(value, dict):
            flat.update(flatten(value, name + "_"))
        else:
            flat[name] = value
    return flat

print(flatten(items[0]))
# {'id': 1, 'title': 'Emma', 'price': '12.50', 'author_name': 'Austen',
#  'author_country': 'UK', 'tags': ['classic', 'novel']}
```

When the function meets a dictionary, it **calls itself** again for that
dictionary and puts `author_` in front of the names. A function calling
itself is called **recursion**. `isinstance(value, dict)` asks "is this value
a dictionary?". `update` adds the contents of one dictionary to another.

## Step 4: Decide what to do with lists

`tags` is a list. There are two ways to put it in a table, and which is right
depends on your question:

**a) Join it into one cell.** You keep one row per record:

```python
row["tags"] = "|".join(item["tags"])    # "classic|novel"
```

Choosing `|` rather than a comma as the separator avoids confusion later when
writing to CSV.

**b) Open a separate row for each item.** A book with two tags gets two rows:

```text
book_id  tag
1        classic
1        novel
2        scifi
```

This form makes questions such as "how many books have each tag?" easy to
answer by counting. Think of it as a separate table that holds the book–tag
**relationship** rather than the book itself. Ulysses, which has no tags,
does not appear in this table at all.

## Step 5: Fix the types

This API sends the price as text: `"12.50"`. You cannot add up text. Convert
to the right type while building the row:

```python
row["price"] = float(item["price"])
```

Type problems you will often meet in APIs:

- numbers arriving as text (`"12.50"`, `"42"`),
- dates arriving as text (`"2024-03-01T09:00:00Z"`; the Time Series path
  covers working with them),
- different spellings of an empty value (`null`, `""`, `"N/A"`).

## Writing the table to a file: `csv`

Python's built-in `csv` module can write a list of dictionaries straight to a
CSV file:

```python
import csv

with open("books.csv", "w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["id", "title", "price"])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
```

- `fieldnames` sets the order of the columns.
- `writeheader()` writes the column names on the first line.
- `newline=""` stops an extra blank line from appearing between rows on
  Windows.

## If you know pandas: `json_normalize`

If you have finished the Data Science path, pandas does most of this in one
line:

```python
import pandas as pd

df = pd.json_normalize(response["data"])
print(df)
```

```text
   id    title  price              tags author.name author.country
0   1     Emma  12.50  [classic, novel]      Austen             UK
1   2     Dune   9.99           [scifi]     Herbert            NaN
2   3  Ulysses  15.00                []       Joyce             IE
```

It flattens nested dictionaries into dotted column names (`author.name`) and
puts `NaN` in missing values. But it leaves the list (`tags`) as it is, and
the price is still text. So you still make the decisions of steps 4 and 5.
Knowing how to do it by hand lets you see what the tool does and what it does
not.

## Summary

- An API response is a tree; a table needs flat rows.
- **1.** Open the envelope: find the list of records (`data`, `items`,
  `results`...). Fields such as `meta` give the total and the page.
- **2.** Pick the columns you want; build a new flat dictionary from each
  record.
- **3.** Open nested dictionaries into columns by joining the path
  (`author_name`); use `get` for missing fields.
- **4.** Decide about lists: join them in one cell, or open a row per item.
- **5.** Fix the types: numbers that arrive as text become `float`/`int`.
- `csv.DictWriter` writes a list of dictionaries to CSV; in pandas,
  `json_normalize` does most of the flattening but makes none of the
  decisions.
