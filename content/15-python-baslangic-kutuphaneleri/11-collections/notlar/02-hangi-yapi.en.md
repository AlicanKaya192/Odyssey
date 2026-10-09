## The same count, three ways

```python
from collections import Counter, defaultdict

text = "to be or not to be that is the question to be"
words = text.split()

counts1 = {}
for w in words:
    counts1[w] = counts1.get(w, 0) + 1
counts2 = defaultdict(int)
for w in words:
    counts2[w] += 1
counts3 = Counter(words)
print(counts1 == dict(counts2) == dict(counts3))
print(counts3.most_common(3))
by_length = defaultdict(list)
for w in sorted(set(words)):
    by_length[len(w)].append(w)
print(dict(by_length))
```

```text
True
[('to', 3), ('be', 3), ('or', 1)]
{2: ['be', 'is', 'or', 'to'], 3: ['not', 'the'], 8: ['question'], 4: ['that']}
```

All three ways gave the same result. The difference is readability:
`Counter(words)` states the intent in one word and `most_common` comes ready.
If you collect something other than counts (a list, a set), use
`defaultdict`; here the words were grouped by length. A plain dictionary with
`get` works everywhere, but it takes the most typing.

## Which structure?

| Need | Structure |
|---|---|
| Keep in order, append at the end | `list` |
| Find by key | `dict` |
| No repeats, "is it in there?" | `set` |
| A small unchanging record | `tuple` / `namedtuple` |
| Counting, the most frequent | `Counter` |
| Grouping by key | `defaultdict(list)` |
| Adding/removing at both ends, a queue | `deque` |
| The last N items | `deque(maxlen=N)` |
| Layers of settings | `ChainMap` |
| A record with changing fields and methods | `dataclass` (advanced Python) |

## Why does it matter?

The right structure makes the code both shorter and faster. On this
computer, removing 100,000 elements from the front took about 0.9 seconds
with a list and 0.005 seconds with a `deque`:

```python
import time
from collections import deque

items = list(range(100_000))
start = time.perf_counter()
while items:
    items.pop(0)
print("list", round(time.perf_counter() - start, 3))
items = deque(range(100_000))
start = time.perf_counter()
while items:
    items.popleft()
print("deque", round(time.perf_counter() - start, 4))
```

On every `pop(0)` the list shifts every element behind it one step; when the
number of elements doubles, the work quadruples. The `deque` does the same
small job on every removal. The times change from computer to computer; the
big gap between them does not.
