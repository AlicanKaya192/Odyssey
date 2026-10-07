Build an RDD with `minispark`, look at its partitions and do a calculation.

**What to do:**

1. The `SparkSession` and `sc` are ready in the starter code.
2. `nums = sc.parallelize(range(1, 21), 4)`.
3. Print the number of partitions.
4. Print the number of items in each partition as a list (`glom()` and
   `map(len)`).
5. Print the total of the squares of the even numbers: `filter`, `map`,
   `sum`.

**Expected output:**

```
4
[5, 5, 5, 5]
1540
```
