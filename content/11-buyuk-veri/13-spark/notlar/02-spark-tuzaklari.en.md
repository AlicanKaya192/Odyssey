Spark code usually runs; the trouble is slowness or the driver's memory.
Common mistakes.

## 1. `collect()` on a big result

`collect()` brings the whole result to the driver. With billions of rows the
driver crashes. Filter and summarise first; write a big result to disk
(`df.write.parquet(...)`), or look at only a few rows (`take(10)`, `show()`).

## 2. Adding up with `groupByKey`

```python
rdd.groupByKey().mapValues(sum)      # every value crosses the network
rdd.reduceByKey(lambda a, b: a + b)  # added up in the partition first
```

Both give the same result, but `reduceByKey` uses a combiner and sends far
less data over the network (Section 12: 32 pairs instead of a million).

## 3. Not caching an RDD used twice

Spark is lazy: if the same RDD is used in two actions, the recipe runs twice.
In this section's example, 6 partition computations with `cache()`, 12
without. Cache RDDs you will reuse and that are expensive to compute; let go
of them when you are done.

## 4. Needless shuffles

Every wide transformation is a shuffle. Use `distinct`, `sortBy` and
`groupBy` when really needed and as little as possible; filter **before** the
shuffle.

## 5. A skewed key

If one key carries most of the data (in Section 12, 66% of the orders on one
machine), that partition keeps everyone waiting. Consider salting or a
different key.

## 6. Too few or too many partitions

With fewer partitions than cores, cores sit idle; with too many, each
partition's preparation work grows (the small pieces in Section 3). The common
advice is a few times as many partitions as cores.

## 7. Calling an action in a loop

```python
for city in cities:
    df.filter(f"city == '{city}'").count()   # the whole plan runs every round
```

A single `groupBy("city").count()` is enough.

## 8. Forgetting laziness

A transformation line that raised no error is not shown to be right: the
error may only come at the action, much later. While writing, look often with
`take(5)` on a small sample.
