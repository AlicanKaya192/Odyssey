## Three non-comparison sorts

| | Counting | Radix | Bucket |
|---|---|---|---|
| Condition | integers, small range `k` | a fixed number of digits | values spread evenly over a range |
| Cost | `O(n + k)` | `O(d × (n + base))` | `O(n)` on average |
| Extra memory | `O(k)` | `O(n + base)` | `O(n)` |
| Stable? | the version writing values from counters carries no information beyond the value; a version sorting records is written stably | every round must be stable | depends on the sort inside the buckets |
| Example | exam scores, ages, hours (0–23) | postcodes, phone numbers, dates (YYYYMMDD) | random numbers between 0 and 1 |

## Negative values

If the range is `[min_value, max_value]`, shift the counter index:

```python
counts = [0] * (max_value - min_value + 1)
for x in items:
    counts[x - min_value] += 1
# when writing back: value = index + min_value
```

## Sorting records stably (not just numbers)

If `[name, grade]` records are to be sorted instead of numbers, counters are
not enough; either a **bucket list** is kept per grade (the order of
appending is preserved, so it is stable):

```python
def sort_by_grade(records, max_grade):
    buckets = [[] for _ in range(max_grade + 1)]
    for record in records:
        buckets[record[1]].append(record)
    return [r for bucket in buckets for r in bucket]
```

or each record's final place is computed from the counters' **prefix sums**
(we will see that method in the Prefix Sums section).

## When to go back to comparison sorting?

- If the range is much larger than `n` (`k >> n`)
- If the values are decimals or strings with no digit structure
- If a short list is being sorted: `sorted` is already fast and one line
