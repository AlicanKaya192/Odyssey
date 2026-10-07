Someone who knows pandas can write most things in dask straight away; these
are the places where they usually get stuck.

## 1. A "structure" comes back, not a result

`print(ddf)` or `print(ddf["unit_price"].mean())` prints a recipe, not a
value. For the value, `.compute()`.

## 2. Calling `compute` inside a loop

```python
for city in cities:
    # the files are read again every round
    ddf[ddf["city"] == city]["unit_price"].mean().compute()
```

Each `compute` runs the recipe from the start. Work it all out with a single
`groupby`, or collect the recipes and use a single `dask.compute(...)`.

## 3. No exact median

`median()` raised `NotImplementedError`; `quantile(0.5)` is an approximate
result (449.72; the real one is 449.05). If an exact median is required,
DuckDB's `median` function, or all of the data.

## 4. Sorting and changing the index are expensive

`sort_values` and `set_index` require the data to move between partitions.
Most analyses do not need them; if you do, do it once and keep the result as
Parquet.

## 5. `dask.bag` uses processes

Its default scheduler is processes; without `if __name__ == "__main__":` it
gives `RuntimeError` / `BrokenProcessPool` on Windows (tried).

## 6. The result may not fit in memory

`compute()` brings the result into memory as a pandas object. If a big
filtered table is `compute`d, memory fills up again. Write a big result
without taking it into memory: `ddf.to_parquet("out/")`.

## 7. Not thinking about the number of partitions

Very small partitions multiply the preparation work; very big ones do not fit
in memory. The dask documentation suggests roughly a hundred megabytes per
partition.

## 8. dask on small data

If the data fits comfortably in memory, dask's task graph is just extra work.
In this track's measurement dask running in sequence took as long as pandas;
the gain comes from the cores and from memory.
