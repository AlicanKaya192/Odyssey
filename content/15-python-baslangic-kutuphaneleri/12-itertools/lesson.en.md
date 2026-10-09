# itertools

Some loop patterns are rebuilt in every project: joining two lists end to
end, taking consecutive elements in pairs, a running total, splitting a list
into pieces, all pairwise combinations... **`itertools`** gives all of these
ready, fast and **lazy**: it does not collect the results in a list up
front, it produces them one by one as they are asked for. The same idea as
the generators you saw in the Python path.

`itertools` functions return **iterators**; to see them on screen we turn
them into lists with `list(...)`.

## Infinite iterators and islice

```python
from itertools import count, cycle, islice, repeat

print(list(islice(count(10, 5), 4)))
print(list(islice(cycle("AB"), 5)))
print(list(repeat("x", 3)))
for i, color in zip(range(4), cycle(["red", "green"])):
    print(i, color)
```

```text
[10, 15, 20, 25]
['A', 'B', 'A', 'B', 'A']
['x', 'x', 'x']
0 red
1 green
2 red
3 green
```

- **`count(start, step)`** counts forever; **`cycle`** goes round a sequence
  forever. Because they are infinite, they are never turned into a list on
  their own; the computer would keep trying until memory ran out.
- **`islice(iterator, n)`** takes the first `n` elements: slicing for
  iterators.
- Since `zip` stops at the shortest sequence, it pairs safely with `cycle`:
  like giving rows colours in turn.

## Joining, pairing, splitting

```python
from itertools import batched, chain, pairwise, zip_longest

print(list(chain([1, 2], (3, 4), "ab")))
names, scores = ["a", "b", "c"], [1, 2]
print(list(zip(names, scores)), list(zip_longest(names, scores, fillvalue=0)))
print(list(pairwise([10, 13, 9, 20])))
print([b - a for a, b in pairwise([10, 13, 9, 20])])
print(list(batched(range(7), 3)))
```

```text
[1, 2, 3, 4, 'a', 'b']
[('a', 1), ('b', 2)] [('a', 1), ('b', 2), ('c', 0)]
[(10, 13), (13, 9), (9, 20)]
[3, -4, 11]
[(0, 1, 2), (3, 4, 5), (6,)]
```

- **`chain`** walks sequences end to end without copying them.
- `zip` stops at the short sequence and loses `c`; **`zip_longest`** fills
  the gaps with `fillvalue`.
- **`pairwise`** gives consecutive pairs: ideal for consecutive differences
  (like a daily change).
- **`batched(seq, n)`** splits into pieces of `n`; the last piece may be
  shorter. Like sending records to an API 100 at a time (since Python 3.12).

## Accumulating and filtering

```python
import operator
from itertools import accumulate, compress, dropwhile, takewhile

sales = [5, 3, 8, 2, 7]
print(list(accumulate(sales)))
print(list(accumulate(sales, max)))
print(list(accumulate(sales, operator.mul)))
print(list(takewhile(lambda x: x < 8, sales)))
print(list(dropwhile(lambda x: x < 8, sales)))
print(list(compress("ABCDE", [1, 0, 1, 0, 1])))
```

```text
[5, 8, 16, 18, 25]
[5, 5, 8, 8, 8]
[5, 15, 120, 240, 1680]
[5, 3]
[8, 2, 7]
['A', 'C', 'E']
```

- **`accumulate`** gives the running total (5, 5+3, 5+3+8...). A second
  argument is another operation: with `max` "the highest so far", with
  `operator.mul` a running product.
- **`takewhile`** takes while the condition holds and **stops** at the first
  one that fails; **`dropwhile`** skips until then and gives everything
  after. The difference from `filter`: once the condition breaks, there is no
  going back.
- **`compress`** picks the ones that are true in the list beside it.

## groupby: gathering consecutive groups

```python
from itertools import groupby

words = ["apple", "avocado", "banana", "blueberry", "cherry", "apricot"]
for letter, group in groupby(words, key=lambda w: w[0]):
    print(letter, list(group))
print("---")
for letter, group in groupby(sorted(words), key=lambda w: w[0]):
    print(letter, list(group))
print([(k, len(list(g))) for k, g in groupby("aaabccdddd")])
```

```text
a ['apple', 'avocado']
b ['banana', 'blueberry']
c ['cherry']
a ['apricot']
---
a ['apple', 'apricot', 'avocado']
b ['banana', 'blueberry']
c ['cherry']
[('a', 3), ('b', 1), ('c', 2), ('d', 4)]
```

**`groupby`** gathers only items with the same key that **stand next to each
other**: because `apricot` is at the end, the `a` group came out twice. If
you want all groups, first **sort by the same key**. The last line counts
consecutive repeats (`aaab...` → `a` 3 times): used for simple compression
and "how many days in a row" questions. If you do not want to sort, the
previous section's `defaultdict(list)` fits better.

## Combinatorics

```python
import math
from itertools import (combinations, combinations_with_replacement,
                       permutations, product)

print(list(product("AB", [1, 2])))
print(sum(1 for _ in product(range(10), repeat=3)))
print(list(permutations("ABC", 2)))
print(list(combinations("ABCD", 2)))
print(list(combinations_with_replacement("AB", 2)))
print(sum(1 for _ in combinations(range(20), 6)), math.comb(20, 6))
```

```text
[('A', 1), ('A', 2), ('B', 1), ('B', 2)]
1000
[('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]
[('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('C', 'D')]
[('A', 'A'), ('A', 'B'), ('B', 'B')]
38760 38760
```

| Function | What it produces | Order matters | Repeats |
|---|---|---|---|
| `product(a, b)` | every `a` with every `b` | yes | yes |
| `product(x, repeat=3)` | like a three-digit code | yes | yes |
| `permutations(x, k)` | arrangements of `k` | yes | no |
| `combinations(x, k)` | groups of `k` | no | no |
| `combinations_with_replacement(x, k)` | groups with repeats | no | yes |

The 1000 possibilities of a three-digit lock were counted with `product`, the
number of 6-person groups from 20 people with `combinations`; the result is
the same as `math.comb`. The number of combinations grows very fast: trying
every possibility is only feasible for small inputs.

## A common mistake: an iterator runs out once

```python
from itertools import islice

numbers = map(int, ["1", "2", "3"])
print(sum(numbers), sum(numbers))
it = iter(range(10))
print(list(islice(it, 3)), list(islice(it, 3)))
squares = (n * n for n in range(5))
print(list(squares), list(squares))
```

```text
6 0
[0, 1, 2] [3, 4, 5]
[0, 1, 4, 9, 16] []
```

An iterator is walked once: the first `sum` of the `map` gave 6, the second
0. `islice` **went on** from the same iterator (0–2, then 3–5). If you need
the result twice, turn it into a list once and use the list.

## Summary

- `count`, `cycle`, `repeat` are infinite; limit them with `islice`.
- `chain` end to end, `zip_longest` fills gaps, `pairwise` consecutive
  pairs, `batched` pieces.
- `accumulate` running results; `takewhile` / `dropwhile` until the condition
  breaks; `compress` picks.
- `groupby` groups only neighbours: sort first.
- `product`, `permutations`, `combinations`.
- Iterators run out once; turn them into a list if you need them again.
