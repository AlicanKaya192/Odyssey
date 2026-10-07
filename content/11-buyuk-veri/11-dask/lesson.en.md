# dask

In Section 3 we split a file into pieces by hand, summarised each piece and
combined the summaries ourselves. In Section 10 we spread work over processes
and threads by hand. **dask** does both jobs at once, by itself, with a syntax
very much like pandas:

- It splits the table into **partitions**; each partition is an ordinary
  pandas table.
- It does not carry out your operations right away; it records them as a
  **task graph**.
- When you say `compute()`, it spreads the tasks over the cores, runs them and
  combines the results.

Since partitions can be processed one after another, dask can also work with
data bigger than its memory.

In the examples a million orders are split into four CSV files:
`orders-0.csv` … `orders-3.csv` (250 000 rows each).

## A dask table

```python
import dask.dataframe as dd

ddf = dd.read_csv("orders-*.csv")
print(ddf.npartitions)
print(ddf.dtypes)
```

```text
4
order_id         int64
order_time      string
customer_id      int64
city            string
category        string
quantity         int64
unit_price     float64
payment         string
dtype: object
```

- `"orders-*.csv"`: all four files with a wildcard; each file became a
  partition.
- The types are known but the data has not been read yet: dask only looked at
  the beginnings of the files to guess the types. If you wrote `print(ddf)`
  you would see `...` in place of the values; dask holds **the structure, not
  the data**.

## Lazy evaluation and `compute`

Let us write Section 3's revenue per city with dask:

```python
revenue = (ddf["quantity"] * ddf["unit_price"]).groupby(ddf["city"]).sum()
print(type(revenue).__name__)
result = revenue.compute()
print((result / 1e6).round(2).sort_values(ascending=False).head(3))
```

```text
Series
city
Istanbul    557.00
Ankara      260.83
Izmir       212.50
dtype: float64
```

The syntax is the same as pandas'. The difference: `revenue` is not a result
but a **recipe**; dask has not read a single row yet. `compute()` runs the
recipe and gives the result as an ordinary pandas object. The numbers are the
same as those we found by hand in Section 3 (Istanbul 557.00 million).

This laziness (*lazy evaluation*) is dask's strength: since it does not start
before seeing the whole job, it can skip needless reads and run independent
steps at the same time.

`head()` and `len()`, on the other hand, run right away: `head` reads only the
first rows of the first partition, `len` counts all the files.

## The task graph

When `compute()` is called, dask draws up a list of tasks: "read", "multiply",
"group and add up" for each partition, then "combine" for all of them.

<figure class="fig">
  <div class="flow">
    <span class="node">Read partitions<br>0 · 1 · 2 · 3</span><span class="arrow">→</span>
    <span class="node">Group and add up<br>in each partition</span><span class="arrow">→</span>
    <span class="node">Combine</span><span class="arrow">→</span>
    <span class="node acc">A pandas result</span>
  </div>
  <figcaption>The first two steps run separately for each partition and can run at the same time; combining happens when they have all finished.</figcaption>
</figure>

Let us split the million-order `orders` table in memory into eight
partitions and see how many tasks there are for the total quantity per
category:

```python
ddf8 = dd.from_pandas(orders, npartitions=8)
s = ddf8.groupby("category")["quantity"].sum()
print(len(s.__dask_graph__()))
```

```text
25
```

