The same recipe for every new API response. You can copy and adapt the code.

## The recipe

```python
import csv

# 1) Open the envelope
items = response["data"]

# 2-5) A flat row from each record
rows = []
for item in items:
    author = item.get("author", {})
    rows.append({
        "id": item["id"],                                  # 2) chosen column
        "title": item.get("title", ""),
        "author_name": author.get("name", ""),             # 3) nested field
        "author_country": author.get("country", "unknown"),
        "tags": "|".join(item.get("tags", [])),            # 4) list → one cell
        "price": float(item["price"]),                     # 5) type fix
    })

# Write to a file
with open("books.csv", "w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
```

`writer.writerows(rows)` writes all rows at once; it is the short form of
calling `writerow` in a loop.

## List → separate rows

```python
pairs = []
for item in items:
    for tag in item.get("tags", []):
        pairs.append({"book_id": item["id"], "tag": tag})
```

Two nested loops: the outer one goes through the books, the inner one through
that book's tags.

## Checklist

- Under which key is the list of records? (`data`, `items`, `results`)
- Does `meta` / `total` say that I do not hold all of it?
- Is every field in every record? If not, `get` with a default.
- Lists: join them, or separate rows?
- Do numbers arrive as text?
- Are the column names consistent? (`author_name`, `author_country`)
