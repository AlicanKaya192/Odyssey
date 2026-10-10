`report(rows)` counts how many times each distinct value appears, but for
every key it scans the whole list with `rows.count`: with 300,000 rows it
exceeds the time limit. Write a solution that produces the same dictionary
in **one pass** (`collections.Counter`). The expected output:

```
8000 38
```

**Expected output:**

```
8000 38
```
