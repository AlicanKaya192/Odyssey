The lines you need to write and read partitioned data and to move around its
folders.

## Layout

```text
orders/
  month=2024-01/part-0.parquet
  month=2024-02/part-0.parquet
  ...
```

The folder name is `column=value`. The partition column is not inside the
file but in its name.

## Writing by hand

```python
from pathlib import Path

for month, part in df.groupby("month"):
    folder = Path("orders") / f"month={month}"
    folder.mkdir(parents=True, exist_ok=True)
    part.drop(columns="month").to_parquet(folder / "part-0.parquet", index=False)
```

## Reading by hand

```python
parts = []
for f in sorted(Path("orders").glob("month=*/*.parquet")):
    month = f.parent.name.split("=")[1]
    if month == "2024-03":                 # partition pruning
        p = pd.read_parquet(f)
        p["month"] = month                 # put the column back from the name
        parts.append(p)
result = pd.concat(parts, ignore_index=True)
```

## Letting pandas do it

```python
df.to_parquet("by_month", partition_cols=["month"], index=False)
pd.read_parquet("by_month")
pd.read_parquet("by_month", filters=[("month", "==", "2024-03")])
```

This needs `pyarrow.dataset` behind the scenes; without it, the by-hand
method.

## Folders with `pathlib`

| Code | What it does |
|---|---|
| `Path("orders") / "month=2024-03"` | Joins a path |
| `folder.mkdir(parents=True, exist_ok=True)` | Creates the folder; no error if it exists |
| `Path("orders").glob("month=*/*.parquet")` | Parquet files one level down |
| `Path("orders").rglob("*.parquet")` | Parquet files in all subfolders |
| `f.parent.name` | The name of the file's folder |
| `f.name` | The file's name |
| `f.stat().st_size` | The file's size, bytes |
| `f.as_posix()` | Writes the path with `/` |

## Bucketing

```python
df["bucket"] = df["customer_id"] % 8
for bucket, part in df.groupby("bucket"):
    ...
# customer 1234: only bucket 1234 % 8 = 2 is read
```

## Choosing a partition column

| Question | A good answer |
|---|---|
| Is it filtered on often? | Yes: time, country, source |
| How many different values does it have? | Dozens, at most a few thousand |
| How big will a partition be? | Tens to hundreds of MB in large systems |

This track's measurement (a million orders): 12 files by month is fine; 366
files by day, and reading all of them is fifteen times slower than one file.