25 tasks. The independent ones (each of the eight partitions' own groups) can
run at the same time; the combining is done when they have all finished. The
same "summarise in the piece, combine the summaries" pattern from Section 3,
but dask builds it.

## Partitions

Each partition is processed as a pandas table in memory, so partition size
matters:

- `dd.read_csv`: each file is at least one partition; big files are cut with
  `blocksize=`.
- `dd.from_pandas(df, npartitions=8)`: splits a table in memory into eight.
- `dd.read_parquet`: in this version it read a single file as a single
  partition; with `split_row_groups=True` each row group became a separate
  partition (10 groups, 10 partitions).

Very small partitions (like the very small pieces in Section 3) multiply each
partition's preparation work; very big partitions may not fit in memory.
dask's own documentation suggests roughly a hundred megabytes per partition.

## Computing several results together

If you need two results from the same data, `compute`-ing them separately
means reading the files twice. `dask.compute` works out both in one go,
sharing the common steps:

```python
import dask

big = ddf[ddf["quantity"] >= 4]
by_category = big.groupby("category")["unit_price"].mean()
count = big.shape[0]
means, n = dask.compute(by_category, count)
print(n)
```

```text
222059
```

## Schedulers

The **scheduler** decides who runs the tasks:

| Scheduler | What it does | When |
|---|---|---|
| `"threads"` | With threads in one process | The default for dask tables; pandas and NumPy release the lock |
| `"processes"` | With separate processes | Work heavy on pure Python |
| `"synchronous"` | One by one, in order | For debugging |

Revenue per city from four CSVs on this computer:

| Way | Time |
|---|---|
| pandas (read the four files and join them) | 1.41 s |
| dask, `"threads"` | 0.98 s |
| dask, `"synchronous"` | 1.45 s |

dask running in sequence took as long as pandas; with threads it was 1.4 times
faster. The real gain here is less speed than **memory**: dask never took all
four files into memory at once.

## `dask.delayed`: making any function lazy

dask is not only for tables. `delayed` turns an ordinary Python function lazy
and parallel:

```python
import time
from dask import delayed

def slow_square(x):
    time.sleep(0.2)
    return x * x

parts = [delayed(slow_square)(i) for i in range(8)]
total = delayed(sum)(parts)
print(total.compute())
```

```text
140
```

- `delayed(slow_square)(i)` does not call the function; it records it as "to
  be called".
- `delayed(sum)(parts)` adds the last step that adds up the eight results.
- `compute()` ran the eight calls at the same time: 0.21 seconds. In sequence
  (`scheduler="synchronous"`) it took 1.61 seconds.

## `dask.bag`: for lists of records

For data that does not fit a table, such as JSON lines and log files, there is
`dask.bag`: it splits a list of records into partitions and runs operations
such as `map` and `filter` in parallel.

```python
import json
import dask.bag as db

if __name__ == "__main__":
    bag = db.read_text("orders.jsonl").map(json.loads)
    izmir = bag.filter(lambda r: r["city"] == "Izmir").count().compute()
```

**Careful:** `dask.bag`'s default scheduler is **processes**. The rule from
Section 10 applies here too: without `if __name__ == "__main__":` this code
failed on Windows with `RuntimeError` and `BrokenProcessPool` (tried).

## Differences from pandas

dask imitates pandas' syntax but cannot do everything the same way. Jobs that
need to see all the data at once are hard or approximate:

```python
ddf["unit_price"].median().compute()
# NotImplementedError: Dask doesn't implement an exact median in all cases ...
print(ddf["unit_price"].quantile(0.5).compute())
```

```text
449.72
```

The exact median is 449.05; dask's `quantile` result is 449.72 because it uses
an approximate method. The table from Section 3 holds here too: the median
cannot be found exactly from pieces.

In the same way, sorting the whole table (`sort_values`) or changing the
index (`set_index`) is expensive because it requires the data to move between
partitions (a *shuffle*).

## When dask?

- The data does not fit in memory but you want to work with **pandas
  syntax**.
- There are many files and you will apply the same operation to all of them.
- You have your own Python functions you want to run in parallel
  (`delayed`).

If the data fits comfortably in memory, pandas is simpler and usually fast
enough. If the job can be expressed in SQL, DuckDB is often faster. dask can
also run on a **cluster** of many computers; then the same code is spread over
machines instead of cores. That is the door to the world we will see with
Spark two sections from now.

## Summary

- dask splits a table into pandas partitions, records operations as a task
  graph and runs them in parallel with `compute()`.
- `dd.read_csv("orders-*.csv")`: each file is a partition; printing shows the
  structure, not the data.
- The result of `compute()` is a pandas object; `dask.compute(a, b)` works out
  two results with a shared read.
- Schedulers: `threads` (the default), `processes`, `synchronous`.
- `delayed` makes any function lazy and parallel; `dask.bag` is for lists of
  records, its default is processes, and `if __name__` is required.
- No exact median, `quantile` is approximate; sorting and changing the index
  are expensive.
