# operator and Sorting

Sorting is in every program: the best-selling products, the newest records,
people by name. You know how to sort a simple list with `sorted`. This
section answers the questions of real data: sorting dictionaries by a field,
by several fields, one ascending and one descending, ignoring upper and lower
case; taking only the first few; adding to a sorted list without breaking
the order. The tools are `sorted`'s `key` parameter, the **`operator`**
module, **`heapq`** and **`bisect`**.

## sorted and list.sort

```python
nums = [5, 2, 9, 1]
result = sorted(nums)
print(result, nums)
print(nums.sort(), nums)
print(sorted("banana"), sorted({"b": 1, "a": 2}))
```

```text
[1, 2, 5, 9] [5, 2, 9, 1]
None [1, 2, 5, 9]
['a', 'a', 'a', 'b', 'n', 'n'] ['a', 'b']
```

- **`sorted(x)`** returns a new list and does not touch the original; it
  takes anything iterable (a string letter by letter, a dictionary by its
  keys).
- **`list.sort()`** sorts the list **in place** and returns `None`: writing
  `x = x.sort()` loses the list.

## key: by what?

```python
words = ["banana", "Cherry", "apple", "Date"]
print(sorted(words))
print(sorted(words, key=str.casefold))
print(sorted(words, key=len, reverse=True))
people = [{"name": "Ada", "age": 36}, {"name": "Alan", "age": 41},
          {"name": "Grace", "age": 36}]
print([p["name"] for p in sorted(people, key=lambda p: p["age"])])
```

```text
['Cherry', 'Date', 'apple', 'banana']
['apple', 'banana', 'Cherry', 'Date']
['banana', 'Cherry', 'apple', 'Date']
['Ada', 'Grace', 'Alan']
```

- Strings are sorted by character number by default: **uppercase letters come
  before lowercase** (`Cherry` before `apple`).
- **`key`** is a function called once per element; the sort uses the value
  it returns. `str.casefold` ignores case, `len` orders by length.
- `reverse=True` reverses. Elements with equal keys **keep the order they
  came in**: `banana` and `Cherry` both have 6 letters, the first one stays
  in front.
- A list of dictionaries by a field: `key=lambda p: p["age"]`.

## operator: itemgetter and attrgetter

```python
from collections import namedtuple
from operator import attrgetter, itemgetter

rows = [("book", 3, 12.0), ("ink", 10, 0.5), ("pen", 3, 1.5)]
print(sorted(rows, key=itemgetter(1)))
print(sorted(rows, key=itemgetter(1, 2)))
Item = namedtuple("Item", "name stock price")
items = [Item(*row) for row in rows]
print([i.name for i in sorted(items, key=attrgetter("price"), reverse=True)])
print(itemgetter(0, 2)(rows[0]))
```

```text
[('book', 3, 12.0), ('pen', 3, 1.5), ('ink', 10, 0.5)]
[('pen', 3, 1.5), ('book', 3, 12.0), ('ink', 10, 0.5)]
['book', 'pen', 'ink']
('book', 12.0)
```

- **`itemgetter(1)`** does the same job as `lambda r: r[1]`; shorter and
  faster. For a dictionary, `itemgetter("age")`.
- **`itemgetter(1, 2)`** returns a tuple: first by stock, then by price when
  the stock is equal. Of the two products with stock 3, the cheaper one
  (`pen`) moved to the front.
- **`attrgetter("price")`** sorts by an attribute of objects (`namedtuple`,
  a class).
- `itemgetter(0, 2)` works on its own too: it pulls two fields from a row
  together.

## Several fields, different directions

```python
from operator import itemgetter

scores = [("ada", "math", 90), ("alan", "math", 85),
          ("grace", "cs", 90), ("linus", "cs", 85)]
by_score = sorted(scores, key=itemgetter(2), reverse=True)
print([s[0] for s in by_score])
two_pass = sorted(by_score, key=itemgetter(1))
print([s[0] for s in two_pass])
print([s[0] for s in sorted(scores, key=lambda s: (s[1], -s[2]))])
```

```text
['ada', 'grace', 'alan', 'linus']
['grace', 'linus', 'ada', 'alan']
['grace', 'linus', 'ada', 'alan']
```

"Ascending by subject, descending by score within the same subject" is done
in two ways:

- **Two passes:** first sort by the **secondary** field (score, descending),
  then by the **primary** field (subject). Python's sort is **stable**: in
  the second sort, elements that stay equal keep their order from the first.
- **One key:** the tuple `(subject, -score)`. A minus sign is enough to flip
  the direction of a number; since there is no minus for a text field, two
  passes are used there.

## heapq and bisect

```python
import bisect
import heapq

prices = [42, 7, 19, 88, 3, 56, 21]
print(heapq.nlargest(3, prices), heapq.nsmallest(2, prices))
for score in [33, 99, 77, 70, 89, 90]:
    print(score, "FDCBA"[bisect.bisect([60, 70, 80, 90], score)])
ordered = [10, 20, 30]
bisect.insort(ordered, 25)
print(ordered, bisect.bisect_left(ordered, 25), bisect.bisect_left(ordered, 26))
```

```text
[88, 56, 42] [3, 7]
33 F
99 A
77 C
70 C
89 B
90 A
[10, 20, 25, 30] 2 3
```

- **`heapq.nlargest(n, x)`** / **`nsmallest`**: the largest / smallest `n`
  elements without sorting the whole list. On large data it is faster than
  `sorted(...)[:10]` for a "top 10"; it takes a `key` too.
- **`bisect`** finds **where a value would go** in a sorted list by binary
  search. The score's position in the grade boundaries `[60, 70, 80, 90]`
  became the index into the letter list: 70, exactly on a boundary, is `C`
  (bisect puts it to the right of the boundary).
- **`bisect.insort`** inserts a value without breaking the order; no need to
  call `sort()` after every insertion. `bisect_left` gives the first position
  of a value.

## Common mistakes

```python
from functools import cmp_to_key

try:
    sorted([3, "a", 1])
except TypeError as error:
    print("TypeError:", error)
values = [3, None, 1]
print(sorted(values, key=lambda v: (v is None, v)))


def compare(a, b):
    return len(a) - len(b) or (a > b) - (a < b)


print(sorted(["bb", "a", "ccc", "ab"], key=cmp_to_key(compare)))
```

```text
TypeError: '<' not supported between instances of 'str' and 'int'
[1, 3, None]
['a', 'ab', 'bb', 'ccc']
```

- Python 3 does not compare text with numbers: a mixed list raises
  `TypeError`. Unify the types first or map them to a common value with
  `key`.
- In a list with `None`, the key `(v is None, v)` moves the `None`s to the
  end: the tuple's first element (`False < True`) is compared first, and
  `None` is never compared with a number.
- In older code you will see "a function comparing two elements" (cmp);
  **`cmp_to_key`** turns it into a `key`. In new code write a `key`
  directly: the comparison here is the same as `key=lambda s: (len(s), s)`.

## Summary

- `sorted` gives a new list, `list.sort()` works in place and returns `None`.
- `key=` once per element; `str.casefold`, `len`, `lambda`, `itemgetter`,
  `attrgetter`.
- A stable sort: multi-field sorting with two passes or a tuple key; a minus
  for direction on numbers.
- `heapq.nlargest` / `nsmallest` for the first n; `bisect` to find a position
  in a sorted list, `insort` to insert without breaking the order.
