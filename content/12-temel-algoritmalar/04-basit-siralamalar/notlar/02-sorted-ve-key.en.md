## `sorted` or `list.sort`?

| | `sorted(items)` | `items.sort()` |
|---|---|---|
| Returns | a new list | `None` |
| The original list | unchanged | sorted in place |
| Accepts | any iterable (list, tuple, string, set…) | lists only |

A common mistake: writing `items = items.sort()`. Since `sort` returns
`None`, `items` becomes `None`.

## A key with `key=`

```python
people = [("Ada", 36), ("Bora", 25), ("Cem", 36)]

sorted(people, key=lambda p: p[1])          # by age
# [('Bora', 25), ('Ada', 36), ('Cem', 36)]

from operator import itemgetter
sorted(people, key=itemgetter(1))            # the same, without a lambda
```

The `key` function is called **once** per element; comparisons are made on
the keys.

## Sorting by several criteria

A tuple key is compared from left to right:

```python
sorted(people, key=lambda p: (p[1], p[0]))   # age first, then name if equal
# [('Bora', 25), ('Ada', 36), ('Cem', 36)]
```

If **one ascending and one descending** is wanted, negate the numeric
criterion:

```python
sorted(people, key=lambda p: (-p[1], p[0]))  # age high to low, name A-Z
# [('Ada', 36), ('Cem', 36), ('Bora', 25)]
```

A string criterion cannot be negated; then take advantage of stability and
do **two passes**: first sort by the second criterion, then by the first.

```python
step1 = sorted(people, key=lambda p: p[0], reverse=True)   # name Z-A
step2 = sorted(step1, key=lambda p: p[1])                  # age ascending
# [('Bora', 25), ('Cem', 36), ('Ada', 36)]
```

Because the second sort is stable, people of the same age keep the order of
the first pass (name Z-A).

## Upper and lower case

Strings are compared by character code: all capital letters come before
lowercase ones. For case-insensitive sorting, `key=str.lower`. (The correct
order of Turkish letters needs `locale` or a custom key; `"ç"` falls to the
end because its code is greater than `"z"`'s.)
