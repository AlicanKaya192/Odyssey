Write the function `most_frequent(items)`: it returns the most frequent value
and how many times it occurs as a `(value, count)` tuple. On a tie, the value
**seen first in the list** wins. `None` for an empty list.

- `["b", "a", "b", "c", "a"]` → `("b", 2)` (a is there twice too, but b was
  seen first)

Build a counter dictionary. Do not use `.count()`, `Counter` or `most_common`.
Since the dictionary keeps insertion order, choosing the **strictly greater**
one (`>`) while walking the counters keeps the first on a tie.

**Expected output:**

```
('b', 2)
(3, 3)
None
```
