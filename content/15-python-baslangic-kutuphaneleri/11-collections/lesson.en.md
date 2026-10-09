# collections

Lists, dictionaries, sets and tuples do most of the work. But some jobs are
written again and again in every project: counting how often something
occurs, grouping items by a key, a queue with items added and removed at both
ends, a small record whose fields are accessed by name. The **`collections`**
module gives ready, fast and readable structures for these.

## Counter: counting

```python
from collections import Counter

words = "the cat and the dog and the bird".split()
counts = Counter(words)
print(counts)
print(counts["the"], counts["fish"])
print(counts.most_common(2))
counts.update(["cat", "cat"])
print(counts["cat"], counts.total())
print(Counter("mississippi").most_common(3))
```

```text
Counter({'the': 3, 'and': 2, 'cat': 1, 'dog': 1, 'bird': 1})
3 0
[('the', 3), ('and', 2)]
3 10
[('i', 4), ('s', 4), ('p', 2)]
```

- **`Counter(list)`** counts how often each item occurs; it behaves like a
  dictionary.
- A missing item raises no error, it gives **0** (`counts["fish"]`).
- **`most_common(n)`** gives the `n` most frequent items with their counts,
  from most to least. One line for word frequencies, best-selling products,
  the most common error message.
- `update` adds and counts new items; `total()` is the sum of all counts.
- A string can be given too: it counts the letters. Items with equal counts
  (`i` and `s`) come in the order they were first seen.

Doing the same with a plain dictionary would need a
`counts[w] = counts.get(w, 0) + 1` loop.

## Arithmetic with Counter

```python
from collections import Counter

a = Counter(apples=3, pears=1)
b = Counter(apples=1, kiwis=2)
print(a + b)
print(a - b)
print(a & b, a | b)
```

```text
Counter({'apples': 4, 'kiwis': 2, 'pears': 1})
Counter({'apples': 2, 'pears': 1})
Counter({'apples': 1}) Counter({'apples': 3, 'kiwis': 2, 'pears': 1})
```

`+` adds the counts, `-` subtracts and **drops those falling to zero or
below** (`kiwis` disappeared). `&` takes the smaller count of each item, `|`
the bigger. It is used to merge two stock counts or to find "what is in the
order but not in stock".

## defaultdict: a default for a missing key

```python
from collections import defaultdict

pairs = [("fruit", "apple"), ("veg", "carrot"), ("fruit", "pear"),
         ("veg", "leek"), ("nut", "almond")]
groups = defaultdict(list)
for kind, name in pairs:
    groups[kind].append(name)
print(dict(groups))
counts = defaultdict(int)
for kind, _ in pairs:
    counts[kind] += 1
print(dict(counts))
plain = {}
try:
    plain["fruit"].append("apple")
except KeyError as error:
    print("KeyError:", error)
print(groups["missing"], "missing" in groups)
```

```text
{'fruit': ['apple', 'pear'], 'veg': ['carrot', 'leek'], 'nut': ['almond']}
{'fruit': 2, 'veg': 2, 'nut': 1}
KeyError: 'fruit'
[] True
```

- **`defaultdict(list)`**: the first time a missing key is accessed, it sets
  up an empty list for it; the "does the key exist, otherwise put an empty
  list" code goes away. The short way of **grouping**.
- `defaultdict(int)`: the default is `0`, like a counter.
- With a plain dictionary the same line raised `KeyError`.
- **Careful:** even **reading** creates the key: after `groups["missing"]`,
  `missing` is in the dictionary. To check whether it exists, use `in`.

## namedtuple: a tuple with named fields

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p, p.x, p[1])
x, y = p
print((x ** 2 + y ** 2) ** 0.5)
print(p._replace(x=10), p._asdict())
try:
    p.x = 5
except AttributeError as error:
    print("AttributeError:", error)
```

```text
Point(x=3, y=4) 3 4
5.0
Point(x=10, y=4) {'x': 3, 'y': 4}
AttributeError: can't set attribute
```

- **`namedtuple`** produces a tuple type: fields are accessed both **by
  name** (`p.x`) and **by position** (`p[1]`), and it can be unpacked into
  variables.
- Writing `point.x` instead of `point[0]` makes the code explain itself;
  useful when returning several values from a function.
- Being a tuple, it is **immutable**: a field cannot be assigned. A changed
  copy comes from `_replace`, a dictionary from `_asdict()`.

For records with changeable fields, default values and methods, the advanced
Python module has `dataclasses`.

## deque: a double-ended queue

```python
from collections import deque

queue = deque(["a", "b", "c"])
queue.append("d")
queue.appendleft("z")
print(queue)
print(queue.popleft(), queue.pop(), queue)
last = deque(maxlen=3)
for n in range(1, 7):
    last.append(n)
print(last)
d = deque([1, 2, 3, 4, 5])
d.rotate(2)
print(d)
```

```text
deque(['z', 'a', 'b', 'c', 'd'])
z d deque(['a', 'b', 'c'])
deque([4, 5, 6], maxlen=3)
deque([4, 5, 1, 2, 3])
```

- A **`deque`** (double-ended queue, pronounced "deck") is a list with fast
  adding and removing at both ends: `append` / `appendleft`, `pop` /
  `popleft`.
- Removing from the front of a list (`list.pop(0)`) shifts every element
  behind it; `deque.popleft()` does not. On this computer, removing 100,000
  elements from the front took about 0.9 seconds with a list and 0.005 seconds
  with a `deque`. Use `deque` for a queue (first in, first out).
- With **`maxlen`**, when full it drops the old item from the other end: for
  sliding windows like "the last 3 records".
- `rotate(n)` rotates the elements to the right.

## ChainMap: layered dictionaries

```python
from collections import ChainMap

defaults = {"theme": "dark", "lang": "en", "size": 14}
user = {"lang": "tr"}
settings = ChainMap(user, defaults)
print(settings["lang"], settings["theme"], len(settings))
user["size"] = 16
print(settings["size"], defaults["size"])
```

```text
tr dark 3
16 14
```

`ChainMap` searches several dictionaries in order: first the user's setting,
otherwise the default. The dictionaries are not copied; when `user` changes,
`settings` changes too, while `defaults` stays as it is. It suits layers of
settings (command line > environment variable > file > default).

## Summary

- `Counter`: counting, `most_common`, `+ - & |`.
- `defaultdict(list)` for grouping, `defaultdict(int)` for counting; reading
  also creates the key.
- `namedtuple`: an immutable record accessed by name.
- `deque`: fast adding/removing at both ends, a sliding window with `maxlen`.
- `ChainMap`: searching dictionaries layer by layer.
