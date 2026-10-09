The idea of counting sort (using the value directly as an address) is used
every day in data work. Python has ready-made tools for it.

## Histogram: `collections.Counter`

```python
from collections import Counter

grades = ["B", "A", "C", "B", "B", "A"]
counts = Counter(grades)
print(counts["B"])               # 3
print(counts.most_common(2))     # [('B', 3), ('A', 2)]
```

A `Counter` is a dictionary; the range need not be limited, and the values
can be strings. Building it is `O(n)`.

## Grouping: `defaultdict(list)`

```python
from collections import defaultdict

students = [("Ada", "A"), ("Bora", "B"), ("Cem", "A"), ("Deniz", "C")]
by_grade = defaultdict(list)
for name, grade in students:
    by_grade[grade].append(name)
print(dict(by_grade))   # {'A': ['Ada', 'Cem'], 'B': ['Bora'], 'C': ['Deniz']}
```

Every group keeps the input order. Since the buckets live in a dictionary,
the keys need not be numbers in a small range.

## Careful: `itertools.groupby` wants sorted data

`groupby` only collects equal keys that stand **next to each other**. If the
data is not sorted, the same key comes out in several groups:

```python
from itertools import groupby

letters = ["a", "b", "a"]
print([key for key, _ in groupby(letters)])            # ['a', 'b', 'a']
print([key for key, _ in groupby(sorted(letters))])    # ['a', 'b']
```

For grouping unsorted data, `defaultdict` is safer and `O(n)`.

## The pandas equivalent

In the Data Science path, `value_counts()` is the table version of a
histogram and `groupby()` the table version of grouping with buckets; the
same hash and bucket idea runs inside them.
