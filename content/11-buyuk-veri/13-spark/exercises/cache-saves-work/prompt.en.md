Use the same RDD in two actions; compare the number of partitions computed
with and without the cache.

**What to do:**

1. `nums = sc.parallelize(range(1_000), 4)`.
2. Without a cache: `plain = nums.map(lambda x: x * 2)`. Take the counter
   into a variable, call `plain.count()` and `plain.sum()`, and print the
   increase in the counter.
3. With a cache: `cached = nums.map(lambda x: x * 2).cache()`. Do the same and
   print the increase.
4. Print whether the two `sum` results are the same.

**Expected output:**

```
16
8
True
```
