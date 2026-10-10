Three exam scores of five students sit in a matrix: rows are students,
columns exams. With this section's tools, the answers are one line each:

```python
import numpy as np

names = np.array(["ada", "alan", "grace", "linus", "guido"])
scores = np.array([[72, 88, 95], [55, 61, 70], [90, 94, 85],
                   [40, 75, 62], [83, 79, 91]])
passed_all = (scores >= 60).all(axis=1)
print(names[passed_all].tolist())
print(names[scores.argmax(axis=0)].tolist())
mean = scores.mean(axis=1)
print(names[np.argsort(mean)[::-1]][:3].tolist())
curved = np.where(scores < 60, 60, scores)
print(int(curved.sum() - scores.sum()))
ranks = np.argsort(np.argsort(-mean)) + 1
print(dict(zip(names.tolist(), ranks.tolist())))
```

```text
['ada', 'grace', 'guido']
['grace', 'grace', 'ada']
['grace', 'ada', 'guido']
25
{'ada': 2, 'alan': 4, 'grace': 1, 'linus': 5, 'guido': 3}
```

## Line by line

| Question | Code |
|---|---|
| Those who passed every exam | `names[...]` with the mask `(scores >= 60).all(axis=1)` |
| The top student of each exam | `scores.argmax(axis=0)` → the row of the largest in each column |
| The top three by average | `np.argsort(mean)[::-1][:3]` |
| Raising scores below 60 to 60 | `np.where(scores < 60, 60, scores)`; 25 points added |
| A rank number (1 = best) | `np.argsort(np.argsort(-mean)) + 1` |

## argsort twice

`argsort` once answers "which item is where in the sorted array"
(`[2, 0, 4, 1, 3]`: grace first, then ada...). A second `argsort` reverses
this: "what position each item has in the sorted array" (`ada` is at position
1, that is 2nd). The minus sign is for sorting largest first.

## Why no loop?

You could write the same questions with `for` loops; in NumPy each is a single
expression running at C speed. The gap grows with the data: with thousands of
students and hundreds of exams, a loop takes seconds, an array operation
milliseconds.
