# How Spark Works

At the end of the last section we saw MapReduce's two limits: every step
writes to disk, and turning everything into map and reduce is tedious.
**Apache Spark** was born as an answer to these two problems (it started at
Berkeley in 2009 and later moved to Apache). Today it is the most common tool
for processing big data on clusters.

Spark has two big ideas:

1. **Keeping intermediate results in memory.** Jobs that go over the data
   again and again (such as machine learning) do not go back and forth to
   disk on every round.
2. **A rich, lazy language.** There are many more operations than `map` and
   `reduce`; all of them are first recorded as a plan, and the work starts
   only when a result is asked for.

## Real Spark and this section

Real Spark runs on a cluster and needs **Java**. To use it from Python there
is the `pyspark` package; installing it requires installing Java (a JDK) on
the computer first. So that Odyssey's exercises run without installing
anything on your computer, this section uses a small simulator called
**`minispark`**: it sits in the exercises as a read-only tab.

`minispark` runs in a single Python process but carries Spark's **names and
ideas** exactly: partitions, lazy transformations, actions, lineage, caching,
shuffles, DataFrames and SQL. The code you write here also runs on real
PySpark, with a few small differences.

## Getting started: SparkSession

```python
from minispark import SparkSession

spark = SparkSession.builder.appName("orders").getOrCreate()
sc = spark.sparkContext
```

- `SparkSession`: the entrance to Spark. In real Spark it also sets up the
  connection to the cluster.
- `sparkContext` (`sc` for short): the entrance to the lower-level world of
  RDDs.

## RDD: a collection split into partitions

Spark's basic structure is the **RDD** (*Resilient Distributed Dataset*): an
unchangeable collection of items split into partitions.

```python
nums = sc.parallelize(range(10), 3)
print(nums.getNumPartitions())
print(nums.glom().collect())
```

```text
3
[[0, 1, 2], [3, 4, 5], [6, 7, 8, 9]]
```

`parallelize` spread a Python collection over three partitions. `glom` makes
each partition a list, so we can see inside the partitions. On a real cluster
each partition could live on a different machine.

## Transformations and actions

Operations in Spark come in two kinds:

<figure class="fig">
  <div class="versus">
    <div><h4>Transformation (lazy)</h4><p><code>map</code>, <code>filter</code>, <code>flatMap</code><br><code>reduceByKey</code>, <code>distinct</code><br>Describes a new RDD<br>Computes nothing</p></div>
    <div class="ok"><h4>Action</h4><p><code>collect</code>, <code>count</code>, <code>take</code><br><code>sum</code>, <code>reduce</code><br>Asks for a result<br>Runs the whole recipe</p></div>
  </div>
  <figcaption>Transformations are chained; the work starts only when an action comes.</figcaption>
</figure>

- **Transformations** describe a new RDD but **compute nothing**: `map`,
  `filter`, `flatMap`, `reduceByKey`, `distinct`…
- **Actions** ask for a result and trigger the whole recipe to run:
  `collect`, `count`, `take`, `sum`, `reduce`…

`minispark`'s `sc.stats` counter lets us see this. Section 12's word count, in
Spark:

```python
lines = sc.parallelize(["the cat sat", "the dog sat", "the cat ran"], 2)
counts = (lines.flatMap(lambda line: line.split())
               .map(lambda word: (word, 1))
               .reduceByKey(lambda a, b: a + b))
print(sc.stats.jobs, sc.stats.partitions_computed)
print(sorted(counts.collect()))
print(sc.stats.jobs, sc.stats.partitions_computed, sc.stats.shuffles)
```

```text
0 0
[('cat', 2), ('dog', 1), ('ran', 1), ('sat', 2), ('the', 3)]
1 8 1
```

- After three transformations both the number of jobs and the number of
  partitions computed are **0**: Spark only wrote a recipe.
- `collect()` is an action: the recipe ran. 1 job, 8 partition computations
  (four steps × two partitions) and 1 shuffle.

The map, shuffle and reduce we wrote as three separate steps in Section 12 are
three lines here: `flatMap` + `map` are the map step, `reduceByKey` is both
the shuffle and the reduce. `reduceByKey` also applies the combiner itself:
first a local total in each partition, then the shuffle.

## Lineage and resilience

Every RDD knows where it came from, that is, the steps that produce it:

```python
print(counts.toDebugString())
```

```text
+- reduceByKey (shuffle)
  +- map
    +- flatMap
      +- parallelize
```

This lineage is the secret of Spark's resilience (the *Resilient* in its
name). If a machine breaks and a partition is lost, Spark does not read the
data from a backup; it works that partition out again by **re-running** the
steps in its lineage. Since transformations have no side effects, the same
result comes out.

## Narrow and wide transformations

Notice the `(shuffle)` mark in the lineage:

- **Narrow transformation:** each partition is worked out from its own data
  only. `map`, `filter`, `flatMap`. No data moves between machines; cheap.
- **Wide transformation:** a partition's result depends on the data of many
  partitions. `reduceByKey`, `groupByKey`, `distinct`, `sortBy`. It needs a
  **shuffle**: data moves between machines over the network; expensive.

