Partitioning mistakes often do not show at once: the code runs, the result
comes out wrong or slow.

## 1. Splitting too finely

Reading 366 day files was fifteen times slower than one file. Splitting by
customer means 245 461 folders. Choose a column with few values; for a column
with many values, use buckets.

## 2. Writing months without a leading zero

Folder names are compared as text:

```python
"2024-10" < "2024-9"     # True
"2024-10" < "2024-09"    # False
```

Text comparison goes character by character, and `1` comes before `9`. Always
write the month with two digits: `strftime("%Y-%m")` does it by itself.

## 3. Forgetting `exist_ok=True`

```python
folder.mkdir(parents=True)          # FileExistsError if the folder exists
folder.mkdir(parents=True, exist_ok=True)
```

On the second run the folder already exists; without `exist_ok=True` the code
fails.

## 4. Keeping the partition column both in the name and in the file

If you also write the column into the file there are two sources, and when one
changes (renaming the folder, for example) they no longer agree. Drop the
partition column from the file (`drop(columns=...)`) and put it back from the
name when reading.

## 5. Forgetting the type of a column rebuilt from the name

A value from a folder name is **text**: `"2024-03"`. If you need a number or
a date, convert it (`int(...)`, `pd.to_datetime(...)`). When reading with
`partition_cols`, pandas makes this column a `category`.

## 6. Rewriting everything for new data

When a new month arrives, deleting all the folders and writing from scratch
is needless; just add the new month's folder. If an old month needs fixing,
rewrite only that folder.

## 7. Writing to the same folder twice and forgetting the old file

`partition_cols` creates new randomly named files on every write. If you write
the same data to the same folder a second time the old files stay too, and
every row comes back twice when read. Clear the old folder before rewriting.

## 8. `/` or odd characters in a partition value

A value such as `category=home/garden` splits the folder path. Keep partition
values plain (letters, digits, `-`, `_`).
