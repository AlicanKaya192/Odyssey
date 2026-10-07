Everything you need to estimate on paper how much room a table will take is
on this page. An estimate is a good start; for the exact number, still
measure with `memory_usage(deep=True)`.

## Units

| Unit | Bytes | In Python |
|---|---|---|
| 1 KB | 1 024 | `1024` |
| 1 MB | 1 048 576 | `1024**2` |
| 1 GB | 1 073 741 824 | `1024**3` |
| 1 TB | 1 099 511 627 776 | `1024**4` |

From bytes to megabytes: `bytes / 1024**2`. From gigabytes to bytes:
`gb * 1024**3`.

Disk makers count 1 GB = 10⁹ bytes; that is why a "1 TB" disk shows up as
931 GB in Windows.

## How many bytes is one value?

| Type | Bytes | Can hold |
|---|---|---|
| `bool` | 1 | `True` / `False` |
| `int8` | 1 | -128 … 127 |
| `uint8` | 1 | 0 … 255 |
| `int16` | 2 | -32 768 … 32 767 |
| `int32` | 4 | about ±2.1 billion |
| `int64` | 8 | about ±9.2 × 10¹⁸ |
| `float32` | 4 | about 7 digits of precision |
| `float64` | 8 | about 15–16 digits of precision |
| `datetime64[ns]` | 8 | date-time to the nanosecond |

When pandas reads a CSV it makes whole numbers `int64` and decimals
`float64`. Moving to smaller types is the subject of Section 2.

**Text has no fixed width.** Each cell takes as much room as the text is
long, so you can only know the size of a text column by measuring.

## Quick estimate

```text
size (bytes) ≈ rows × numeric columns × 8
```

| Rows | Numeric columns | About |
|---|---|---|
| 1 million | 10 | 76 MB |
| 10 million | 6 | 458 MB |
| 100 million | 10 | 7.5 GB |
| 1 billion | 6 | 44.7 GB |

Text columns come on top of this.

## To measure

```python
import os

os.path.getsize("orders.csv")             # a file, bytes
df.memory_usage(deep=True)                # column by column, bytes
df.memory_usage(deep=True).sum()          # the table, bytes
array.nbytes                              # a NumPy array, bytes
```

## This track's measurements (1 million orders)

| | Size |
|---|---|
| CSV file | 61.1 MB |
| pandas 3, `str` text | 95.9 MB |
| old `object` text | 252.3 MB |
| 1 million numbers, Python list | 34.3 MB |
| 1 million numbers, NumPy array | 7.6 MB |
