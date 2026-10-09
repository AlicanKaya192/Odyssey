# Solving with Hashing

In earlier sections we measured that a set and a dictionary answer "is it in
there?" in `O(1)` on average, and used that to bring many algorithms down from
`O(n²)` to `O(n)`. In this section we see **how** that is possible, and then
collect the most common **hashing patterns**.

## The hash function: from a value to an address

A **hash function** takes a value and produces an **integer** from it. In
Python the built-in `hash()` does that:

```python
print(hash(42), hash(42) == hash(42))
print(hash((1, 2)) == hash((1, 2)))
try:
    hash([1, 2])
except TypeError as error:
    print(type(error).__name__, "-", error)
```

```text
42 True
True
TypeError - unhashable type: 'list'
```

There are two rules: **the same value always gives the same hash**; and only
**immutable** values (numbers, strings, tuples) can be hashed. A list cannot
be hashed because it can change: if its contents changed, its hash would
change too and it would lose its place in the dictionary.

## Inside a dictionary: buckets

A dictionary keeps a row of **buckets** inside. To place a key, it takes the
key's hash and divides by the number of buckets; the **remainder** is the
key's bucket. Looking up does the same calculation and goes straight to that
bucket; there is no need to walk the whole dictionary.

Let us write it ourselves with a small table of 8 buckets (keys are student
numbers, values are ages):

```python
class TinyMap:
    def __init__(self, size=8):
        self.buckets = [[] for _ in range(size)]

    def _bucket(self, key):
        return self.buckets[hash(key) % len(self.buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:          # the key is already there: update the value
                pair[1] = value
                return
        bucket.append([key, value])

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

ages = TinyMap()
for student_id, age in [(10, 31), (3, 25), (18, 40), (26, 19), (7, 52)]:
    ages.put(student_id, age)
for i, bucket in enumerate(ages.buckets):
    print(i, bucket)
print(ages.get(18), ages.get(99))
```

```text
0 []
1 []
2 [[10, 31], [18, 40], [26, 19]]
3 [[3, 25]]
4 []
5 []
6 []
7 [[7, 52]]
40 None
```

Since an integer's hash is the integer itself, 10, 18 and 26 leave the same
remainder (2) when divided by 8: all three fell into **the same bucket**. This
is called a **collision**. On a collision the few elements in the bucket are
checked one by one; as long as buckets stay short, those few steps are
constant: **`O(1)` on average**.

<figure class="fig">
  <div class="flow">
    <span class="node">Key: 18</span><span class="arrow">→</span>
    <span class="node">hash(18) = 18</span><span class="arrow">→</span>
    <span class="node">18 % 8 = 2</span><span class="arrow">→</span>
    <span class="node acc">Bucket 2</span>
  </div>
  <figcaption>A lookup does the same calculation; only the three pairs in bucket 2 are checked, the other seven buckets are never touched.</figcaption>
</figure>

A real dictionary resolves collisions another way (by probing for a free
slot), and as it fills up it **grows the number of buckets** and re-places
everything; like `append` on a list, the rebuilding is rare, so the average
stays constant.

## Your own class in a dictionary

When you use objects of your own class in a set or a dictionary, Python by
default looks at **the object's identity**: two objects with the same contents
count as different. To say "same contents, same object", write both `__eq__`
and `__hash__`:

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

class Point2:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    def __hash__(self):
        return hash((self.x, self.y))

a, b = Point(1, 2), Point(1, 2)
c, d = Point2(1, 2), Point2(1, 2)
print(a == b, len({a, b}))
print(c == d, len({c, d}))
```

```text
False 2
True 1
```

The rule: **two equal objects must have equal hashes.** If you write `__eq__`
and forget `__hash__`, Python makes the object unhashable. The easy way: hash
`x` and `y` together as a **tuple**.

## Hashing patterns

All the patterns below walk the list **once** and ask a set or a dictionary at
each step: `O(n)`.

**1. Seen it? (a set)** The first repeated element, removing repeats, what two
lists share. We did these in earlier sections.

**2. How many times? (a counter dictionary)** Word frequencies, the most
common value. `collections.Counter` is the ready-made one.

**3. Look for the complement (two-sum).** In an unsorted list, the **indices**
of two elements adding up to `target`. For each `x`, has its complement
`target - x` been seen before?

```python
def two_sum(numbers, target):
    seen = {}                          # value → index
    for i, x in enumerate(numbers):
        if target - x in seen:
            return seen[target - x], i
        seen[x] = i
    return None

print(two_sum([8, 3, 11, 5, 7], 12))
print(two_sum([8, 3, 11, 5, 7], 100))
```

```text
(3, 4)
None
```

`3 + 9`? There is no 9. `5 + 7 = 12`: 5 is at index 3, 7 at index 4. Two
pointers needed a **sorted** list; hashing is `O(n)` on an unsorted list too.
Its price is `O(n)` extra memory.

**4. Group by a shared key.** Grouping words made of the same letters
(anagrams): each word's **sorted letters** become the shared key.

```python
def group_anagrams(words):
    groups = {}
    for w in words:
        key = "".join(sorted(w))       # "listen" → "eilnst"
        groups.setdefault(key, []).append(w)
    return list(groups.values())

print(group_anagrams(["listen", "silent", "enlist", "google", "gogole", "cat"]))
```

```text
[['listen', 'silent', 'enlist'], ['google', 'gogole'], ['cat']]
```

Choosing a good key is the real craft of a hashing solution: "which piece of
information, used as the key, makes members of the same group land on the same
key?"

## Things to watch

- **String hashes change on every run.** For security Python adds a different
  random seed to string hashes in every process (we measured it in the Big
  Data path's MapReduce section). Do not write a hash value to a file and use
  it later; if you need a stable number, use `zlib.crc32` or `hashlib`.
- **A set has no order.** If you need order, use the set only for "seen it?"
  and keep the order in a separate list.
- **No mutable keys.** A list cannot be a key; turn it into a tuple
  (`tuple(items)`).

## Summary

- A hash function produces an integer from a value; equal values give equal
  hashes.
- A dictionary and a set put a key in bucket `hash % bucket_count`; a lookup
  goes straight to that bucket: `O(1)` on average.
- On a collision the few elements in the bucket are checked; the table grows
  as it fills.
- To use your own class as a key, `__eq__` and `__hash__` together.
- Patterns: seen it (a set), how many times (a counter), look for the
  complement (two-sum), group by a shared key (anagrams); all `O(n)` time,
  `O(n)` extra memory.
