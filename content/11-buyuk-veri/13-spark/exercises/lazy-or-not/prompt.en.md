Show with the counter that transformations compute nothing and an action
runs everything.

**What to do:**

1. `nums = sc.parallelize(range(100), 5)`.
2. Chain three transformations: `map(lambda x: x * 3)`,
   `filter(lambda x: x % 2 == 0)`, `map(lambda x: x + 1)`; keep the result as
   `result`.
3. Print `sc.stats.jobs` and `sc.stats.partitions_computed` on one line.
4. Print the result of `result.count()`.
5. Print the same two counters again on one line.

**Expected output:**

```
0 0
50
1 20
```

Zero jobs before the action; afterwards one job and five partitions of each
of the four steps.
