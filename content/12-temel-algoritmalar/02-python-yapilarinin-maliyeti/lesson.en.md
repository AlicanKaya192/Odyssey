# The Cost of Python's Structures

One-line operations in Python look innocent: `x in items`,
`items.insert(0, x)`, `items.pop(0)`. But as we saw in the previous section,
a loop can be hiding inside a single line. Knowing which structure does
which job cheaply and which expensively often makes a bigger difference
than changing the algorithm.

In this section we measure time too. Time depends on the computer, so look
not at the numbers themselves but at **the size of the gap between two
approaches**. All the measurements below were taken on this computer.

## How is a list stored?

A list keeps its elements in **boxes laid out side by side** in memory.
That is why reaching an element with `items[i]` is a single step however
long the list is: `O(1)`. Python works out where box `i` is and goes there.

And adding to the end with `append`? If the list were rebuilt on every
addition, that would be `O(n)`. Instead Python **reserves extra room**.
Let us watch how much memory the list takes:

```python
import sys

items = []
last = sys.getsizeof(items)
print(0, last)
for i in range(1, 33):
    items.append(i)
    size = sys.getsizeof(items)
    if size != last:
        print(i, size)
        last = size
```

```text
0 56
1 88
5 120
9 184
17 248
25 312
```

Out of 32 additions, the list grew in only a few (the number on the left is
the element count, on the right the bytes). When it grows, all elements are
copied to a new, wider place, which is expensive; but the reserved room
grows each time, so those moments get rarer and rarer. On average every
`append` is constant work: this is called **amortised O(1)**.

## Adding and removing at the front: O(n)

Because the boxes sit side by side, adding an element at the **front** means
shifting every element one box to the right. Removing from the front shifts
them all one to the left. With 50 000 elements in the list, that is 50 000
shifts per operation.

```python
import time

def measure(func):
    start = time.perf_counter()
    func()
    return round((time.perf_counter() - start) * 1000, 2)   # milliseconds

def add_to_end():
    items = []
    for i in range(50_000):
        items.append(i)

def add_to_front():
    items = []
    for i in range(50_000):
        items.insert(0, i)

print("append    :", measure(add_to_end), "ms")
print("insert(0) :", measure(add_to_front), "ms")
```

```text
append    : 2.3 ms
insert(0) : 334.0 ms
```

For removing from the front (a **queue**: first in, first out) Python has
`collections.deque`. A `deque` is open at both ends; adding and removing at
either end is `O(1)`:

```python
from collections import deque

def pop_list():
    items = list(range(50_000))
    while items:
        items.pop(0)

def pop_deque():
    items = deque(range(50_000))
    while items:
        items.popleft()

print("list.pop(0)     :", measure(pop_list), "ms")
print("deque.popleft() :", measure(pop_deque), "ms")
```

```text
list.pop(0)     : 254.44 ms
deque.popleft() : 3.73 ms
```

The price of a `deque`: reaching an element in the middle with `items[i]` is
not as fast as on a list. It is the right tool for work processed in order
and fed from both ends.

## `in`: searching a list, looking up a set

`x in items` on a list means linear search: it looks from start to end,
`O(n)`. A **set** and a **dict** instead place their elements according to a
number called a **hash**; checking whether a value is there takes a few
steps on average, however big the set is: `O(1)`. (How hashing works is in
the **Solving with Hashing** section.)

```python
numbers_list = list(range(100_000))
numbers_set = set(numbers_list)

def search_list():
    for _ in range(1000):
        -1 in numbers_list

def search_set():
    for _ in range(1000):
        -1 in numbers_set

print("list:", measure(search_list), "ms")
print("set :", measure(search_set), "ms")
```

```text
list: 973.79 ms
set : 0.05 ms
```

The same 1000 searches; the gap is thousands of times. The price of a set:
it keeps no order, does not keep the same element twice, and only accepts
**immutable** values (numbers, strings, tuples).

## Hidden O(n²)

Where this gap blows up most often is `in` on a list inside a loop. Let us
remove the repeats from a list without changing the order:

```python
data = list(range(20_000)) * 2      # every number twice

def unique_with_list():
    result = []
    for value in data:
        if value not in result:      # search in a list: O(n)
            result.append(value)
    return result

def unique_with_set():
    result = []
    seen = set()
    for value in data:
        if value not in seen:        # look up in a set: O(1)
            seen.add(value)
            result.append(value)
    return result

print("list:", measure(unique_with_list), "ms")
print("set :", measure(unique_with_set), "ms")
print(unique_with_list() == unique_with_set())
```

```text
list: 3816.9 ms
set : 3.51 ms
True
```

The two functions give the same result, but the first is `O(n²)` and the
second `O(n)`. The difference is a single line: which structure we ask `in`.
The extra set spends `O(n)` memory; in return seconds drop to milliseconds.

## A table of costs

| Operation | `list` | `set` / `dict` | `deque` |
|---|---|---|---|
| Indexing `x[i]` | `O(1)` | none / `O(1)` by key | `O(n)` |
| Adding to the end | `O(1)` amortised | `O(1)` | `O(1)` |
| Adding / removing at the front | `O(n)` | none | `O(1)` |
| Searching with `in` | `O(n)` | `O(1)` average | `O(n)` |
| Deleting a value | `O(n)` | `O(1)` average | `O(n)` |
| Keeps order? | yes | `set` no, `dict` insertion order | yes |

`sort` and `sorted` are `O(n log n)`: we will see why in the efficient sorts
section.

## Building a string piece by piece

Strings (`str`) in Python are **immutable**: `s = s + "x"` builds a new
string every time. When joining many pieces, collecting them in a list and
joining once at the end with `"".join(parts)` is both the clear and the safe
way.

## Summary

- List: indexing and adding to the end are fast; adding/removing at the
  front and `in` are slow (`O(n)`).
- `append` is amortised `O(1)`: the list reserves extra room.
- For a queue, `collections.deque`: `O(1)` at both ends.
- If "is it in there?" is asked often, use a set or a dict: `O(1)` on
  average.
- One-line `in`, `index`, `count`, `remove` and `insert(0, …)` inside a loop
  are hidden `O(n)`; they make the total `O(n²)`.
