The lines you will write most often with dask.

## Building a table

```python
import dask.dataframe as dd

ddf = dd.read_csv("orders-*.csv")                       # each file a partition
ddf = dd.read_csv("big.csv", blocksize="64MB")          # cut a big file
ddf = dd.read_parquet("orders.parquet", split_row_groups=True)
ddf = dd.from_pandas(df, npartitions=8)
```

## Looking

```python
ddf.npartitions          # number of partitions
ddf.dtypes               # types (without reading)
ddf.head()               # first rows of the first partition (runs at once)
len(ddf)                 # counts all the files (runs at once)
```

## Computing

```python
result = ddf.groupby("city")["unit_price"].mean()   # a recipe
result.compute()                                     # a pandas result

import dask
a, b = dask.compute(x, y)                            # two results, one shared read
```

## Partition by partition

```python
ddf.map_partitions(len).compute()                    # each partition's row count
ddf.map_partitions(lambda p: p[p["quantity"] >= 4])  # the same operation on each
```

## Scheduler

```python
result.compute(scheduler="threads")        # the default (tables)
result.compute(scheduler="processes")      # work heavy on pure Python
result.compute(scheduler="synchronous")    # for debugging
```

## `delayed`

```python
from dask import delayed

parts = [delayed(f)(i) for i in range(8)]
total = delayed(sum)(parts)
total.compute()
```

## `bag`

```python
import dask.bag as db

if __name__ == "__main__":                 # the default is processes
    bag = db.read_text("orders.jsonl").map(json.loads)
    bag.filter(lambda r: r["city"] == "Izmir").count().compute()
    bag.pluck("payment").frequencies().compute()
```

## This track's measurements

| Job | Time |
|---|---|
| 4 CSVs, revenue per city, pandas | 1.41 s |
| The same job, dask `threads` | 0.98 s |
| The same job, dask `synchronous` | 1.45 s |
| 8 × 0.2 s waits, `delayed` | 0.21 s |
| The same in sequence | 1.61 s |