Spark splits a job into **stages** at the shuffles; the narrow transformations
inside a stage pass the data along one after another in memory. Good Spark
code keeps the number of shuffles low. For example, `groupByKey` carries every
value over the network, while `reduceByKey` combines inside the partition
first and sends far less data (the combiner from Section 12).

## Caching: not computing the same data twice

If you use an RDD in two actions, Spark runs the recipe **twice**, since it is
lazy. `cache()` tells it to keep the result in memory the first time it is
computed:

```python
squares = nums.map(lambda x: x * x).cache()
before = sc.stats.partitions_computed
squares.count()
squares.sum()
print(sc.stats.partitions_computed - before)
```

```text
6
```

The two actions made 6 partition computations in all: `count` computed the
three partitions of the two steps, `sum` read from the cache. Without
`cache()`, `sum` would have computed them all again: 12. This is why Spark is
many times faster than MapReduce at machine learning: an algorithm that goes
over the data again and again reads it from the cache on every round.

## DataFrame: tables and a plan

RDDs are flexible but low level. Everyday work uses Spark's **DataFrame**: a
table with columns, as in pandas, but split into partitions and lazy.

```python
from orders_data import make_orders

df = spark.createDataFrame(make_orders(100_000), numPartitions=4)
big = df.withColumn("revenue", "quantity * unit_price").filter("quantity >= 4")
summary = big.groupBy("city").agg({"revenue": "sum", "order_id": "count"}).orderBy("city")
summary.show()
```

```text
    city  sum(revenue)  count(order_id)
   Adana    4784431.21             1518
  Ankara   11477315.59             3587
 Antalya    6671726.14             2064
   Bursa    6461439.90             1997
Istanbul   24791508.41             7554
   Izmir    9588024.17             2873
   Konya    5142625.90             1538
 Trabzon    3496253.54             1045
```

- `withColumn` is a new column, `filter` filtering, `groupBy(...).agg(...)`
  grouping: all transformations, all lazy.
- `show()` is an action: the plan ran now.

(In real PySpark conditions are often written with column objects:
`df.filter(df.quantity >= 4)`. `minispark` takes them as text.)

To see the plan, `explain()`:

```python
summary.explain()
```

```text
+- orderBy(city) (shuffle)
  +- groupBy(city).agg({'revenue': 'sum', 'order_id': 'count'}) (shuffle)
    +- filter(quantity >= 4)
      +- withColumn(revenue = quantity * unit_price)
        +- createDataFrame(4 partitions)
```

Real Spark **improves** the plan before running it (with an optimiser called
Catalyst): it moves filtering right next to the reading, reads only the
columns needed and reorders joins. The column selection and skipping by
statistics in Parquet (Section 5) happen in Spark by themselves too.

## Spark SQL

You can also give a DataFrame a name and query it with SQL:

```python
df.createOrReplaceTempView("orders")
spark.sql("""
    SELECT payment, count(*) AS n
    FROM orders
    GROUP BY payment
    ORDER BY n DESC
""").show()
```

```text
 payment     n
    card 72243
transfer 19885
    cash  7872
```

DataFrame syntax and SQL turn into the same plan; write whichever you find
more readable. (`minispark` runs SQL with DuckDB behind the scenes; real Spark
has its own SQL engine.)

## Spark on a cluster

<figure class="fig">
  <div class="flow">
    <span class="node acc">Driver<br>plan, tasks</span><span class="arrow">→</span>
    <span class="node">Cluster manager<br>machines, memory</span><span class="arrow">→</span>
    <span class="node">Executors<br>process partitions</span>
  </div>
  <figcaption>The driver is your program; the executors process partitions on the cluster's machines and keep the cache.</figcaption>
</figure>

- **Driver:** your program; it builds the plan, hands out the tasks and
  gathers the results.
- **Executors:** workers running on the machines in the cluster; each
  processes partitions and keeps the cache.
- **Cluster manager:** hands machines and memory to jobs (YARN, Kubernetes
  or Spark's own manager).

`collect()` brings the whole result to the driver; if the result is big, the
driver's memory fills up. A big result is written to disk
(`df.write.parquet(...)`), not brought to the driver. This is the cluster
counterpart of Section 8's rule "do not take a big result into pandas".

## Spark, dask, DuckDB: which one?

| Situation | Suitable tool |
|---|---|
| One machine, SQL on files | DuckDB |
| One machine, pandas syntax, bigger than memory | dask |
| Many machines, terabytes, a company cluster | Spark |
| Many machines, Python-heavy work | dask (distributed) or Spark |

For most analysis one powerful machine and the right tool (Parquet + DuckDB)
is enough. Spark comes to the fore when the data really outgrows one machine
and there is already a cluster.

## Summary

- Spark keeps intermediate results in memory and offers a rich, lazy
  language; an answer to MapReduce's two limits.
- RDD: an unchangeable collection split into partitions. Transformations are
  lazy, actions run them.
- Lineage: a lost partition is worked out again by re-running the steps.
- A narrow transformation stays inside the partition, a wide one needs a
  shuffle; `reduceByKey` is cheaper than `groupByKey`.
- `cache()` stops the same RDD being computed twice (6 partition computations
  instead of 12 in this example).
- DataFrames and Spark SQL turn into the same plan; `explain()` shows the
  plan.
- On a cluster, a driver and executors; `collect()` brings the result to the
  driver, and a big result is written to disk.
